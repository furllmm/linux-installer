# 🐧 Modern Linux Installer v2.0.0

A professional, modern Linux installation tool with an intuitive GUI for creating Linux installations on VHD files and direct partition installations with dual-boot support.

## ✨ Features

### 🎨 Modern User Interface
- **Dark Theme**: Professional dark UI with modern styling
- **Tabbed Interface**: Organized workflow with dedicated tabs for different operations
- **Real-time Progress**: Live status updates with progress indicators and emoji feedback
- **Responsive Design**: Scalable interface that adapts to different screen sizes

### 🔧 Installation Methods
- **VHD Installation**: Create and manage Virtual Hard Disk files for Linux installations
- **Direct Partition Installation**: Install directly to existing ext4 partitions
- **Dual-Boot Integration**: Automatic Windows boot menu configuration with BCDEDIT

### 🐧 Distribution Support
Auto-detection for major Linux distributions:
- Ubuntu/Debian (Casper-based)
- Arch Linux & Manjaro
- Fedora/Red Hat
- Slax/Slackware
- TinyCore/Puppy Linux
- Generic GRUB-based distributions

### 🛠️ Advanced Features
- **Cross-Platform**: Native support for Windows and Linux
- **WSL Integration**: Seamless Windows Subsystem for Linux support
- **GRUB Management**: Automatic bootloader installation and configuration
- **System Diagnostics**: Built-in dependency checking and system information
- **Error Logging**: Comprehensive error tracking and log viewing
- **Administrator Detection**: Automatic privilege checking with warnings

## 📋 System Requirements

### Windows
- **OS**: Windows 10/11 (64-bit recommended)
- **Python**: 3.6 or higher
- **WSL**: Windows Subsystem for Linux enabled
- **Dependencies**: 7-Zip, QEMU
- **Privileges**: Administrator rights for full functionality

### Linux
- **OS**: Ubuntu 18.04+, Debian 10+, or equivalent
- **Python**: 3.6 or higher with tkinter support
- **Dependencies**: qemu-utils, p7zip-full, grub-common
- **Privileges**: sudo access for disk operations

## 🚀 Quick Installation

### Windows Setup

# Clone the repository
git clone https://github.com/yourusername/modern-linux-installer
cd modern-linux-installer

# Run automated setup
requirements.bat


### Linux Setup

# Clone the repository
git clone https://github.com/yourusername/modern-linux-installer
cd modern-linux-installer

# Run automated setup
sudo chmod +x requirements.sh
sudo ./requirements.sh


## 📖 Usage Guide

### 1. 📁 Setup & ISO Selection
- Browse and select your Linux distribution ISO file
- Automatic distribution detection and validation
- Extract root filesystem from ISO

### 2. 💾 VHD Installation
- Create new VHD files (2-100GB configurable)
- Format VHD as ext4 filesystem
- Copy extracted root filesystem to VHD
- Install GRUB bootloader
- Add VHD to Windows boot menu

### 3. 🗂️ Partition Installation
- Scan and select existing ext4 partitions
- Direct installation to physical partitions
- GRUB installation to partition boot sector

### 4. ⚙️ Advanced Tools
- System information and diagnostics
- Dependency verification
- Application logs and error tracking
- About and help information

## 🔧 Configuration

### Default Paths (Windows)

7-Zip: J:\portableapps\PortableApps\7-ZipPortable\App\7-Zip\7z.exe
QEMU: D:\win\qemu\qemu-img.exe


### Customization
Edit the paths in `linux-installer.py` if your installations differ:

self._7z_path = r"YOUR_7ZIP_PATH\7z.exe"
self.qemu_path = r"YOUR_QEMU_PATH\qemu-img.exe"


## 🚨 Important Notes

### Administrator Privileges
- **Windows**: Run as Administrator for boot menu modifications
- **Linux**: Use sudo for disk operations and mounting
- **Limited Mode**: Basic functionality available without admin rights

### WSL Requirements (Windows)
- WSL must be enabled and configured
- Ubuntu or Debian distribution recommended
- Required for ext4 formatting and Linux filesystem operations

### Backup Warning
⚠️ **Always backup important data before disk operations!**
- VHD creation is generally safe
- Partition operations modify existing disks
- Boot menu changes affect system startup

## 🐛 Troubleshooting

### Common Issues
1. **Dependencies Not Found**: Run requirements script again
2. **WSL Not Available**: Enable WSL in Windows Features
3. **Permission Denied**: Run with administrator/sudo privileges
4. **ISO Not Detected**: Ensure ISO is a valid Linux distribution

### Log Files
- Error logs are automatically saved to `error.log`
- Use "View Logs" in the Advanced tab for troubleshooting
- Include log contents when reporting issues

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

# Clone your fork
git clone https://github.com/yourusername/modern-linux-installer
cd modern-linux-installer

# Install development dependencies
pip install -r requirements-dev.txt  # If available

# Run the application
python linux-installer.py


## 📄 License

This project is licensed under the MIT License 

## 🙏 Acknowledgments

- **7-Zip** for reliable archive extraction
- **QEMU** for VHD creation and management
- **Python tkinter** for the GUI framework
- **Linux community** for inspiration and testing

## 📞 Support

- **Email**:  furfur638@gmail.com

---

**Developed with ❤️ for the Linux community**

*Making Linux installation accessible and modern for everyone*
---

Support & Donations 🙏
If you find this tool helpful and want to support its development, feel free to donate! Every contribution helps me dedicate more time and improve the project.

Ethereum (EVM, low-fee coins preferred):
0xa3c4468d82881afb64e3fb5100aa0d3e6ea1f4dd

Thank you for being part of this journey! 🚀

If you liked this project, please share it to reach more people! ⭐️🙏

