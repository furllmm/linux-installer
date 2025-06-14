#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import ctypes
import platform

class LinuxInstallerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Custom Linux Installer")
        self.root.geometry("500x250")
        self.iso_path = tk.StringVar()
        self.vhd_size_gb = tk.IntVar(value=4)

        # Platform info
        self.is_linux = platform.system().lower() == "linux"
        self.is_windows = platform.system().lower() == "windows"

        tk.Label(root, text="Step 1: Select a Linux ISO file", font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Browse ISO", command=self.browse_iso).pack(pady=5)
        tk.Label(root, textvariable=self.iso_path, wraplength=480, fg="blue").pack(pady=5)

        tk.Button(root, text="Extract Root Filesystem", command=self.extract_rootfs).pack(pady=10)
        if self.is_windows:
            tk.Button(root, text="Create and Mount VHD (Windows)", command=self.create_and_mount_vhd).pack(pady=10)
            tk.Button(root, text="Format VHD as ext4 (WSL)", command=self.format_vhd_ext4).pack(pady=10)
            tk.Button(root, text="Copy RootFS to VHD (WSL)", command=self.copy_rootfs_to_vhd).pack(pady=10)
            tk.Button(root, text="Install GRUB Bootloader (WSL)", command=self.install_grub).pack(pady=10)
            tk.Button(root, text="Add VHD to Windows Boot Menu", command=self.add_vhd_to_boot_menu).pack(pady=10)
        elif self.is_linux:
            tk.Button(root, text="Create and Mount VHD (Linux)", command=self.create_and_mount_vhd_linux).pack(pady=10)
            tk.Button(root, text="Format VHD as ext4 (Linux)", command=self.format_vhd_ext4_linux).pack(pady=10)
            tk.Button(root, text="Copy RootFS to VHD (Linux)", command=self.copy_rootfs_to_vhd_linux).pack(pady=10)
            tk.Button(root, text="Install GRUB Bootloader (Linux)", command=self.install_grub_linux).pack(pady=10)
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=5)

        tk.Label(root, text="VHD Size (GB):").pack(pady=2)
        tk.Scale(root, from_=2, to=2000, orient=tk.HORIZONTAL, variable=self.vhd_size_gb).pack(pady=2)

        # Yönetici uyarısı (sadece Windows)
        if self.is_windows and not self.is_admin():
            messagebox.showwarning("Yönetici Yetkisi Gerekli", "Bu programı yönetici olarak çalıştırmalısınız! Disk işlemleri ve boot menüsü için yönetici izni gereklidir.")

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def browse_iso(self):
        file_path = filedialog.askopenfilename(
            title="Select Linux ISO",
            filetypes=[("ISO files", "*.iso"), ("All files", "*.*")]
        )
        if file_path:
            self.iso_path.set(file_path)
            # Otomatik taban algılama
            base = self.detect_iso_base(file_path)
            if base:
                self.status_label.config(text=f"Algılanan taban: {base}", fg="blue")
            else:
                self.status_label.config(text="Taban algılanamadı.", fg="orange")
        else:
            self.iso_path.set("")

    def detect_iso_base(self, iso_path: str) -> str | None:
        # 7z ile ISO içeriğini listele, tipik dosya/desenlere bak
        try:
            result = subprocess.run([
                "7z", "l", iso_path
            ], capture_output=True, text=True)
            if result.returncode != 0:
                return None
            output = result.stdout.lower()
            if "casper" in output or "filesystem.squashfs" in output:
                return "Ubuntu/Debian (casper)"
            if "live" in output and "slax" in output:
                return "Slax/Slackware tabanlı"
            if "archiso" in output or "airootfs" in output:
                return "Arch tabanlı"
            if "manjaro" in output:
                return "Manjaro (Arch tabanlı)"
            if "fedora" in output or "squashfs.img" in output:
                return "Fedora tabanlı"
            if "initrd.gz" in output and "vmlinuz" in output and "rootfs.gz" in output:
                return "TinyCore/Puppy Linux"
            if "boot/grub" in output:
                return "GRUB tabanlı (genel)"
        except Exception:
            return None
        return None

    def extract_rootfs(self):
        iso = self.iso_path.get()
        if not iso:
            self.status_label.config(text="Please select an ISO file first.", fg="red")
            return
        extract_dir = filedialog.askdirectory(title="Select folder to extract ISO contents")
        if not extract_dir:
            self.status_label.config(text="Extraction cancelled.", fg="red")
            return
        self.status_label.config(text="Extracting ISO... (this may take a while)", fg="orange")
        self.root.update()
        # Use 7z to extract ISO
        try:
            result = subprocess.run([
                "7z", "x", iso, f"-o{extract_dir}", "-y"
            ], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"7-Zip extraction failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"Extraction error: {e}", fg="red")
            return
        # Search for squashfs or casper/rootfs
        found = None
        for root, dirs, files in os.walk(extract_dir):
            for f in files:
                if f.endswith(".squashfs") or f == "filesystem.squashfs" or f == "rootfs" or f == "filesystem.img":
                    found = os.path.join(root, f)
                    break
            if found:
                break
        if found:
            self.status_label.config(text=f"Found rootfs: {found}", fg="green")
        else:
            self.status_label.config(text="Root filesystem not found in extracted ISO.", fg="red")

    def create_and_mount_vhd(self):
        vhd_path = filedialog.asksaveasfilename(
            title="Save VHD file as",
            defaultextension=".vhd",
            filetypes=[("VHD files", "*.vhd")]
        )
        if not vhd_path:
            self.status_label.config(text="VHD creation cancelled.", fg="red")
            return
        size_gb = self.vhd_size_gb.get()
        self.status_label.config(text=f"Creating {size_gb}GB VHD...", fg="orange")
        self.root.update()
        # PowerShell command to create VHD (mount işlemi WSL ile yapılacak)
        ps_script = f"""
        $vhdPath = '{vhd_path}'
        New-VHD -Path $vhdPath -SizeBytes {size_gb}GB -Dynamic | Out-Null
        """
        try:
            result = subprocess.run([
                "powershell", "-Command", ps_script
            ], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"VHD creation failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"VHD error: {e}", fg="red")
            return
        # WSL ile mount
        try:
            result = subprocess.run([
                "wsl", "--mount", vhd_path, "--bare"], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"WSL mount failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"WSL mount error: {e}", fg="red")
            return
        self.status_label.config(text=f"VHD created and mounted: {vhd_path}", fg="green")

    def format_vhd_ext4(self):
        self.status_label.config(text="VHD aygıtı bulunuyor...", fg="orange")
        self.root.update()
        # lsblk ile device path bul
        try:
            result = subprocess.run(["wsl", "lsblk", "-o", "NAME,SIZE,TYPE,MOUNTPOINT"], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            dev_path = None
            for line in lines:
                if "disk" in line and "vhd" in line:
                    dev_name = line.split()[0]
                    dev_path = f"/dev/{dev_name}"
                    break
            if not dev_path:
                self.status_label.config(text="VHD aygıtı bulunamadı.", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"lsblk error: {e}", fg="red")
            return
        self.status_label.config(text=f"VHD aygıtı: {dev_path}, ext4 formatlanıyor...", fg="orange")
        self.root.update()
        try:
            result = subprocess.run(["wsl", "sudo", "mkfs.ext4", dev_path], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"WSL format failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"WSL error: {e}", fg="red")
            return
        self.status_label.config(text=f"VHD ext4 olarak formatlandı: {dev_path}", fg="green")

    def copy_rootfs_to_vhd(self):
        # Ask for rootfs and mount point
        rootfs_path = filedialog.askopenfilename(title="Select extracted rootfs (squashfs/rootfs/img)")
        if not rootfs_path:
            self.status_label.config(text="Rootfs copy cancelled.", fg="red")
            return
        mount_point = filedialog.askdirectory(title="Select empty folder for VHD mount (must exist)")
        if not mount_point:
            self.status_label.config(text="VHD mount cancelled.", fg="red")
            return
        self.status_label.config(text="Mounting VHD in WSL...", fg="orange")
        self.root.update()
        # Find VHD device
        ps_script = """
        $vhd = Get-VHD | Where-Object { $_.Attached -eq $true } | Sort-Object -Property Path -Descending | Select-Object -First 1
        $disk = Get-Disk | Where-Object { $_.Location -like ('*' + $vhd.Path + '*') }
        $disk.Number
        """
        try:
            result = subprocess.run([
                "powershell", "-Command", ps_script
            ], capture_output=True, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                self.status_label.config(text="Could not find attached VHD disk.", fg="red")
                return
            disk_number = result.stdout.strip()
        except Exception as e:
            self.status_label.config(text=f"Error finding VHD disk: {e}", fg="red")
            return
        dev_path = f"/dev/sd{chr(98+int(disk_number))}"
        # Mount VHD in WSL
        try:
            result = subprocess.run([
                "wsl", "sudo", "mount", dev_path, mount_point], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"WSL mount failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"WSL mount error: {e}", fg="red")
            return
        # Extract rootfs to mount point
        self.status_label.config(text="Copying rootfs to VHD...", fg="orange")
        self.root.update()
        try:
            # Use unsquashfs if squashfs, else rsync/cp
            if rootfs_path.endswith(".squashfs"):
                result = subprocess.run([
                    "wsl", "sudo", "unsquashfs", "-f", "-d", mount_point, rootfs_path], capture_output=True, text=True)
            else:
                result = subprocess.run([
                    "wsl", "sudo", "cp", "-a", rootfs_path, mount_point], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"Copy failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"Copy error: {e}", fg="red")
            return
        # Unmount VHD
        try:
            subprocess.run(["wsl", "sudo", "umount", mount_point], capture_output=True, text=True)
        except Exception:
            pass
        # ISO'dan kernel ve initrd kopyala
        iso_boot_dir = os.path.join(os.path.dirname(rootfs_path), "boot")
        vmlinuz = os.path.join(iso_boot_dir, "vmlinuz")
        initrd = os.path.join(iso_boot_dir, "initrd.img")
        if not os.path.exists(vmlinuz) or not os.path.exists(initrd):
            self.status_label.config(text="ISO'da vmlinuz veya initrd.img bulunamadı! GRUB çalışmayabilir.", fg="red")
        # Kopyalama işlemi sonrası kernel ve initrd'yi de VHD'ye kopyala
        try:
            if os.path.exists(vmlinuz):
                subprocess.run(["wsl", "sudo", "cp", vmlinuz, mount_point], capture_output=True, text=True)
            if os.path.exists(initrd):
                subprocess.run(["wsl", "sudo", "cp", initrd, mount_point], capture_output=True, text=True)
        except Exception:
            pass
        self.status_label.config(text="Rootfs copied to VHD.", fg="green")

    def install_grub(self):
        # Ask for VHD mount point
        mount_point = filedialog.askdirectory(title="Select VHD mount point (must be empty)")
        if not mount_point:
            self.status_label.config(text="GRUB install cancelled.", fg="red")
            return
        self.status_label.config(text="Installing GRUB (WSL)...", fg="orange")
        self.root.update()
        try:
            # Mount VHD again
            ps_script = """
            $vhd = Get-VHD | Where-Object { $_.Attached -eq $true } | Sort-Object -Property Path -Descending | Select-Object -First 1
            $disk = Get-Disk | Where-Object { $_.Location -like ('*' + $vhd.Path + '*') }
            $disk.Number
            """
            result = subprocess.run([
                "powershell", "-Command", ps_script
            ], capture_output=True, text=True)
            if result.returncode != 0 or not result.stdout.strip():
                self.status_label.config(text="Could not find attached VHD disk.", fg="red")
                return
            disk_number = result.stdout.strip()
            dev_path = f"/dev/sd{chr(98+int(disk_number))}"
            subprocess.run(["wsl", "sudo", "mount", dev_path, mount_point], capture_output=True, text=True)
            # GRUB satırı kernel ve initrd kontrolü ile oluşturulacak
            grub_cfg = os.path.join(mount_point, "boot", "grub", "grub.cfg")
            kernel_path = "/boot/vmlinuz" if os.path.exists(os.path.join(mount_point, "boot", "vmlinuz")) else None
            initrd_path = "/boot/initrd.img" if os.path.exists(os.path.join(mount_point, "boot", "initrd.img")) else None
            if not kernel_path or not initrd_path:
                self.status_label.config(text="VHD'de kernel/initrd yok! GRUB menüsü eksik olabilir.", fg="red")
            with open(grub_cfg, "w") as f:
                f.write(f"""menuentry 'Linux VHD' {{\n    set root=(hd0,1)\n    linux {kernel_path or '/boot/vmlinuz'} root=/dev/sda1 ro quiet\n    initrd {initrd_path or '/boot/initrd.img'}\n}}\n""")
            # Unmount VHD
            subprocess.run(["wsl", "sudo", "umount", mount_point], capture_output=True, text=True)
        except Exception as e:
            self.status_label.config(text=f"GRUB error: {e}", fg="red")
            return
        self.status_label.config(text="GRUB installed and grub.cfg generated.", fg="green")

    def add_vhd_to_boot_menu(self):
        # Ask for VHD path
        vhd_path = filedialog.askopenfilename(title="Select VHD file")
        if not vhd_path:
            self.status_label.config(text="Boot menu add cancelled.", fg="red")
            return
        self.status_label.config(text="Adding VHD to Windows boot menu...", fg="orange")
        self.root.update()
        # Use bcdedit to add a new boot entry
        try:
            guid = subprocess.check_output(["bcdedit", "/create", "/d", "Linux VHD", "/application", "bootsector"], text=True)
            guid = guid.strip().split()[-1]
            subprocess.run(["bcdedit", "/set", guid, "device", f"vhd=[C:]\\{os.path.basename(vhd_path)}"], capture_output=True, text=True)
            subprocess.run(["bcdedit", "/set", guid, "path", "\\bootsect.lnx"], capture_output=True, text=True)
            subprocess.run(["bcdedit", "/displayorder", guid, "/addlast"], capture_output=True, text=True)
        except Exception as e:
            self.status_label.config(text=f"bcdedit error: {e}", fg="red")
            return
        # bootsect.lnx kontrolü ve uyarı
        bootsect_path = os.path.join(os.path.dirname(vhd_path), "bootsect.lnx")
        if not os.path.exists(bootsect_path):
            self.status_label.config(text="bootsect.lnx bulunamadı! Windows doğrudan açamaz. Grub2Win veya EFI kurulumu önerilir.", fg="red")
            return
        self.status_label.config(text="VHD added to Windows boot menu.", fg="green")

    # Linux için VHD oluşturma ve mount
    def create_and_mount_vhd_linux(self):
        vhd_path = filedialog.asksaveasfilename(
            title="Save VHD file as",
            defaultextension=".vhd",
            filetypes=[("VHD files", "*.vhd")]
        )
        if not vhd_path:
            self.status_label.config(text="VHD creation cancelled.", fg="red")
            return
        size_gb = self.vhd_size_gb.get()
        self.status_label.config(text=f"Creating {size_gb}GB VHD (Linux)...", fg="orange")
        self.root.update()
        try:
            result = subprocess.run([
                "qemu-img", "create", "-f", "vpc", vhd_path, f"{size_gb}G"
            ], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"VHD creation failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"VHD error: {e}", fg="red")
            return
        # Mount VHD
        try:
            subprocess.run(["sudo", "modprobe", "nbd", "max_part=8"], capture_output=True, text=True)
            result = subprocess.run(["sudo", "qemu-nbd", "-c", "/dev/nbd0", vhd_path], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"VHD mount failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"VHD mount error: {e}", fg="red")
            return
        self.status_label.config(text=f"VHD created and mounted at /dev/nbd0", fg="green")

    def format_vhd_ext4_linux(self):
        self.status_label.config(text="Formatting /dev/nbd0 as ext4...", fg="orange")
        self.root.update()
        try:
            result = subprocess.run(["sudo", "mkfs.ext4", "/dev/nbd0"], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"Format failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"Format error: {e}", fg="red")
            return
        self.status_label.config(text="VHD formatted as ext4 (/dev/nbd0)", fg="green")

    def copy_rootfs_to_vhd_linux(self):
        rootfs_path = filedialog.askopenfilename(title="Select extracted rootfs (squashfs/rootfs/img)")
        if not rootfs_path:
            self.status_label.config(text="Rootfs copy cancelled.", fg="red")
            return
        mount_point = filedialog.askdirectory(title="Select empty folder for VHD mount (must exist)")
        if not mount_point:
            self.status_label.config(text="VHD mount cancelled.", fg="red")
            return
        self.status_label.config(text="Mounting VHD (/dev/nbd0)...", fg="orange")
        self.root.update()
        try:
            result = subprocess.run(["sudo", "mount", "/dev/nbd0", mount_point], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"Mount failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"Mount error: {e}", fg="red")
            return
        self.status_label.config(text="Copying rootfs to VHD...", fg="orange")
        self.root.update()
        try:
            if rootfs_path.endswith(".squashfs"):
                result = subprocess.run(["sudo", "unsquashfs", "-f", "-d", mount_point, rootfs_path], capture_output=True, text=True)
            else:
                result = subprocess.run(["sudo", "cp", "-a", rootfs_path, mount_point], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"Copy failed: {result.stderr}", fg="red")
                return
        except Exception as e:
            self.status_label.config(text=f"Copy error: {e}", fg="red")
            return
        try:
            subprocess.run(["sudo", "umount", mount_point], capture_output=True, text=True)
        except Exception:
            pass
        self.status_label.config(text="Rootfs copied to VHD.", fg="green")

    def install_grub_linux(self):
        mount_point = filedialog.askdirectory(title="Select VHD mount point (must be empty)")
        if not mount_point:
            self.status_label.config(text="GRUB install cancelled.", fg="red")
            return
        self.status_label.config(text="Installing GRUB (Linux)...", fg="orange")
        self.root.update()
        try:
            subprocess.run(["sudo", "mount", "/dev/nbd0", mount_point], capture_output=True, text=True)
            grub_cfg = os.path.join(mount_point, "boot", "grub", "grub.cfg")
            os.makedirs(os.path.dirname(grub_cfg), exist_ok=True)
            kernel_path = "/boot/vmlinuz" if os.path.exists(os.path.join(mount_point, "boot", "vmlinuz")) else None
            initrd_path = "/boot/initrd.img" if os.path.exists(os.path.join(mount_point, "boot", "initrd.img")) else None
            with open(grub_cfg, "w") as f:
                f.write(f"""menuentry 'Linux VHD' {{\n    set root=(hd0,1)\n    linux {kernel_path or '/boot/vmlinuz'} root=/dev/sda1 ro quiet\n    initrd {initrd_path or '/boot/initrd.img'}\n}}\n""")
            result = subprocess.run(["sudo", "grub-install", "--root-directory=" + mount_point, "/dev/nbd0"], capture_output=True, text=True)
            if result.returncode != 0:
                self.status_label.config(text=f"GRUB install failed: {result.stderr}", fg="red")
                return
            subprocess.run(["sudo", "umount", mount_point], capture_output=True, text=True)
        except Exception as e:
            self.status_label.config(text=f"GRUB error: {e}", fg="red")
            return
        self.status_label.config(text="GRUB installed and grub.cfg generated.", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = LinuxInstallerGUI(root)
    root.mainloop()
