#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import subprocess
import ctypes
import platform
import sys
import re
import tempfile
import traceback
import json
from threading import Thread
import time

class ModernLinuxInstaller:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.validate_dependencies()
        self.create_ui()
        
    def setup_window(self):
        """Configure the main window with modern styling"""
        self.root.title("🐧 Modern Linux Installer")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        
        # Configure modern ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define color scheme
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3d3d3d',
            'accent': '#007acc',
            'accent_hover': '#005a9e',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#404040'
        }
        
        # Configure ttk styles
        self.configure_styles()
        
    def configure_styles(self):
        """Configure modern ttk widget styles"""
        # Configure notebook (tabs)
        self.style.configure('Modern.TNotebook', 
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        self.style.configure('Modern.TNotebook.Tab',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           padding=[20, 10],
                           borderwidth=0)
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['accent']),
                                ('active', self.colors['bg_tertiary'])])
        
        # Configure frames
        self.style.configure('Modern.TFrame',
                           background=self.colors['bg_secondary'],
                           borderwidth=1,
                           relief='solid')
        
        # Configure labels
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 16, 'bold'))
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 10))
        self.style.configure('Status.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9))
        
        # Configure buttons
        self.style.configure('Modern.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 9))
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['accent_hover']),
                                ('pressed', self.colors['accent_hover'])])
        
        # Configure progressbar
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_tertiary'],
                           borderwidth=0,
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])

    def setup_variables(self):
        """Initialize all tkinter variables"""
        self.iso_path = tk.StringVar()
        self.vhd_size_gb = tk.IntVar(value=8)
        self.selected_vhd_path = tk.StringVar()
        self.selected_partition = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready to start installation")
        self.progress_var = tk.DoubleVar()
        
        # Platform info
        self.is_linux = platform.system().lower() == "linux"
        self.is_windows = platform.system().lower() == "windows"
        
    def validate_dependencies(self):
        """Validate required executables with modern error handling"""
        self._7z_path = r"J:\portableapps\PortableApps\7-ZipPortable\App\7-Zip\7z.exe"
        self.qemu_path = r"D:\win\qemu\qemu-img.exe"
        
        # Check for 7z
        if not os.path.exists(self._7z_path):
            found_7z = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.exists(os.path.join(path, "7z.exe")):
                    self._7z_path = os.path.join(path, "7z.exe")
                    found_7z = True
                    break
            if not found_7z:
                self.show_error("Missing Dependency", 
                              "7-Zip not found!\nPlease install 7-Zip or update the path in the script.")
                sys.exit(1)
        
        # Check for qemu-img
        if not os.path.exists(self.qemu_path):
            found_qemu = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.exists(os.path.join(path, "qemu-img.exe")):
                    self.qemu_path = os.path.join(path, "qemu-img.exe")
                    found_qemu = True
                    break
            if not found_qemu:
                self.show_error("Missing Dependency", 
                              "QEMU not found!\nPlease install QEMU or update the path in the script.")
                sys.exit(1)

    def create_ui(self):
        """Create the modern UI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_setup_tab()
        self.create_vhd_tab()
        self.create_partition_tab()
        self.create_advanced_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
        # Admin check
        if self.is_windows and not self.is_admin():
            self.show_admin_warning()

    def create_header(self, parent):
        """Create the application header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side='left')
        
        title_label = tk.Label(title_frame, 
                              text="🐧 Modern Linux Installer",
                              font=('Segoe UI', 24, 'bold'),
                              fg=self.colors['text_primary'],
                              bg=self.colors['bg_primary'])
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_frame,
                                 text="Professional Linux installation tool for Windows & Linux",
                                 font=('Segoe UI', 11),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_primary'])
        subtitle_label.pack(anchor='w')
        
        # Version info
        version_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        version_frame.pack(side='right')
        
        version_label = tk.Label(version_frame,
                                text="v2.0.0",
                                font=('Segoe UI', 10, 'bold'),
                                fg=self.colors['accent'],
                                bg=self.colors['bg_primary'])
        version_label.pack()
        
        platform_label = tk.Label(version_frame,
                                 text=f"Running on {platform.system()}",
                                 font=('Segoe UI', 9),
                                 fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_primary'])
        platform_label.pack()

    def create_setup_tab(self):
        """Create the setup/ISO selection tab"""
        setup_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(setup_frame, text='📁 Setup & ISO')
        
        # ISO Selection Section
        iso_section = self.create_section(setup_frame, "ISO File Selection", "Select your Linux distribution ISO file")
        
        # ISO path display
        iso_display_frame = tk.Frame(iso_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        iso_display_frame.pack(fill='x', pady=(10, 5))
        
        iso_icon = tk.Label(iso_display_frame, text="💿", font=('Segoe UI', 16),
                           bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        iso_icon.pack(side='left', padx=10, pady=10)
        
        iso_path_label = tk.Label(iso_display_frame, textvariable=self.iso_path,
                                 font=('Segoe UI', 10), wraplength=600,
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                                 justify='left')
        iso_path_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)
        
        # Browse button
        browse_btn = self.create_modern_button(iso_section, "🔍 Browse ISO File", self.browse_iso)
        browse_btn.pack(pady=5)
        
        # Detected distribution info
        self.distro_info_frame = tk.Frame(iso_section, bg=self.colors['bg_secondary'])
        self.distro_info_frame.pack(fill='x', pady=10)
        
        # Extraction Section
        extract_section = self.create_section(setup_frame, "Root Filesystem Extraction", "Extract the Linux root filesystem from ISO")
        
        extract_btn = self.create_modern_button(extract_section, "📦 Extract Root Filesystem", self.extract_rootfs)
        extract_btn.pack(pady=10)

    def create_vhd_tab(self):
        """Create the VHD installation tab"""
        vhd_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(vhd_frame, text='💾 VHD Installation')
        
        # VHD Creation Section
        creation_section = self.create_section(vhd_frame, "VHD Creation & Management", "Create and manage Virtual Hard Disk files")
        
        # VHD Size selector
        size_frame = tk.Frame(creation_section, bg=self.colors['bg_secondary'])
        size_frame.pack(fill='x', pady=10)
        
        tk.Label(size_frame, text="VHD Size:", font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side='left')
        
        size_scale = tk.Scale(size_frame, from_=2, to=100, orient='horizontal',
                             variable=self.vhd_size_gb, bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_primary'], highlightthickness=0,
                             troughcolor=self.colors['bg_primary'])
        size_scale.pack(side='left', padx=10, fill='x', expand=True)
        
        size_label = tk.Label(size_frame, textvariable=self.vhd_size_gb,
                             font=('Segoe UI', 10, 'bold'),
                             bg=self.colors['bg_secondary'], fg=self.colors['accent'])
        size_label.pack(side='right')
        
        tk.Label(size_frame, text="GB", font=('Segoe UI', 10),
                bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side='right')
        
        # VHD operations
        vhd_ops_frame = tk.Frame(creation_section, bg=self.colors['bg_secondary'])
        vhd_ops_frame.pack(fill='x', pady=10)
        
        # Left column
        left_col = tk.Frame(vhd_ops_frame, bg=self.colors['bg_secondary'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_modern_button(left_col, "🆕 Create VHD", self.create_and_mount_vhd).pack(fill='x', pady=2)
        self.create_modern_button(left_col, "📁 Select VHD", self.select_ext4_vhd).pack(fill='x', pady=2)
        self.create_modern_button(left_col, "🔧 Format as ext4", self.format_vhd_ext4).pack(fill='x', pady=2)
        
        # Right column
        right_col = tk.Frame(vhd_ops_frame, bg=self.colors['bg_secondary'])
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_modern_button(right_col, "📋 Copy RootFS", self.copy_rootfs_to_vhd).pack(fill='x', pady=2)
        self.create_modern_button(right_col, "⚙️ Install GRUB", self.install_grub).pack(fill='x', pady=2)
        self.create_modern_button(right_col, "🚀 Add to Boot Menu", self.add_vhd_to_boot_menu).pack(fill='x', pady=2)
        
        # Selected VHD display
        vhd_display_frame = tk.Frame(creation_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        vhd_display_frame.pack(fill='x', pady=10)
        
        vhd_icon = tk.Label(vhd_display_frame, text="💾", font=('Segoe UI', 16),
                           bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        vhd_icon.pack(side='left', padx=10, pady=10)
        
        vhd_path_label = tk.Label(vhd_display_frame, textvariable=self.selected_vhd_path,
                                 font=('Segoe UI', 10), wraplength=600,
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        vhd_path_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)

    def create_partition_tab(self):
        """Create the partition installation tab"""
        partition_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(partition_frame, text='🗂️ Partition Installation')
        
        # Partition Selection Section
        partition_section = self.create_section(partition_frame, "Partition Installation", "Install directly to an existing ext4 partition")
        
        # Partition selection
        select_frame = tk.Frame(partition_section, bg=self.colors['bg_secondary'])
        select_frame.pack(fill='x', pady=10)
        
        self.create_modern_button(select_frame, "🔍 Select ext4 Partition", self.select_ext4_partition).pack(side='left')
        
        refresh_btn = self.create_modern_button(select_frame, "🔄 Refresh", self.refresh_partitions)
        refresh_btn.pack(side='right')
        
        # Selected partition display
        partition_display_frame = tk.Frame(partition_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        partition_display_frame.pack(fill='x', pady=10)
        
        partition_icon = tk.Label(partition_display_frame, text="🗂️", font=('Segoe UI', 16),
                                 bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        partition_icon.pack(side='left', padx=10, pady=10)
        
        partition_label = tk.Label(partition_display_frame, textvariable=self.selected_partition,
                                  font=('Segoe UI', 10), wraplength=600,
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        partition_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)
        
        # Partition operations
        partition_ops_frame = tk.Frame(partition_section, bg=self.colors['bg_secondary'])
        partition_ops_frame.pack(fill='x', pady=20)
        
        # Operations buttons
        ops_left = tk.Frame(partition_ops_frame, bg=self.colors['bg_secondary'])
        ops_left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_modern_button(ops_left, "📋 Copy RootFS to Partition", self.copy_rootfs_to_partition).pack(fill='x', pady=5)
        
        ops_right = tk.Frame(partition_ops_frame, bg=self.colors['bg_secondary'])
        ops_right.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_modern_button(ops_right, "⚙️ Install GRUB to Partition", self.install_grub_to_partition).pack(fill='x', pady=5)

    def create_advanced_tab(self):
        """Create the advanced settings tab"""
        advanced_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(advanced_frame, text='⚙️ Advanced')
        
        # System Information Section
        sys_section = self.create_section(advanced_frame, "System Information", "Current system and dependency status")
        
        info_frame = tk.Frame(sys_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        info_frame.pack(fill='x', pady=10)
        
        # System info
        info_text = f"""
🖥️ Operating System: {platform.system()} {platform.release()}
🏗️ Architecture: {platform.machine()}
🐍 Python Version: {platform.python_version()}
📁 7-Zip Path: {self._7z_path}
💿 QEMU Path: {self.qemu_path}
👤 Admin Rights: {'Yes' if self.is_admin() else 'No'}
        """.strip()
        
        info_label = tk.Label(info_frame, text=info_text, font=('Consolas', 9),
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             justify='left')
        info_label.pack(padx=20, pady=15)
        
        # Tools Section
        tools_section = self.create_section(advanced_frame, "System Tools", "Additional utilities and diagnostics")
        
        tools_frame = tk.Frame(tools_section, bg=self.colors['bg_secondary'])
        tools_frame.pack(fill='x', pady=10)
        
        self.create_modern_button(tools_frame, "🔧 Check Dependencies", self.check_dependencies).pack(side='left', padx=5)
        self.create_modern_button(tools_frame, "📋 View Logs", self.view_logs).pack(side='left', padx=5)
        self.create_modern_button(tools_frame, "ℹ️ About", self.show_about).pack(side='right', padx=5)

    def create_section(self, parent, title, description):
        """Create a modern section with title and description"""
        section_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        section_frame.pack(fill='x', padx=20, pady=10)
        
        # Section header
        header_frame = tk.Frame(section_frame, bg=self.colors['bg_tertiary'])
        header_frame.pack(fill='x')
        
        title_label = tk.Label(header_frame, text=title, font=('Segoe UI', 12, 'bold'),
                              bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        title_label.pack(side='left', padx=15, pady=10)
        
        desc_label = tk.Label(header_frame, text=description, font=('Segoe UI', 9),
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'])
        desc_label.pack(side='right', padx=15, pady=10)
        
        # Section content
        content_frame = tk.Frame(section_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        return content_frame

    def create_modern_button(self, parent, text, command, style='primary'):
        """Create a modern styled button"""
        if style == 'primary':
            bg_color = self.colors['accent']
            hover_color = self.colors['accent_hover']
        elif style == 'success':
            bg_color = self.colors['success']
            hover_color = '#45a049'
        elif style == 'warning':
            bg_color = self.colors['warning']
            hover_color = '#e68900'
        elif style == 'error':
            bg_color = self.colors['error']
            hover_color = '#d32f2f'
        else:
            bg_color = self.colors['bg_tertiary']
            hover_color = self.colors['border']
        
        button = tk.Button(parent, text=text, command=command,
                          bg=bg_color, fg=self.colors['text_primary'],
                          font=('Segoe UI', 9, 'bold'), relief='flat',
                          borderwidth=0, cursor='hand2')
        
        # Hover effects
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=bg_color)
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button

    def create_status_bar(self, parent):
        """Create the modern status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        status_frame.pack(fill='x', pady=(20, 0))
        
        # Status icon and text
        status_content = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        status_content.pack(side='left', fill='x', expand=True)
        
        self.status_icon = tk.Label(status_content, text="✅", font=('Segoe UI', 12),
                                   bg=self.colors['bg_secondary'], fg=self.colors['success'])
        self.status_icon.pack(side='left', padx=10, pady=8)
        
        self.status_label = tk.Label(status_content, textvariable=self.status_text,
                                    font=('Segoe UI', 10), bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'])
        self.status_label.pack(side='left', pady=8)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(status_frame, style='Modern.Horizontal.TProgressbar',
                                           variable=self.progress_var, length=200)
        self.progress_bar.pack(side='right', padx=10, pady=8)

    def update_status(self, message, status_type='info', progress=None):
        """Update status bar with modern styling"""
        icons = {
            'info': '💡',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'working': '⚙️'
        }
        
        colors = {
            'info': self.colors['text_primary'],
            'success': self.colors['success'],
            'warning': self.colors['warning'],
            'error': self.colors['error'],
            'working': self.colors['accent']
        }
        
        self.status_text.set(message)
        self.status_icon.config(text=icons.get(status_type, '💡'),
                               fg=colors.get(status_type, self.colors['text_primary']))
        
        if progress is not None:
            self.progress_var.set(progress)
        
        self.root.update()

    def show_error(self, title, message):
        """Show modern error dialog"""
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        """Show modern success dialog"""
        messagebox.showinfo(title, message)

    def show_admin_warning(self):
        """Show modern admin warning"""
        messagebox.showwarning("Administrator Rights Required",
                              "🔐 Administrator privileges are required for:\n\n"
                              "• Disk operations and formatting\n"
                              "• Boot menu modifications\n"
                              "• System-level installations\n\n"
                              "Please run this application as administrator for full functionality.")

    def is_admin(self):
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    # Core functionality methods (keeping the same logic but with modern UI updates)
    
    def browse_iso(self):
        """Browse for ISO file with modern feedback"""
        self.update_status("Selecting ISO file...", 'working')
        
        file_path = filedialog.askopenfilename(
            title="Select Linux ISO File",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        
        if file_path:
            self.iso_path.set(file_path)
            self.update_status("ISO file selected successfully", 'success')
            
            # Detect distribution in background
            Thread(target=self.detect_and_display_distro, args=(file_path,), daemon=True).start()
        else:
            self.iso_path.set("No ISO file selected")
            self.update_status("ISO selection cancelled", 'warning')

    def detect_and_display_distro(self, iso_path):
        """Detect distribution and update UI"""
        self.update_status("Analyzing ISO file...", 'working', 25)
        
        distro = self.detect_iso_base(iso_path)
        
        # Clear previous distro info
        for widget in self.distro_info_frame.winfo_children():
            widget.destroy()
        
        if distro:
            # Create distro info display
            info_frame = tk.Frame(self.distro_info_frame, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
            info_frame.pack(fill='x', pady=5)
            
            distro_icon = tk.Label(info_frame, text="🐧", font=('Segoe UI', 16),
                                  bg=self.colors['bg_tertiary'], fg=self.colors['success'])
            distro_icon.pack(side='left', padx=10, pady=8)
            
            distro_label = tk.Label(info_frame, text=f"Detected: {distro}",
                                   font=('Segoe UI', 10, 'bold'),
                                   bg=self.colors['bg_tertiary'], fg=self.colors['success'])
            distro_label.pack(side='left', padx=(0, 10), pady=8)
            
            self.update_status(f"Detected distribution: {distro}", 'success', 100)
        else:
            self.update_status("Could not detect distribution type", 'warning', 100)

    def detect_iso_base(self, iso_path: str):
        """Detect ISO distribution type"""
        try:
            result = subprocess.run([self._7z_path, "l", iso_path], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return None
                
            output = result.stdout.lower()
            
            if "casper" in output or "filesystem.squashfs" in output:
                return "Ubuntu/Debian (Casper)"
            elif "live" in output and "slax" in output:
                return "Slax/Slackware"
            elif "archiso" in output or "airootfs" in output:
                return "Arch Linux"
            elif "manjaro" in output:
                return "Manjaro Linux"
            elif "fedora" in output or "squashfs.img" in output:
                return "Fedora/Red Hat"
            elif "initrd.gz" in output and "vmlinuz" in output and "rootfs.gz" in output:
                return "TinyCore/Puppy Linux"
            elif "boot/grub" in output:
                return "Generic GRUB-based"
                
        except Exception:
            pass
        return None

    def extract_rootfs(self):
        """Extract root filesystem with progress"""
        if not self.iso_path.get() or self.iso_path.get() == "No ISO file selected":
            self.show_error("Error", "Please select an ISO file first!")
            return
            
        extract_dir = filedialog.askdirectory(title="Select extraction destination folder")
        if not extract_dir:
            self.update_status("Extraction cancelled", 'warning')
            return
            
        # Run extraction in background thread
        Thread(target=self.perform_extraction, args=(self.iso_path.get(), extract_dir), daemon=True).start()

    def perform_extraction(self, iso_path, extract_dir):
        """Perform ISO extraction with progress updates"""
        try:
            self.update_status("Extracting ISO file... This may take several minutes", 'working', 10)
            
            result = subprocess.run([self._7z_path, "x", iso_path, f"-o{extract_dir}", "-y"],
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                self.update_status(f"Extraction failed: {result.stderr}", 'error', 0)
                return
                
            self.update_status("Searching for root filesystem...", 'working', 80)
            
            # Search for rootfs
            found = None
            for root_dir, _, files in os.walk(extract_dir):
                for f in files:
                    if (f.endswith(".squashfs") or f == "filesystem.squashfs" or 
                        f == "rootfs" or f == "filesystem.img"):
                        found = os.path.join(root_dir, f)
                        break
                if found:
                    break
                    
            if found:
                self.update_status(f"✅ Root filesystem found: {os.path.basename(found)}", 'success', 100)
            else:
                self.update_status("⚠️ Root filesystem not found in extracted files", 'warning', 100)
                
        except Exception as e:
            self.update_status(f"Extraction error: {str(e)}", 'error', 0)

    # VHD Methods
    def create_and_mount_vhd(self):
        """Create VHD with modern progress tracking"""
        vhd_path = filedialog.asksaveasfilename(
            title="Save VHD file as",
            defaultextension=".vhd",
            filetypes=[("VHD files", "*.vhd")]
        )
        if not vhd_path:
            return
            
        Thread(target=self.perform_vhd_creation, args=(vhd_path,), daemon=True).start()

    def perform_vhd_creation(self, vhd_path):
        """Create VHD in background with progress"""
        try:
            size_gb = self.vhd_size_gb.get()
            self.update_status(f"Creating {size_gb}GB VHD file...", 'working', 25)
            
            result = subprocess.run([self.qemu_path, "create", "-f", "vpc", vhd_path, f"{size_gb}G"],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.update_status(f"✅ VHD created successfully: {os.path.basename(vhd_path)}", 'success', 100)
                self.selected_vhd_path.set(f"📁 {vhd_path}")
            else:
                self.update_status(f"❌ VHD creation failed: {result.stderr}", 'error', 0)
                
        except Exception as e:
            self.update_status(f"❌ VHD creation error: {str(e)}", 'error', 0)

    def select_ext4_vhd(self):
        """Select existing VHD file"""
        vhd_path = filedialog.askopenfilename(
            title="Select ext4-formatted VHD file",
            filetypes=[("VHD files", "*.vhd"), ("All files", "*.*")]
        )
        if vhd_path:
            self.selected_vhd_path.set(f"📁 {vhd_path}")
            self.update_status(f"VHD selected: {os.path.basename(vhd_path)}", 'success')
        else:
            self.selected_vhd_path.set("No VHD selected")

    def format_vhd_ext4(self):
        """Format VHD as ext4"""
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
            
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_vhd_format, args=(vhd_path,), daemon=True).start()

    def perform_vhd_format(self, vhd_path):
        """Format VHD in background"""
        try:
            self.update_status("Formatting VHD as ext4...", 'working', 50)
            
            if self.is_windows:
                result = subprocess.run(["wsl", "--exec", "mkfs.ext4", vhd_path],
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(["mkfs.ext4", vhd_path],
                                      capture_output=True, text=True)
                                      
            if result.returncode == 0:
                self.update_status("✅ VHD formatted as ext4 successfully", 'success', 100)
            else:
                self.update_status(f"❌ Format failed: {result.stderr}", 'error', 0)
                
        except Exception as e:
            self.update_status(f"❌ Format error: {str(e)}", 'error', 0)

    def copy_rootfs_to_vhd(self):
        """Copy rootfs to VHD"""
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
            
        rootfs_path = filedialog.askopenfilename(title="Select extracted rootfs file")
        if not rootfs_path:
            return
            
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_rootfs_copy_vhd, args=(rootfs_path, vhd_path), daemon=True).start()

    def perform_rootfs_copy_vhd(self, rootfs_path, vhd_path):
        """Copy rootfs to VHD in background"""
        try:
            self.update_status("Copying root filesystem to VHD...", 'working', 25)
            
            mount_point = tempfile.mkdtemp()
            
            if self.is_windows:
                subprocess.run(["wsl", "--exec", "mount", "-t", "ext4", vhd_path, mount_point], check=True)
                subprocess.run(["wsl", "--exec", "cp", "-a", rootfs_path, mount_point], check=True)
                subprocess.run(["wsl", "--exec", "umount", mount_point], check=True)
            else:
                subprocess.run(["sudo", "mount", vhd_path, mount_point], check=True)
                subprocess.run(["sudo", "cp", "-a", rootfs_path, mount_point], check=True)
                subprocess.run(["sudo", "umount", mount_point], check=True)
                
            self.update_status("✅ Root filesystem copied to VHD successfully", 'success', 100)
            
        except Exception as e:
            self.update_status(f"❌ Copy failed: {str(e)}", 'error', 0)

    def install_grub(self):
        """Install GRUB to VHD"""
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
            
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_grub_install_vhd, args=(vhd_path,), daemon=True).start()

    def perform_grub_install_vhd(self, vhd_path):
        """Install GRUB to VHD in background"""
        try:
            self.update_status("Installing GRUB bootloader...", 'working', 50)
            
            if self.is_windows:
                result = subprocess.run(["wsl", "--exec", "grub-install", 
                                       "--target=i386-pc", "--boot-directory=/boot", vhd_path],
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(["sudo", "grub-install", vhd_path],
                                      capture_output=True, text=True)
                                      
            if result.returncode == 0:
                self.update_status("✅ GRUB installed successfully", 'success', 100)
            else:
                self.update_status(f"❌ GRUB installation failed: {result.stderr}", 'error', 0)
                
        except Exception as e:
            self.update_status(f"❌ GRUB installation error: {str(e)}", 'error', 0)

    def add_vhd_to_boot_menu(self):
        """Add VHD to Windows boot menu"""
        if not self.is_windows:
            self.show_error("Error", "This feature is only available on Windows!")
            return
            
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
            
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_boot_menu_add, args=(vhd_path,), daemon=True).start()

    def perform_boot_menu_add(self, vhd_path):
        """Add VHD to boot menu in background"""
        try:
            self.update_status("Adding VHD to Windows boot menu...", 'working', 25)
            
            # Create boot entry
            result = subprocess.run(["bcdedit", "/create", "/d", "Linux VHD", "/application", "osloader"],
                                  capture_output=True, text=True, check=True)
            
            match = re.search(r"\{[a-fA-F0-9\-]+\}", result.stdout)
            if not match:
                raise ValueError("Failed to parse GUID from bcdedit output")
                
            guid = match.group()
            self.update_status("Configuring boot entry...", 'working', 75)
            
            # Configure boot entry
            subprocess.run([
                "bcdedit", "/set", guid, "device", f"vhd=[locate]\\{vhd_path}",
                "osdevice", f"vhd=[locate]\\{vhd_path}",
                "path", "\\Windows\\system32\\winload.efi",
                "description", "Linux VHD",
                "locale", "en-US",
                "inherit", "{bootloadersettings}",
                "displayorder", guid, "/addlast"
            ], check=True)
            
            self.update_status("✅ VHD added to boot menu successfully", 'success', 100)
            self.show_success("Success", "VHD has been added to the Windows boot menu!\n\nRestart your computer to see the new boot option.")
            
        except Exception as e:
            self.update_status(f"❌ Boot menu addition failed: {str(e)}", 'error', 0)

    # Partition Methods
    def select_ext4_partition(self):
        """Select ext4 partition with modern dialog"""
        Thread(target=self.perform_partition_selection, daemon=True).start()

    def perform_partition_selection(self):
        """Get partition list and show selection dialog"""
        try:
            self.update_status("Scanning for ext4 partitions...", 'working', 50)
            
            if self.is_windows:
                result = subprocess.run(["wsl", "lsblk", "-o", "NAME,FSTYPE,MOUNTPOINT,SIZE"],
                                      capture_output=True, text=True, check=True)
                partitions = [line for line in result.stdout.split('\n') 
                            if 'ext4' in line and not 'SWAP' in line]
            else:
                result = subprocess.run(["lsblk", "-o", "NAME,FSTYPE,MOUNTPOINT,SIZE", "-J"],
                                      capture_output=True, text=True, check=True)
                devices = json.loads(result.stdout)
                partitions = []
                for device in devices['blockdevices']:
                    for part in device.get('children', []):
                        if part.get('fstype') == 'ext4' and not part.get('mountpoint'):
                            partitions.append(f"{part['name']} ({part.get('size', 'unknown')})")
            
            if not partitions:
                self.update_status("❌ No ext4 partitions found", 'error', 100)
                return
                
            # Show selection dialog on main thread
            self.root.after(0, self.show_partition_dialog, partitions)
            
        except Exception as e:
            self.update_status(f"❌ Partition scan failed: {str(e)}", 'error', 0)

    def show_partition_dialog(self, partitions):
        """Show partition selection dialog"""
        choice = simpledialog.askstring("Select Partition",
            "Available ext4 partitions:\n" + '\n'.join(partitions) +
            "\n\nEnter device name (e.g. sda3):")
        
        if choice:
            self.selected_partition.set(f"🗂️ Selected: /dev/{choice}")
            self.update_status(f"Partition selected: /dev/{choice}", 'success', 100)
        else:
            self.update_status("Partition selection cancelled", 'warning', 100)

    def refresh_partitions(self):
        """Refresh partition list"""
        self.update_status("Refreshing partition list...", 'working')
        self.selected_partition.set("No partition selected")
        time.sleep(1)  # Visual feedback
        self.update_status("Partition list refreshed", 'success')

    def copy_rootfs_to_partition(self):
        """Copy rootfs to selected partition"""
        if not self.selected_partition.get() or "No partition selected" in self.selected_partition.get():
            self.show_error("Error", "Please select an ext4 partition first!")
            return
            
        rootfs_path = filedialog.askopenfilename(title="Select extracted rootfs file")
        if not rootfs_path:
            return
            
        partition = self.get_selected_partition_device()
        Thread(target=self.perform_rootfs_copy_partition, args=(rootfs_path, partition), daemon=True).start()

    def perform_rootfs_copy_partition(self, rootfs_path, partition):
        """Copy rootfs to partition in background"""
        try:
            self.update_status(f"Copying root filesystem to {partition}...", 'working', 25)
            
            mount_point = "/tmp/linux_install_mount"
            
            if self.is_windows:
                subprocess.run(["wsl", "--exec", "sudo", "mkdir", "-p", mount_point], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "mount", partition, mount_point], check=True)
                
                if rootfs_path.endswith(".squashfs"):
                    subprocess.run(["wsl", "--exec", "sudo", "unsquashfs", "-f", "-d", mount_point, rootfs_path], check=True)
                else:
                    subprocess.run(["wsl", "--exec", "sudo", "cp", "-a", f"{rootfs_path}/*", mount_point], check=True)
                    
                subprocess.run(["wsl", "--exec", "sudo", "umount", mount_point], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "rmdir", mount_point], check=True)
            else:
                subprocess.run(["sudo", "mkdir", "-p", mount_point], check=True)
                subprocess.run(["sudo", "mount", partition, mount_point], check=True)
                
                if rootfs_path.endswith(".squashfs"):
                    subprocess.run(["sudo", "unsquashfs", "-f", "-d", mount_point, rootfs_path], check=True)
                else:
                    subprocess.run(["sudo", "cp", "-a", f"{rootfs_path}/*", mount_point], check=True)
                    
                subprocess.run(["sudo", "umount", mount_point], check=True)
                subprocess.run(["sudo", "rmdir", mount_point], check=True)
            
            self.update_status(f"✅ Root filesystem copied to {partition} successfully", 'success', 100)
            
        except Exception as e:
            self.update_status(f"❌ Copy to partition failed: {str(e)}", 'error', 0)

    def install_grub_to_partition(self):
        """Install GRUB to selected partition"""
        if not self.selected_partition.get() or "No partition selected" in self.selected_partition.get():
            self.show_error("Error", "Please select an ext4 partition first!")
            return
            
        partition = self.get_selected_partition_device()
        Thread(target=self.perform_grub_install_partition, args=(partition,), daemon=True).start()

    def perform_grub_install_partition(self, partition):
        """Install GRUB to partition in background"""
        try:
            self.update_status(f"Installing GRUB to {partition}...", 'working', 25)
            
            mount_point = "/tmp/linux_install_mount"
            disk_device = re.sub(r'\d+$', '', partition)
            
            if self.is_windows:
                subprocess.run(["wsl", "--exec", "sudo", "mkdir", "-p", mount_point], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "mount", partition, mount_point], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "grub-install", 
                              f"--root-directory={mount_point}", disk_device], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "umount", mount_point], check=True)
                subprocess.run(["wsl", "--exec", "sudo", "rmdir", mount_point], check=True)
            else:
                subprocess.run(["sudo", "mkdir", "-p", mount_point], check=True)
                subprocess.run(["sudo", "mount", partition, mount_point], check=True)
                subprocess.run(["sudo", "grub-install", f"--root-directory={mount_point}", disk_device], check=True)
                subprocess.run(["sudo", "umount", mount_point], check=True)
                subprocess.run(["sudo", "rmdir", mount_point], check=True)
            
            self.update_status(f"✅ GRUB installed to {partition} successfully", 'success', 100)
            
        except Exception as e:
            self.update_status(f"❌ GRUB installation to partition failed: {str(e)}", 'error', 0)

    def get_selected_partition_device(self):
        """Extract device path from selected partition"""
        if self.selected_partition.get():
            selected_text = self.selected_partition.get()
            if "Selected: " in selected_text:
                return selected_text.split("Selected: ")[1]
        return None

    # Advanced tab methods
    def check_dependencies(self):
        """Check system dependencies"""
        self.update_status("Checking dependencies...", 'working', 50)
        
        deps_status = []
        deps_status.append(f"✅ 7-Zip: {self._7z_path}" if os.path.exists(self._7z_path) else "❌ 7-Zip: Not found")
        deps_status.append(f"✅ QEMU: {self.qemu_path}" if os.path.exists(self.qemu_path) else "❌ QEMU: Not found")
        
        if self.is_windows:
            wsl_check = subprocess.run(["wsl", "--status"], capture_output=True, text=True)
            deps_status.append("✅ WSL: Available" if wsl_check.returncode == 0 else "❌ WSL: Not available")
        
        deps_status.append(f"✅ Admin Rights: Available" if self.is_admin() else "⚠️ Admin Rights: Limited")
        
        messagebox.showinfo("Dependency Check", "\n".join(deps_status))
        self.update_status("Dependency check completed", 'success', 100)

    def view_logs(self):
        """View application logs"""
        if os.path.exists("error.log"):
            try:
                with open("error.log", "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        messagebox.showinfo("Application Logs", content[-2000:])  # Show last 2000 chars
                    else:
                        messagebox.showinfo("Application Logs", "No errors logged.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read log file: {e}")
        else:
            messagebox.showinfo("Application Logs", "No log file found.")

    def show_about(self):
        """Show about dialog"""
        about_text = """
🐧 Modern Linux Installer v2.0.0

A professional Linux installation tool for Windows & Linux systems.

Features:
• Modern, intuitive user interface
• VHD-based Linux installations
• Direct partition installations
• Multi-distribution support
• Real-time progress tracking
• Cross-platform compatibility

Developed with ❤️ for the Linux community

GitHub: https://github.com/yourusername/modern-linux-installer
        """.strip()
        
        messagebox.showinfo("About Modern Linux Installer", about_text)

def show_fallback_error(msg: str):
    """Fallback error display when Tkinter fails"""
    try:
        ctypes.windll.user32.MessageBoxW(0, msg, "Modern Linux Installer Error", 0x10)
    except:
        print(f"Critical error: {msg}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ModernLinuxInstaller(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"An error occurred:\n{e}\n\n{traceback.format_exc()}"
        # Write error message to file as well
        try:
            with open("error.log", "w", encoding="utf-8") as f:
                f.write(error_msg)
        except:
            pass
        try:
            messagebox.showerror("Error", error_msg)
        except:
            show_fallback_error(error_msg)
