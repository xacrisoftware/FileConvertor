# FILE CONVERTOR

> Drop a file. Pick a format. Done.

A simple file converter for Windows. Works offline. No ads. No signup.

---

## 📦 What you can convert

| Category | Input → Output | Count |
|----------|---------------|-------|
| 🖼️ Images | PNG ↔ JPEG ↔ WEBP ↔ BMP ↔ GIF ↔ TIFF ↔ ICO ↔ AVIF ↔ PPM ↔ PCX ↔ TGA ↔ QOI ↔ DDS ↔ SGI ↔ PDF ↔ more | **29** |
| 🎬 Video | MP4 ↔ AVI ↔ MOV ↔ MKV ↔ WEBM ↔ GIF ↔ FLV ↔ WMV ↔ M4V ↔ MPEG ↔ 3GP ↔ OGV ↔ TS ↔ VOB ↔ more | **17** |
| 🎵 Audio | MP3 ↔ WAV ↔ OGG ↔ FLAC ↔ M4A ↔ AAC ↔ OPUS ↔ AIFF ↔ AC3 ↔ WMA ↔ more | **12** |
| 📄 Documents | TXT ↔ PDF ↔ DOCX | **3** |
| 🗜️ Archives | ZIP / TAR / TAR.GZ — create or extract | **3** |
| 📊 Data | CSV ⟷ JSON | **2** |

**58 formats total.**

---

## ✨ Features

- Dark minimal UI — just select a file and pick a format
- Drag & drop on home page — auto-detects file type
- Swap formats with one click (⇄)
- Edit output filename before converting
- Quality slider (images) and bitrate selector (audio/video)
- Cancel conversion if you change your mind
- [Open] button — opens file right after conversion
- Keeps history of all conversions
- English / Russian interface

---

## ⬇️ Download & Install

### 🪟 Portable (just run it)
Download `FileConvertor.exe` and double-click. No installation needed.

### 📦 Installer
Download `FileConvertor_Setup_v1.0.0.exe`, run it, click Next → Next → Install.

### 🐍 From source (requires Python)

```bash
git clone https://github.com/xacrisoftware/FileConvertor.git
cd FileConvertor
pip install -r requirements.txt
python src/main.py
```

---

## 🔧 Requirements

- Windows 10 or 11 (64-bit)
- [FFmpeg](https://ffmpeg.org/) — only needed for video & audio (`winget install ffmpeg`)

---

## 🧱 Built with

- [Python](https://python.org) + [CustomTkinter](https://customtkinter.tomschimansky.com)
- [Pillow](https://python-pillow.org) — images
- [moviepy](https://zulko.github.io/moviepy/) — video
- [pydub](https://github.com/jiaaro/pydub) — audio
- [fpdf2](https://pyfpdf.github.io/fpdf2/) / [python-docx](https://python-docx.readthedocs.io/) — documents
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF reading

---

## 📄 License

MIT — do whatever you want.
