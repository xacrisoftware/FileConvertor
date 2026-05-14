# FILE CONVERTOR

A simple file converter for Windows. Drop a file, pick a format, done.

58 formats. Dark theme. No ads. No internet needed.

---

## What it can do

- Turn PNG into JPG, MP4 into GIF, PDF into TXT — anything to anything
- Resize, compress, change quality
- Create and unpack ZIP / TAR archives
- Convert CSV ↔ JSON

## How to use

**Portable:** download `FileConvertor.exe`, double-click, go.

**Installer:** download `FileConvertor_Setup.exe`, run it, follow the wizard.

**From source:**
```
git clone https://github.com/xacrisoftware/FileConvertor.git
cd FileConvertor
pip install -r requirements.txt
python src/main.py
```

## Requirements

- Windows 10 or 11
- [FFmpeg](https://ffmpeg.org/) for video and audio (`winget install ffmpeg`)
