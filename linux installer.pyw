#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import subprocess
import platform
import sys
import re
import tempfile
import traceback
import json
from threading import Thread
import time
import shutil

class ModernLinuxInstaller:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_variables()
        self.setup_window()
        self.validate_dependencies()
        self.create_ui()

    def setup_variables(self):
        self.iso_path = tk.StringVar()
        self.vhd_size_gb = tk.IntVar(value=8)
        self.selected_vhd_path = tk.StringVar()
        self.selected_partition = tk.StringVar()
        self.status_text = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.vhd_fs_type = tk.StringVar(value="ext4")
        self.lang = tk.StringVar(value="en")
        self.LANGS = {
            'en': {
                'app_title': "🐧 Modern Linux Installer",
                'subtitle': "Professional Linux installation tool for Windows",
                'ready': "Ready to start installation",
                'select_iso': "Select Linux ISO File",
                'iso_selected': "ISO file selected successfully",
                'iso_cancel': "ISO selection cancelled",
                'extract_rootfs': "Extract Root Filesystem",
                'select_rootfs': "Select Existing RootFS Folder",
                'partition_scan': "Scanning for ext2/3/4 partitions...",
                'no_partition': "No ext2/3/4 partition found. Please ensure it is mounted with ext2fsd.",
                'partition_select': "Select Partition",
                'partition_selected': "Partition selected: {name}",
                'partition_cancel': "Partition selection cancelled",
                'copying_rootfs': "Copying root filesystem to {target}...",
                'copy_success': "Root filesystem copied to {target} successfully",
                'copy_error': "Copy to partition failed: {err}",
                'rootfs_folder_error': "RootFS must be a folder! Please extract squashfs and select the folder.",
                'vhd_format_warn': "VHD formatting is only supported in Linux or with external tools.",
                'grub_warn': "GRUB installation is only supported in Linux. Please perform this step in a Linux environment.",
                'refreshing': "Refreshing partition list...",
                'refreshed': "Partition list refreshed",
                'setup_tab': '📁 Setup & ISO',
                'vhd_tab': '💾 VHD Installation',
                'partition_tab': '🗂️ Partition Installation',
                'advanced_tab': '⚙️ Advanced',
                'iso_section': 'ISO File Selection',
                'iso_section_desc': 'Select your Linux distribution ISO file',
                'rootfs_section': 'Root Filesystem Extraction',
                'rootfs_section_desc': 'Extract the Linux root filesystem from ISO or select an existing one',
                'browse_iso': '🔍 Browse ISO File',
                'extract_btn': '📦 Extract Root Filesystem',
                'select_rootfs_btn': '📂 Select Existing RootFS',
                'vhd_section': 'VHD Creation & Management',
                'vhd_section_desc': 'Create and manage Virtual Hard Disk files',
                'vhd_size': 'VHD Size:',
                'filesystem': 'Filesystem:',
                'create_vhd': '🆕 Create VHD',
                'select_vhd': '📁 Select VHD',
                'format_vhd': '🔧 Format VHD',
                'copy_rootfs': '📋 Copy RootFS',
                'install_grub': '⚙️ Install GRUB',
                'add_boot': '🚀 Add to Boot Menu',
                'partition_section': 'Partition Installation',
                'partition_section_desc': 'Install directly to an existing ext2/3/4 partition',
                'select_partition': '🔍 Select ext2/3/4 Partition',
                'refresh': '🔄 Refresh',
                'copy_rootfs_partition': '📋 Copy RootFS to Partition',
                'install_grub_partition': '⚙️ Install GRUB to Partition',
                'system_info': 'System Information',
                'system_info_desc': 'Current system and dependency status',
                'tools_section': 'System Tools',
                'tools_section_desc': 'Additional utilities and diagnostics',
                'check_deps': '🔧 Check Dependencies',
                'view_logs': '📋 View Logs',
                'about': 'ℹ️ About',
                'lang_label': 'Language / Dil:',
            },
            'tr': {
                'app_title': "🐧 Modern Linux Installer",
                'subtitle': "Windows için profesyonel Linux kurulum aracı",
                'ready': "Kuruluma hazır",
                'select_iso': "Linux ISO Dosyasını Seç",
                'iso_selected': "ISO dosyası başarıyla seçildi",
                'iso_cancel': "ISO seçimi iptal edildi",
                'extract_rootfs': "RootFS'yi Çıkart",
                'select_rootfs': "Mevcut RootFS Klasörünü Seç",
                'partition_scan': "Ext2/3/4 bölümler taranıyor...",
                'no_partition': "Hiçbir ext2/3/4 bölümü bulunamadı. Lütfen ext2fsd ile mount ettiğinizden emin olun.",
                'partition_select': "Bölüm Seçimi",
                'partition_selected': "Bölüm seçildi: {name}",
                'partition_cancel': "Bölüm seçimi iptal edildi",
                'copying_rootfs': "RootFS {target} bölümüne kopyalanıyor...",
                'copy_success': "RootFS başarıyla {target} bölümüne kopyalandı",
                'copy_error': "Bölüme kopyalama hatası: {err}",
                'rootfs_folder_error': "RootFS bir klasör olmalı! squashfs dosyasını açıp klasör olarak seçin.",
                'vhd_format_warn': "VHD formatlama sadece Linux ortamında veya harici araçlarla yapılabilir.",
                'grub_warn': "GRUB kurulumu sadece Linux ortamında yapılabilir. Lütfen işlemi uygun bir Linux ortamında gerçekleştirin.",
                'refreshing': "Bölüm listesi yenileniyor...",
                'refreshed': "Bölüm listesi yenilendi",
                'setup_tab': '📁 Kurulum & ISO',
                'vhd_tab': '💾 VHD Kurulumu',
                'partition_tab': '🗂️ Bölüm Kurulumu',
                'advanced_tab': '⚙️ Gelişmiş',
                'iso_section': 'ISO Dosyası Seçimi',
                'iso_section_desc': 'Linux dağıtımınızın ISO dosyasını seçin',
                'rootfs_section': 'RootFS Çıkartma',
                'rootfs_section_desc': 'ISO’dan rootfs çıkartın veya mevcut bir klasörü seçin',
                'browse_iso': '🔍 ISO Dosyası Seç',
                'extract_btn': '📦 RootFS’yi Çıkart',
                'select_rootfs_btn': '📂 Mevcut RootFS Seç',
                'vhd_section': 'VHD Oluşturma & Yönetim',
                'vhd_section_desc': 'VHD dosyalarını oluşturun ve yönetin',
                'vhd_size': 'VHD Boyutu:',
                'filesystem': 'Dosya Sistemi:',
                'create_vhd': '🆕 VHD Oluştur',
                'select_vhd': '📁 VHD Seç',
                'format_vhd': '🔧 VHD Formatla',
                'copy_rootfs': '📋 RootFS Kopyala',
                'install_grub': '⚙️ GRUB Kur',
                'add_boot': '🚀 Boot Menüsüne Ekle',
                'partition_section': 'Bölüm Kurulumu',
                'partition_section_desc': 'Mevcut ext2/3/4 bölüme doğrudan kurulum',
                'select_partition': '🔍 ext2/3/4 Bölüm Seç',
                'refresh': '🔄 Yenile',
                'copy_rootfs_partition': '📋 RootFS’yi Bölüme Kopyala',
                'install_grub_partition': '⚙️ GRUB’u Bölüme Kur',
                'system_info': 'Sistem Bilgisi',
                'system_info_desc': 'Mevcut sistem ve bağımlılık durumu',
                'tools_section': 'Sistem Araçları',
                'tools_section_desc': 'Ek araçlar ve tanılamalar',
                'check_deps': '🔧 Bağımlılıkları Kontrol Et',
                'view_logs': '📋 Logları Görüntüle',
                'about': 'ℹ️ Hakkında',
                'lang_label': 'Dil / Language:',
            }
        }
        self.status_text.set(self.LANGS[self.lang.get()]['ready'])
        self.is_linux = platform.system().lower() == "linux"
        self.is_windows = platform.system().lower() == "windows"

    def setup_window(self):
        self.root.title(self.LANGS[self.lang.get()]['app_title'])
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        self.style = ttk.Style()
        self.style.theme_use('clam')
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
        self.configure_styles()

    def update_language(self):
        self.root.title(self.LANGS[self.lang.get()]['app_title'])
        self.status_text.set(self.LANGS[self.lang.get()]['ready'])
        self.notebook.tab(0, text=self.LANGS[self.lang.get()]['setup_tab'])
        self.notebook.tab(1, text=self.LANGS[self.lang.get()]['vhd_tab'])
        self.notebook.tab(2, text=self.LANGS[self.lang.get()]['partition_tab'])
        self.notebook.tab(3, text=self.LANGS[self.lang.get()]['advanced_tab'])
        self.title_label.config(text=self.LANGS[self.lang.get()]['app_title'])
        self.subtitle_label.config(text=self.LANGS[self.lang.get()]['subtitle'])
        # Diğer UI elemanlarını da burada güncelleyebilirsin

    def configure_styles(self):
        self.style.configure('Modern.TNotebook', background=self.colors['bg_primary'], borderwidth=0)
        self.style.configure('Modern.TNotebook.Tab', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], padding=[20, 10], borderwidth=0)
        self.style.map('Modern.TNotebook.Tab', background=[('selected', self.colors['accent']), ('active', self.colors['bg_tertiary'])])
        self.style.configure('Modern.TFrame', background=self.colors['bg_secondary'], borderwidth=1, relief='solid')
        self.style.configure('Title.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], font=('Segoe UI', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_secondary'], font=('Segoe UI', 10))
        self.style.configure('Status.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], font=('Segoe UI', 9))
        self.style.configure('Modern.TButton', background=self.colors['accent'], foreground=self.colors['text_primary'], borderwidth=0, focuscolor='none', font=('Segoe UI', 9))
        self.style.map('Modern.TButton', background=[('active', self.colors['accent_hover']), ('pressed', self.colors['accent_hover'])])
        self.style.configure('Modern.Horizontal.TProgressbar', background=self.colors['accent'], troughcolor=self.colors['bg_tertiary'], borderwidth=0, lightcolor=self.colors['accent'], darkcolor=self.colors['accent'])

    def validate_dependencies(self):
        self._7z_path = r"J:\portableapps\PortableApps\7-ZipPortable\App\7-Zip\7z.exe"
        self.qemu_path = r"D:\win\qemu\qemu-img.exe"
        if not os.path.exists(self._7z_path):
            found_7z = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.exists(os.path.join(path, "7z.exe")):
                    self._7z_path = os.path.join(path, "7z.exe")
                    found_7z = True
                    break
            if not found_7z:
                self.show_error("Missing Dependency", "7-Zip not found!\nPlease install 7-Zip or update the path in the script.")
                sys.exit(1)
        if not os.path.exists(self.qemu_path):
            found_qemu = False
            for path in os.environ["PATH"].split(os.pathsep):
                if os.path.exists(os.path.join(path, "qemu-img.exe")):
                    self.qemu_path = os.path.join(path, "qemu-img.exe")
                    found_qemu = True
                    break
            if not found_qemu:
                self.show_error("Missing Dependency", "QEMU not found!\nPlease install QEMU or update the path in the script.")
                sys.exit(1)

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.create_header(main_frame)
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, pady=(20, 0))
        self.create_setup_tab()
        self.create_vhd_tab()
        self.create_partition_tab()
        self.create_advanced_tab()
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        title_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        title_frame.pack(side='left')
        self.title_label = tk.Label(title_frame, text=self.LANGS[self.lang.get()]['app_title'], font=('Segoe UI', 24, 'bold'), fg=self.colors['text_primary'], bg=self.colors['bg_primary'])
        self.title_label.pack(anchor='w')
        self.subtitle_label = tk.Label(title_frame, text=self.LANGS[self.lang.get()]['subtitle'], font=('Segoe UI', 11), fg=self.colors['text_secondary'], bg=self.colors['bg_primary'])
        self.subtitle_label.pack(anchor='w')
        version_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        version_frame.pack(side='right')
        version_label = tk.Label(version_frame, text="v1.1.0", font=('Segoe UI', 10, 'bold'), fg=self.colors['accent'], bg=self.colors['bg_primary'])
        version_label.pack()
        platform_label = tk.Label(version_frame, text=f"Running on {platform.system()}", font=('Segoe UI', 9), fg=self.colors['text_secondary'], bg=self.colors['bg_primary'])
        platform_label.pack()
        # Language selector
        lang_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        lang_frame.pack(side='right', padx=10)
        lang_label = tk.Label(lang_frame, text=self.LANGS[self.lang.get()]['lang_label'], bg=self.colors['bg_primary'], fg=self.colors['text_secondary'])
        lang_label.pack(side='left')
        lang_menu = ttk.Combobox(lang_frame, textvariable=self.lang, values=["en", "tr"], state="readonly", width=5)
        lang_menu.pack(side='left')
        lang_menu.bind("<<ComboboxSelected>>", lambda e: self.update_language())

    def create_setup_tab(self):
        setup_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(setup_frame, text=self.LANGS[self.lang.get()]['setup_tab'])
        # ISO Section
        iso_section = self.create_section(setup_frame, self.LANGS[self.lang.get()]['iso_section'], self.LANGS[self.lang.get()]['iso_section_desc'])
        iso_display_frame = tk.Frame(iso_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        iso_display_frame.pack(fill='x', pady=(10, 5))
        iso_icon = tk.Label(iso_display_frame, text="💿", font=('Segoe UI', 16), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        iso_icon.pack(side='left', padx=10, pady=10)
        iso_path_label = tk.Label(iso_display_frame, textvariable=self.iso_path, font=('Segoe UI', 10), wraplength=600, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], justify='left')
        iso_path_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)
        browse_btn = self.create_modern_button(iso_section, self.LANGS[self.lang.get()]['browse_iso'], self.browse_iso)
        browse_btn.pack(pady=5)
        self.distro_info_frame = tk.Frame(iso_section, bg=self.colors['bg_secondary'])
        self.distro_info_frame.pack(fill='x', pady=10)
        # RootFS Section
        extract_section = self.create_section(setup_frame, self.LANGS[self.lang.get()]['rootfs_section'], self.LANGS[self.lang.get()]['rootfs_section_desc'])
        extract_btn = self.create_modern_button(extract_section, self.LANGS[self.lang.get()]['extract_btn'], self.extract_rootfs)
        extract_btn.pack(pady=5)
        select_rootfs_btn = self.create_modern_button(extract_section, self.LANGS[self.lang.get()]['select_rootfs_btn'], self.select_existing_rootfs)
        select_rootfs_btn.pack(pady=5)
        rootfs_display_frame = tk.Frame(extract_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        rootfs_display_frame.pack(fill='x', pady=5)
        rootfs_icon = tk.Label(rootfs_display_frame, text="🗄️", font=('Segoe UI', 16), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        rootfs_icon.pack(side='left', padx=10, pady=10)
        self.selected_rootfs_path = tk.StringVar()
        rootfs_path_label = tk.Label(rootfs_display_frame, textvariable=self.selected_rootfs_path, font=('Segoe UI', 10), wraplength=600, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], justify='left')
        rootfs_path_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)

    def create_vhd_tab(self):
        vhd_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(vhd_frame, text=self.LANGS[self.lang.get()]['vhd_tab'])
        vhd_section = self.create_section(vhd_frame, self.LANGS[self.lang.get()]['vhd_section'], self.LANGS[self.lang.get()]['vhd_section_desc'])

        # VHD boyutu seçici
        size_frame = tk.Frame(vhd_section, bg=self.colors['bg_secondary'])
        size_frame.pack(fill='x', pady=10)
        tk.Label(size_frame, text=self.LANGS[self.lang.get()]['vhd_size'], font=('Segoe UI', 10, 'bold'), bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side='left')
        size_scale = tk.Scale(size_frame, from_=2, to=100, orient='horizontal', variable=self.vhd_size_gb, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], highlightthickness=0, troughcolor=self.colors['bg_primary'])
        size_scale.pack(side='left', padx=10, fill='x', expand=True)
        size_label = tk.Label(size_frame, textvariable=self.vhd_size_gb, font=('Segoe UI', 10, 'bold'), bg=self.colors['bg_secondary'], fg=self.colors['accent'])
        size_label.pack(side='right')
        tk.Label(size_frame, text="GB", font=('Segoe UI', 10), bg=self.colors['bg_secondary'], fg=self.colors['text_primary']).pack(side='right')

        # VHD oluşturma butonu
        self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['create_vhd'], self.create_and_mount_vhd).pack(fill='x', pady=5)

        # Seçili VHD gösterimi
        vhd_display_frame = tk.Frame(vhd_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        vhd_display_frame.pack(fill='x', pady=10)
        vhd_icon = tk.Label(vhd_display_frame, text="💾", font=('Segoe UI', 16), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        vhd_icon.pack(side='left', padx=10, pady=10)
        vhd_path_label = tk.Label(vhd_display_frame, textvariable=self.selected_vhd_path, font=('Segoe UI', 10), wraplength=600, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        vhd_path_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)

        # Platforma göre format/kopyala/GRUB/BCD butonları
        if self.is_windows:
            format_warn = tk.Label(vhd_section, text=self.LANGS[self.lang.get()]['vhd_format_warn'], font=('Segoe UI', 9, 'italic'), bg=self.colors['bg_secondary'], fg=self.colors['warning'])
            format_warn.pack(pady=5)
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['select_rootfs_btn'], self.select_existing_rootfs).pack(fill='x', pady=5)
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['copy_rootfs'], self.copy_rootfs_to_vhd).pack(fill='x', pady=5)
            grub_warn = tk.Label(vhd_section, text=self.LANGS[self.lang.get()]['grub_warn'], font=('Segoe UI', 9, 'italic'), bg=self.colors['bg_secondary'], fg=self.colors['warning'])
            grub_warn.pack(pady=5)
            self.create_modern_button(vhd_section, "BCD'ye Ekle" if self.lang.get() == "tr" else "Add to BCD", self.add_vhd_to_boot_menu).pack(fill='x', pady=5)
        else:
            # Linux: Otomatik formatla, mount et, kopyala, GRUB kur
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['select_rootfs_btn'], self.select_existing_rootfs).pack(fill='x', pady=5)
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['format_vhd'], self.format_vhd_multi_fs).pack(fill='x', pady=5)
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['copy_rootfs'], self.copy_rootfs_to_vhd).pack(fill='x', pady=5)
            self.create_modern_button(vhd_section, self.LANGS[self.lang.get()]['install_grub'], self.install_grub).pack(fill='x', pady=5)

    def create_partition_tab(self):
        partition_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(partition_frame, text=self.LANGS[self.lang.get()]['partition_tab'])
        partition_section = self.create_section(partition_frame, self.LANGS[self.lang.get()]['partition_section'], self.LANGS[self.lang.get()]['partition_section_desc'])

        # Partition seçimi ve yenile
        select_frame = tk.Frame(partition_section, bg=self.colors['bg_secondary'])
        select_frame.pack(fill='x', pady=10)
        self.create_modern_button(select_frame, self.LANGS[self.lang.get()]['select_partition'], self.select_ext4_partition).pack(side='left')
        self.create_modern_button(select_frame, self.LANGS[self.lang.get()]['refresh'], self.refresh_partitions).pack(side='right')

        # Seçili partition gösterimi
        partition_display_frame = tk.Frame(partition_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        partition_display_frame.pack(fill='x', pady=10)
        partition_icon = tk.Label(partition_display_frame, text="🗂️", font=('Segoe UI', 16), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        partition_icon.pack(side='left', padx=10, pady=10)
        partition_label = tk.Label(partition_display_frame, textvariable=self.selected_partition, font=('Segoe UI', 10), wraplength=600, bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        partition_label.pack(side='left', padx=(0, 10), pady=10, fill='x', expand=True)

        # RootFS kopyalama
        self.create_modern_button(partition_section, self.LANGS[self.lang.get()]['copy_rootfs_partition'], self.copy_rootfs_to_partition).pack(fill='x', pady=5)
        # GRUB kurulumu uyarısı
        grub_warn = tk.Label(partition_section, text=self.LANGS[self.lang.get()]['grub_warn'], font=('Segoe UI', 9, 'italic'), bg=self.colors['bg_secondary'], fg=self.colors['warning'])
        grub_warn.pack(pady=5)
        # (İstersen GRUB butonu da ekleyebilirsin)

        # BCD'ye ekle butonu (sadece Windows'ta göster)
        if self.is_windows:
            self.create_modern_button(partition_section, "BCD'ye Ekle" if self.lang.get() == "tr" else "Add to BCD", self.add_partition_to_boot_menu).pack(fill='x', pady=5)

    def create_advanced_tab(self):
        advanced_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(advanced_frame, text=self.LANGS[self.lang.get()]['advanced_tab'])
        sys_section = self.create_section(advanced_frame, self.LANGS[self.lang.get()]['system_info'], self.LANGS[self.lang.get()]['system_info_desc'])
        info_frame = tk.Frame(sys_section, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
        info_frame.pack(fill='x', pady=10)
        info_text = f"""
🖥️ OS: {platform.system()} {platform.release()}
🏗️ Arch: {platform.machine()}
🐍 Python: {platform.python_version()}
📁 7-Zip: {self._7z_path}
💿 QEMU: {self.qemu_path}
        """.strip()
        info_label = tk.Label(info_frame, text=info_text, font=('Consolas', 9), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'], justify='left')
        info_label.pack(padx=20, pady=15)
        tools_section = self.create_section(advanced_frame, self.LANGS[self.lang.get()]['tools_section'], self.LANGS[self.lang.get()]['tools_section_desc'])
        tools_frame = tk.Frame(tools_section, bg=self.colors['bg_secondary'])
        tools_frame.pack(fill='x', pady=10)
        self.create_modern_button(tools_frame, self.LANGS[self.lang.get()]['check_deps'], self.check_dependencies).pack(side='left', padx=5)
        self.create_modern_button(tools_frame, self.LANGS[self.lang.get()]['view_logs'], self.view_logs).pack(side='left', padx=5)
        self.create_modern_button(tools_frame, self.LANGS[self.lang.get()]['about'], self.show_about).pack(side='right', padx=5)

    def create_advanced_tab(self):
        advanced_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(advanced_frame, text=self.LANGS[self.lang.get()]['advanced_tab'])
        sys_section = self.create_section(advanced_frame, self.LANGS[self.lang.get()]['system_info'], self.LANGS[self.lang.get()]['system_info_desc'])
        # (Buraya sistem bilgisi ve araçlar için arayüz ekleyebilirsin)

    # ...
    # (Diğer sekme fonksiyonlarını ve core fonksiyonları da aynı şekilde güncellemelisin)
    # ...

    def create_section(self, parent, title, description):
        section_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        section_frame.pack(fill='x', padx=20, pady=10)
        header_frame = tk.Frame(section_frame, bg=self.colors['bg_tertiary'])
        header_frame.pack(fill='x')
        title_label = tk.Label(header_frame, text=title, font=('Segoe UI', 12, 'bold'), bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'])
        title_label.pack(side='left', padx=15, pady=10)
        desc_label = tk.Label(header_frame, text=description, font=('Segoe UI', 9), bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'])
        desc_label.pack(side='right', padx=15, pady=10)
        content_frame = tk.Frame(section_frame, bg=self.colors['bg_secondary'])
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        return content_frame

    def create_modern_button(self, parent, text, command, style='primary'):
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
        button = tk.Button(parent, text=text, command=command, bg=bg_color, fg=self.colors['text_primary'], font=('Segoe UI', 9, 'bold'), relief='flat', borderwidth=0, cursor='hand2')
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=bg_color)
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        return button

    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='solid', bd=1)
        status_frame.pack(fill='x', pady=(20, 0))
        status_content = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        status_content.pack(side='left', fill='x', expand=True)
        self.status_icon = tk.Label(status_content, text="✅", font=('Segoe UI', 12), bg=self.colors['bg_secondary'], fg=self.colors['success'])
        self.status_icon.pack(side='left', padx=10, pady=8)
        self.status_label = tk.Label(status_content, textvariable=self.status_text, font=('Segoe UI', 10), bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        self.status_label.pack(side='left', pady=8)
        self.progress_bar = ttk.Progressbar(status_frame, style='Modern.Horizontal.TProgressbar', variable=self.progress_var, length=200)
        self.progress_bar.pack(side='right', padx=10, pady=8)

    def update_status(self, message, status_type='info', progress=None):
        icons = {'info': '💡', 'success': '✅', 'warning': '⚠️', 'error': '❌', 'working': '⚙️'}
        colors = {'info': self.colors['text_primary'], 'success': self.colors['success'], 'warning': self.colors['warning'], 'error': self.colors['error'], 'working': self.colors['accent']}
        self.status_text.set(message)
        self.status_icon.config(text=icons.get(status_type, '💡'), fg=colors.get(status_type, self.colors['text_primary']))
        if progress is not None:
            self.progress_var.set(progress)
        self.root.update()

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        messagebox.showinfo(title, message)

    def select_ext4_partition(self):
        Thread(target=self.perform_partition_selection, daemon=True).start()

    def perform_partition_selection(self):
        try:
            self.update_status(self.LANGS[self.lang.get()]['partition_scan'], 'working', 50)
            linux_fs_types = ["ext2", "ext3", "ext4"]
            partitions = []
            if self.is_windows:
                try:
                    win_result = subprocess.run(
                        ["wmic", "logicaldisk", "get", "name,description,filesystem,size"],
                        capture_output=True, text=True
                    )
                    lines = win_result.stdout.strip().split("\n")
                    header = lines[0]
                    for l in lines[1:]:
                        l = l.strip()
                        if not l or l.startswith("Name"):
                            continue
                        parts = l.split()
                        if len(parts) >= 3:
                            desc = parts[0]
                            fs = parts[1].lower()
                            name = parts[2]
                            size = parts[3] if len(parts) > 3 else "?"
                            if fs in linux_fs_types:
                                partitions.append(f"{name} (ext2fsd: {desc}, {fs}, {size})")
                except Exception:
                    self.update_status("❌ Partition scan failed: ext2fsd veya WMIC ile diskler listelenemedi.", 'error', 100)
                    return
            else:
                self.update_status("❌ Bu özellik sadece Windows ortamında ve ext2fsd ile kullanılabilir.", 'error', 100)
                return
            if not partitions:
                self.update_status(self.LANGS[self.lang.get()]['no_partition'], 'error', 100)
                return
            self.root.after(0, self.show_partition_dialog, partitions)
        except Exception as e:
            self.update_status(f"❌ Partition scan failed: {str(e)}", 'error', 0)

    def show_partition_dialog(self, partitions):
        choice = simpledialog.askstring(self.LANGS[self.lang.get()]['partition_select'],
            self.LANGS[self.lang.get()]['partition_select'] + ":\n" + '\n'.join(partitions) +
            "\n\nEnter drive letter (e.g. E:)")
        if choice:
            self.selected_partition.set(f"🗂️ {choice}")
            self.update_status(self.LANGS[self.lang.get()]['partition_selected'].format(name=choice), 'success', 100)
        else:
            self.update_status(self.LANGS[self.lang.get()]['partition_cancel'], 'warning', 100)

    def refresh_partitions(self):
        self.update_status(self.LANGS[self.lang.get()]['refreshing'], 'working')
        self.selected_partition.set("")
        time.sleep(1)
        self.update_status(self.LANGS[self.lang.get()]['refreshed'], 'success')

    def copy_rootfs_to_partition(self):
        if not self.selected_partition.get():
            self.show_error("Error", self.LANGS[self.lang.get()]['partition_select'])
            return
        rootfs_path = self.selected_rootfs_path.get()
        if not rootfs_path:
            self.show_error("Error", self.LANGS[self.lang.get()]['select_rootfs'])
            return
        partition = self.selected_partition.get().replace("🗂️ ", "").strip()
        Thread(target=self.perform_rootfs_copy_partition, args=(rootfs_path, partition), daemon=True).start()

    def perform_rootfs_copy_partition(self, rootfs_path, partition):
        try:
            self.update_status(self.LANGS[self.lang.get()]['copying_rootfs'].format(target=partition), 'working', 25)
            if os.path.isdir(rootfs_path):
                for item in os.listdir(rootfs_path):
                    s = os.path.join(rootfs_path, item)
                    d = os.path.join(partition, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
            else:
                self.update_status(self.LANGS[self.lang.get()]['rootfs_folder_error'], 'error', 0)
                return
            self.update_status(self.LANGS[self.lang.get()]['copy_success'].format(target=partition), 'success', 100)
        except Exception as e:
            self.update_status(self.LANGS[self.lang.get()]['copy_error'].format(err=str(e)), 'error', 0)

    def add_partition_to_boot_menu(self):
        if not self.is_windows:
            self.show_error("Error", "This feature is only available on Windows!")
            return
        if not self.selected_partition.get():
            self.show_error("Error", "Please select a partition first!")
            return
        partition = self.selected_partition.get().replace("🗂️ ", "").strip()
        Thread(target=self.perform_partition_boot_menu_add, args=(partition,), daemon=True).start()

    def perform_partition_boot_menu_add(self, partition):
        try:
            self.update_status("Adding partition to Windows boot menu...", 'working', 25)
            result = subprocess.run(["bcdedit", "/create", "/d", "Linux Partition", "/application", "osloader"], capture_output=True, text=True, check=True)
            match = re.search(r"\{[a-fA-F0-9\-]+\}", result.stdout)
            if not match:
                raise ValueError("Failed to parse GUID from bcdedit output")
            guid = match.group()
            self.update_status("Configuring boot entry...", 'working', 75)
            subprocess.run([
                "bcdedit", "/set", guid, "device", partition,
                "osdevice", partition,
                "path", "\\Windows\\system32\\winload.efi",
                "description", "Linux Partition",
                "locale", "en-US",
                "inherit", "{bootloadersettings}",
                "displayorder", guid, "/addlast"
            ], check=True)
            self.update_status("✅ Partition added to boot menu successfully", 'success', 100)
            self.show_success("Success", "Partition has been added to the Windows boot menu!\n\nRestart your computer to see the new boot option.")
        except Exception as e:
            self.update_status(f"❌ Boot menu addition failed: {str(e)}", 'error', 0)

    def create_and_mount_vhd(self):
        vhd_path = filedialog.asksaveasfilename(
            title="Save VHD file as",
            defaultextension=".vhd",
            filetypes=[("VHD files", "*.vhd")]
        )
        if not vhd_path:
            return
        Thread(target=self.perform_vhd_creation, args=(vhd_path,), daemon=True).start()

    def perform_vhd_creation(self, vhd_path):
        try:
            size_gb = self.vhd_size_gb.get()
            self.update_status(f"Creating {size_gb}GB VHD file...", 'working', 25)
            result = subprocess.run([self.qemu_path, "create", "-f", "vpc", vhd_path, f"{size_gb}G"], capture_output=True, text=True)
            if result.returncode == 0:
                self.update_status(f"✅ VHD created successfully: {os.path.basename(vhd_path)}", 'success', 100)
                self.selected_vhd_path.set(f"📁 {vhd_path}")
            else:
                self.update_status(f"❌ VHD creation failed: {result.stderr}", 'error', 0)
        except Exception as e:
            self.update_status(f"❌ VHD creation error: {str(e)}", 'error', 0)

    def copy_rootfs_to_vhd(self):
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
        rootfs_path = self.selected_rootfs_path.get()
        if not rootfs_path:
            self.show_error("Error", "Please select a RootFS folder first!")
            return
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_rootfs_copy_vhd, args=(rootfs_path, vhd_path), daemon=True).start()

    def perform_rootfs_copy_vhd(self, rootfs_path, vhd_path):
        self.update_status("VHD'ye rootfs kopyalama işlemi sadece Linux ortamında yapılabilir. Lütfen işlemi uygun bir Linux ortamında gerçekleştirin.", 'warning', 0)
        return

    def add_vhd_to_boot_menu(self):
        if not self.is_windows:
            self.show_error("Error", "This feature is only available on Windows!")
            return
        if not self.selected_vhd_path.get() or "No VHD selected" in self.selected_vhd_path.get():
            self.show_error("Error", "Please select a VHD file first!")
            return
        vhd_path = self.selected_vhd_path.get().replace("📁 ", "")
        Thread(target=self.perform_boot_menu_add, args=(vhd_path,), daemon=True).start()

    def perform_boot_menu_add(self, vhd_path):
        try:
            self.update_status("Adding VHD to Windows boot menu...", 'working', 25)
            result = subprocess.run(["bcdedit", "/create", "/d", "Linux VHD", "/application", "osloader"], capture_output=True, text=True, check=True)
            match = re.search(r"\{[a-fA-F0-9\-]+\}", result.stdout)
            if not match:
                raise ValueError("Failed to parse GUID from bcdedit output")
            guid = match.group()
            self.update_status("Configuring boot entry...", 'working', 75)
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

    def browse_iso(self):
        self.update_status(self.LANGS[self.lang.get()]['select_iso'], 'working')
        file_path = filedialog.askopenfilename(
            title=self.LANGS[self.lang.get()]['select_iso'],
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        if file_path:
            self.iso_path.set(file_path)
            self.update_status(self.LANGS[self.lang.get()]['iso_selected'], 'success')
            Thread(target=self.detect_and_display_distro, args=(file_path,), daemon=True).start()
        else:
            self.iso_path.set("")
            self.update_status(self.LANGS[self.lang.get()]['iso_cancel'], 'warning')

    def extract_rootfs(self):
        if not self.iso_path.get():
            self.show_error("Error", self.LANGS[self.lang.get()]['select_iso'])
            return
        extract_dir = filedialog.askdirectory(title=self.LANGS[self.lang.get()]['extract_rootfs'])
        if not extract_dir:
            self.update_status(self.LANGS[self.lang.get()]['iso_cancel'], 'warning')
            return
        Thread(target=self.perform_extraction, args=(self.iso_path.get(), extract_dir), daemon=True).start()

    def perform_extraction(self, iso_path, extract_dir):
        try:
            self.update_status(self.LANGS[self.lang.get()]['extract_rootfs'] + "...", 'working', 10)
            result = subprocess.run([self._7z_path, "x", iso_path, f"-o{extract_dir}", "-y"], capture_output=True, text=True)
            if result.returncode != 0:
                self.update_status(f"Extraction failed: {result.stderr}", 'error', 0)
                return
            self.update_status("Searching for root filesystem...", 'working', 80)
            found = None
            rootfs_patterns = [
                ".squashfs", ".img", ".xfs", ".btrfs", ".cpio", ".lz4", ".zst", ".gz", ".lzma", ".ext2", ".ext3", ".ext4", ".linuxfs"
            ]
            rootfs_names = [
                "filesystem.squashfs", "filesystem.img", "rootfs", "rootfs.img", "linuxfs", "rootfs.xfs", "rootfs.btrfs"
            ]
            for root_dir, _, files in os.walk(extract_dir):
                for f in files:
                    if any(f.endswith(ext) for ext in rootfs_patterns) or f in rootfs_names:
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

    def detect_and_display_distro(self, iso_path):
        self.update_status("Analyzing ISO file...", 'working', 25)
        distro = self.detect_iso_base(iso_path)
        for widget in self.distro_info_frame.winfo_children():
            widget.destroy()
        if distro:
            info_frame = tk.Frame(self.distro_info_frame, bg=self.colors['bg_tertiary'], relief='solid', bd=1)
            info_frame.pack(fill='x', pady=5)
            distro_icon = tk.Label(info_frame, text="🐧", font=('Segoe UI', 16), bg=self.colors['bg_tertiary'], fg=self.colors['success'])
            distro_icon.pack(side='left', padx=10, pady=8)
            distro_label = tk.Label(info_frame, text=f"Detected: {distro}", font=('Segoe UI', 10, 'bold'), bg=self.colors['bg_tertiary'], fg=self.colors['success'])
            distro_label.pack(side='left', padx=(0, 10), pady=8)
            self.update_status(f"Detected distribution: {distro}", 'success', 100)
        else:
            self.update_status("Could not detect distribution type", 'warning', 100)

    def detect_iso_base(self, iso_path: str):
        try:
            result = subprocess.run([self._7z_path, "l", iso_path], capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return None
            output = result.stdout.lower()
            if "linuxfs" in output:
                if "antix" in output:
                    return "antiX Linux"
                elif "mx" in output:
                    return "MX Linux"
                elif "puppy" in output:
                    return "Puppy Linux"
                else:
                    return "Unknown linuxfs-based distro"
            if "antix" in output or "antiX" in output:
                return "antiX Linux"
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

    def select_existing_rootfs(self):
        folder_path = filedialog.askdirectory(title=self.LANGS[self.lang.get()]['select_rootfs'])
        if folder_path:
            self.selected_rootfs_path.set(folder_path)
            self.update_status(f"{self.LANGS[self.lang.get()]['select_rootfs']}: {os.path.basename(folder_path)}", 'success')
        else:
            self.update_status(self.LANGS[self.lang.get()]['partition_cancel'], 'warning')

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ModernLinuxInstaller(root)
        root.mainloop()
    except Exception as e:
        import traceback
        error_msg = f"An error occurred:\n{e}\n\n{traceback.format_exc()}"
        try:
            with open("error.log", "w", encoding="utf-8") as f:
                f.write(error_msg)
        except:
            pass
        try:
            messagebox.showerror("Error", error_msg)
        except:
            print(error_msg)
