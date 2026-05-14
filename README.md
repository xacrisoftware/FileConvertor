<p align="center">
  <img src="https://img.shields.io/badge/⬇%20FILE%20CONVERTOR-1.0.0-000?style=for-the-badge&labelColor=1a1a1a" alt="FILE CONVERTOR" height="50">
</p>

<p align="center">
  <strong>A simple file converter for Windows.</strong><br>
  <em>Drop a file, pick a format, go.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/Offline-Yes-success?style=flat-square" alt="Offline">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/github/stars/xacrisoftware/FileConvertor?style=flat-square" alt="Stars">
</p>

---

## 📸 Screenshots

<p align="center">
  <img src="assets/screenshots/Screenshot_3.png" alt="FILE CONVERTOR" width="80%">
</p>

<p align="center">
  <img src="assets/screenshots/Screenshot_4.png" alt="FILE CONVERTOR" width="80%">
</p>

---

## ✨ Features

| | |
|---|---|
| **58 formats** | Images, Video, Audio, Documents, Archives, Data |
| **Dark theme** | Minimal UI, Consolas font, sharp corners |
| **Fully offline** | Your files never leave your computer |
| **Drag & drop** | Drop a file, app detects the type automatically |
| **Swap formats** | One click to swap source ↔ target |
| **Quality control** | Sliders for images, bitrate selectors for audio/video |

---

## 📦 What you can convert

| Category | Supported formats |
|----------|------------------|
| 🖼️ **Images** (29) | PNG, JPEG, WEBP, BMP, GIF, TIFF, ICO, AVIF, JPEG2000, PPM, PCX, TGA, QOI, DDS, SGI, PDF |
| 🎬 **Video** (17) | MP4, AVI, MOV, MKV, WEBM, GIF, FLV, WMV, M4V, MPEG, 3GP, OGV, TS, VOB |
| 🎵 **Audio** (12) | MP3, WAV, OGG, FLAC, M4A, AAC, OPUS, AIFF, AC3, WMA |
| 📄 **Documents** (3) | TXT ↔ PDF ↔ DOCX |
| 🗜️ **Archives** (3) | ZIP / TAR / TAR.GZ — create or extract |
| 📊 **Data** (2) | CSV ⟷ JSON |

---

## ⬇️ Download

| Version | File | What to do |
|---------|------|-----------|
| 🪟 **Portable** | `FileConvertor.exe` | Download and run. No install. |
| 📦 **Installer** | `FileConvertor_Setup_v1.0.0.exe` | Run, click Next, done. Desktop shortcut. |
| 🐍 **Source** | `git clone ...` | Requires Python + dependencies |

**[Download latest →](https://github.com/xacrisoftware/FileConvertor/releases)**

```bash
# From source
git clone https://github.com/xacrisoftware/FileConvertor.git
cd FileConvertor
pip install -r requirements.txt
python src/main.py
```

---

## 🔧 Requirements

- **Windows 10 or 11** (64-bit)
- **FFmpeg** — needed for video & audio conversion ([download](https://ffmpeg.org/) or `winget install ffmpeg`)

---

## 🧱 Tech stack

| Layer | Libraries |
|-------|-----------|
| **UI** | [Python](https://python.org) + [CustomTkinter](https://customtkinter.tomschimansky.com) |
| **Images** | [Pillow](https://python-pillow.org) — 29 formats |
| **Video** | [moviepy](https://zulko.github.io/moviepy) — 17 formats |
| **Audio** | [pydub](https://github.com/jiaaro/pydub) — 12 formats |
| **Documents** | [fpdf2](https://pyfpdf.github.io/fpdf2) + [python-docx](https://python-docx.readthedocs.io) + [PyMuPDF](https://pymupdf.readthedocs.io) |
| **Archives** | zipfile / tarfile (stdlib) |

---

## 📄 License

MIT — do whatever you want. See [LICENSE](LICENSE).
