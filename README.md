# 🐧 Modern Linux Installer (Windows/ext2fsd Edition)

A professional Linux installation tool for Windows systems, designed to work with ext2/3/4 partitions mounted via [ext2fsd](http://www.ext2fsd.com/) or similar drivers. This version does **not** require WSL or any Linux environment.

## Features
- Modern, intuitive user interface (Tkinter)
- VHD-based Linux installations (VHD creation only; format/copy in Linux)
- Direct installation to existing ext2/3/4 partitions (mounted via ext2fsd)
- Multi-distribution ISO detection (Ubuntu, Debian, antiX, MX, Puppy, etc.)
- Real-time progress tracking
- Windows-native rootfs copy to ext2/3/4 partitions
- No WSL or Linux required for partition operations

## Requirements
- **Windows 10/11**
- **Python 3.8+** (with Tkinter)
- **ext2fsd** (or similar) for mounting ext2/3/4 partitions as Windows drive letters
- **7-Zip** (for ISO extraction; path can be set in the script)
- **QEMU** (for VHD creation; path can be set in the script)

## Installation
1. Install [Python 3.8+](https://www.python.org/downloads/) (ensure Tkinter is included).
2. Install [ext2fsd](http://www.ext2fsd.com/) and mount your ext2/3/4 partitions as Windows drive letters (e.g., E:, F:).
3. Install [7-Zip](https://www.7-zip.org/) and [QEMU](https://www.qemu.org/download/), or update their paths in the script if needed.
4. Clone this repository and run:
   ```
   pip install -r requirements.txt
   python linux-installer.py
   ```

## Usage
- **ISO Extraction:** Select your Linux ISO and extract the root filesystem.
- **Select Existing RootFS:** Choose a previously extracted rootfs folder.
- **Partition Installation:**
  - Select an ext2/3/4 partition (must be mounted via ext2fsd and visible as a drive letter).
  - Copy the rootfs to the partition (Windows-native copy).
- **VHD Operations:**
  - Create VHD files (formatting and rootfs copy must be done in a Linux environment).
- **GRUB Installation:**
  - Not supported in Windows. Please install GRUB from a Linux environment after copying rootfs.


## License
MIT


Support & Donations 🙏
If you find this tool helpful and want to support its development, feel free to donate! Every contribution helps me dedicate more time and improve the project.

Ethereum (EVM, low-fee coins preferred):
0xa3c4468d82881afb64e3fb5100aa0d3e6ea1f4dd

Thank you for being part of this journey! 🚀

If you liked this project, please share it to reach more people! ⭐️🙏

