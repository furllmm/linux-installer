#!/bin/bash
# Modern Linux Installer v2.0.0 - Linux Requirements Setup

set -e  # Exit on any error

echo "========================================"
echo " Modern Linux Installer v2.0.0 Setup"
echo "========================================"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    print_error "This script requires root privileges for package installation."
    echo "Please run: sudo $0"
    exit 1
fi

print_info "Running as root - proceeding with installation..."
echo

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
    VERSION=$VERSION_ID
else
    print_error "Cannot detect Linux distribution"
    exit 1
fi

print_info "Detected: $PRETTY_NAME"
echo

# Update package lists
echo "[1/5] Updating package lists..."
case $DISTRO in
    ubuntu|debian)
        apt-get update -qq
        print_status "Package lists updated (apt)"
        ;;
    fedora|centos|rhel)
        if command -v dnf &> /dev/null; then
            dnf check-update -q || true
            print_status "Package lists updated (dnf)"
        else
            yum check-update -q || true
            print_status "Package lists updated (yum)"
        fi
        ;;
    arch|manjaro)
        pacman -Sy --noconfirm
        print_status "Package lists updated (pacman)"
        ;;
    *)
        print_warning "Unknown distribution, attempting with apt..."
        apt-get update -qq || print_error "Failed to update packages"
        ;;
esac
echo

# Install system dependencies
echo "[2/5] Installing system dependencies..."
case $DISTRO in
    ubuntu|debian)
        apt-get install -y \
            python3 \
            python3-tk \
            python3-pip \
            qemu-utils \
            p7zip-full \
            grub-common \
            grub2-common \
            util-linux \
            mount \
            sudo
        print_status "Dependencies installed (apt)"
        ;;
    fedora|centos|rhel)
        if command -v dnf &> /dev/null; then
            dnf install -y \
                python3 \
                python3-tkinter \
                python3-pip \
                qemu-img \
                p7zip \
                grub2-tools \
                util-linux \
                sudo
        else
            yum install -y \
                python3 \
                tkinter \
                python3-pip \
                qemu-img \
                p7zip \
                grub2-tools \
                util-linux \
                sudo
        fi
        print_status "Dependencies installed (dnf/yum)"
        ;;
    arch|manjaro)
        pacman -S --noconfirm \
            python \
            tk \
            python-pip \
            qemu \
            p7zip \
            grub \
            util-linux \
            sudo
        print_status "Dependencies installed (pacman)"
        ;;
    *)
        print_warning "Attempting installation with apt..."
        apt-get install -y python3 python3-tk qemu-utils p7zip-full grub-common || \
            print_error "Failed to install dependencies"
        ;;
esac
echo

# Verify Python version
echo "[3/5] Verifying Python installation..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 6 ]; then
    print_status "Python $PYTHON_VERSION meets requirements (3.6+)"
else
    print_error "Python $PYTHON_VERSION is too old. Python 3.6+ required."
    exit 1
fi

# Test tkinter
python3 -c "import tkinter; print('tkinter test passed')" 2>/dev/null
if [ $? -eq 0 ]; then
    print_status "tkinter support confirmed"
else
    print_error "tkinter not available"
    exit 1
fi
echo

# Verify tools
echo "[4/5] Verifying installed tools..."

# Check qemu-img
if command -v qemu-img &> /dev/null; then
    QEMU_VERSION=$(qemu-img --version | head -1)
    print_status "qemu-img available: $QEMU_VERSION"
else
    print_error "qemu-img not found"
    exit 1
fi

# Check 7z
if command -v 7z &> /dev/null; then
    print_status "7z available"
elif command -v 7za &> /dev/null; then
    print_status "7za available"
elif command -v 7zr &> /dev/null; then
    print_status "7zr available"
else
    print_error "7-Zip not found"
    exit 1
fi

# Check grub tools
if command -v grub-install &> /dev/null; then
    print_status "grub-install available"
else
    print_warning "grub-install not found - GRUB installation may not work"
fi

# Check mount/umount
if command -v mount &> /dev/null && command -v umount &> /dev/null; then
    print_status "mount/umount tools available"
else
    print_error "mount/umount tools not found"
    exit 1
fi
echo

# Set up permissions and final checks
echo "[5/5] Final setup and permissions..."

# Check if user can use sudo
if groups $SUDO_USER | grep -q sudo; then
    print_status "User has sudo privileges"
else
    print_warning "User may not have sudo privileges - some features may not work"
fi

# Create desktop entry if running in desktop environment
if [ -n "$SUDO_USER" ] && [ -d "/home/$SUDO_USER/Desktop" ]; then
    DESKTOP_FILE="/home/$SUDO_USER/Desktop/modern-linux-installer.desktop"
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Modern Linux Installer
Comment=Professional Linux installation tool
Exec=python3 $(pwd)/linux-installer.py
Icon=applications-system
Terminal=false
Categories=System;
EOF
    chown $SUDO_USER:$SUDO_USER "$DESKTOP_FILE"
    chmod +x "$DESKTOP_FILE"
    print_status "Desktop shortcut created"
fi

echo
echo "========================================"
echo " Setup Summary"
echo "========================================"
print_status "Python 3.6+ with tkinter support"
print_status "QEMU tools for VHD management"
print_status "7-Zip for ISO extraction"
print_status "GRUB tools for bootloader installation"
print_status "System utilities (mount, sudo, etc.)"
echo
print_info "You can now run the Modern Linux Installer:"
echo "python3 linux-installer.py"
echo
print_info "For full functionality, ensure your user has sudo privileges"
echo
print_info "Some operations (disk formatting, mounting) require sudo access"
echo

echo "Setup completed successfully! 🐧"