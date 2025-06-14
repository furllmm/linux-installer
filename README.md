# linux-installer

# Custom Linux Installer for Windows (WubiUEFI Alternative)

A graphical Python tool to install Linux distributions on Windows using a VHD file, inspired by WubiUEFI.  
**No need to repartition your disk!**  
Supports Ubuntu, Debian, Arch, Fedora, Slax, Manjaro, TinyCore, and more.

---

## Features

- **Easy GUI:** Select your Linux ISO and follow the steps.
- **Automatic ISO Detection:** Detects the base of your ISO (Ubuntu, Arch, etc.).
- **VHD Creation:** Create a virtual disk (VHD) of any size.
- **Filesystem Setup:** Format the VHD as ext4 using WSL.
- **RootFS Extraction:** Extract and copy the Linux root filesystem to the VHD.
- **GRUB Bootloader:** Installs GRUB and generates a basic `grub.cfg`.
- **Windows Boot Menu:** Adds your Linux VHD to the Windows boot menu (via `bcdedit`).
- **No Partitioning:** Safe for your existing Windows installation.

---

## Requirements

- **Windows 10/11** (Administrator rights required)
- **Python 3.8+**
- **WSL (Windows Subsystem for Linux) installed**
- **7-Zip** (added to your PATH)
- **Linux ISO** (Ubuntu, Debian, Arch, etc.)

---

## Installation

1. **Clone this repository:**
    ```sh
    git clone https://github.com/furllamm/linux-vhd-installer.git
    cd linux-vhd-installer
    ```

2. **Install Python dependencies:**
    - Run `requirements.bat` to install all required Python modules and check for system dependencies.
    - *(Most dependencies are standard libraries.)*

3. **Run the installer as Administrator:**
    - Right-click and select "Run as administrator" or launch from an elevated command prompt.

---

## Usage

1. **Select your Linux ISO.**
2. **Extract the root filesystem** (squashfs/rootfs).
3. **Create and mount a VHD** (choose size with the slider).
4. **Format the VHD as ext4** (via WSL).
5. **Copy the rootfs to the VHD.**
6. **Install GRUB bootloader** (via WSL).
7. **Add the VHD to Windows boot menu.**
8. **Reboot and select your new Linux from the Windows boot menu!**

---

## Supported Distributions

- Ubuntu / Debian (casper)
- Arch / Manjaro
- Fedora
- Slax / Slackware
- TinyCore / Puppy Linux
- Any ISO with standard squashfs/rootfs layout

---

## Notes & Tips

- **Run as Administrator!** Disk and boot menu operations require admin rights.
- **WSL must be installed and enabled.**
- **7-Zip must be in your PATH.**
- **For EFI systems:** You may need to use [Grub2Win](https://sourceforge.net/projects/grub2win/) or install GRUB to the EFI partition manually.
- **If `bootsect.lnx` is missing:** Windows cannot boot directly; use Grub2Win or similar tools.
- **Feedback & Fixes:** This tool is experimental. You are welcome to suggest code improvements or fixes via issues or pull requests.

---

## Disclaimer

This tool is experimental. Use at your own risk.  
Always back up important data before modifying boot settings or disks.

---

## License

MIT License

---

## Contributing

Pull requests and suggestions are welcome!

---

## Credits

- Inspired by [WubiUEFI](https://github.com/hakuna-m/wubiuefi)
- Developed by [furllamm](https://github.com/furllamm)

--

also donate me if u want: :D
EVM (only low fee coins accepted) : 0xa3c4468d82881afb64e3fb5100aa0d3e6ea1f4dd
