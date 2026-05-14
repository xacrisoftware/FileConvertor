import os
import sys
import json
from datetime import datetime
from PIL import Image
import customtkinter as ctk

if getattr(sys, "frozen", False):
    _BASE = sys._MEIPASS
    _DATA = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(__file__)
    _DATA = _BASE

CONFIG_FILE = os.path.join(_DATA, "config.json")
HISTORY_FILE = os.path.join(_DATA, "history.json")
ICONS_DIR = os.path.join(_BASE, "icons")
EXPORTS_DIR = os.path.join(_DATA, "exports")

DEFAULT_CONFIG = {
    "save_history": True,
    "auto_export": False,
    "image_quality": 90,
    "audio_bitrate": "192k",
    "language": "en",
    "last_output_dir": "",
}

IMAGE_EXTENSIONS = {
    ".png": "PNG", ".jpg": "JPEG", ".jpeg": "JPEG",
    ".webp": "WEBP", ".bmp": "BMP", ".gif": "GIF",
    ".tiff": "TIFF", ".tif": "TIFF", ".ico": "ICO",
    ".avif": "AVIF", ".jp2": "JPEG2000", ".ppm": "PPM",
    ".pgm": "PPM", ".pbm": "PPM", ".pcx": "PCX",
    ".tga": "TGA", ".xbm": "XBM", ".qoi": "QOI",
    ".dds": "DDS", ".sgi": "SGI", ".eps": "EPS",
    ".pdf": "PDF", ".icns": "ICNS", ".dib": "DIB",
    ".im": "IM", ".msp": "MSP", ".blp": "BLP",
    ".bufr": "BUFR", ".grib": "GRIB", ".h5": "HDF5",
    ".hdf": "HDF5", ".spi": "SPIDER", ".wmf": "WMF",
    ".cur": "CUR",
}

AUDIO_EXTENSIONS = {
    ".mp3": "MP3", ".wav": "WAV", ".ogg": "OGG",
    ".flac": "FLAC", ".m4a": "M4A", ".aac": "AAC",
    ".opus": "OPUS", ".aiff": "AIFF", ".aif": "AIFF",
    ".ac3": "AC3", ".wma": "WMA", ".ra": "RA", ".voc": "VOC",
}

DOCUMENT_EXTENSIONS = {
    ".txt": "TXT",
    ".pdf": "PDF",
    ".docx": "DOCX",
}

DOCUMENT_OUTPUT_FORMATS = ["TXT", "PDF", "DOCX"]

ARCHIVE_READ_EXTENSIONS = {
    ".zip": "ZIP",
    ".tar": "TAR",
    ".gz": "GZIP",
    ".tar.gz": "TAR.GZ",
    ".tgz": "TAR.GZ",
}

ARCHIVE_CREATE_FORMATS = ["ZIP", "TAR", "TAR.GZ"]

DATA_EXTENSIONS = {
    ".csv": "CSV",
    ".json": "JSON",
}

DATA_OUTPUT_FORMATS = ["CSV", "JSON"]

VIDEO_EXTENSIONS = {
    ".mp4": "MP4", ".avi": "AVI", ".mov": "MOV",
    ".mkv": "MKV", ".webm": "WEBM", ".gif": "GIF",
    ".flv": "FLV", ".wmv": "WMV", ".m4v": "M4V",
    ".mpeg": "MPEG", ".mpg": "MPEG", ".3gp": "3GP",
    ".ogv": "OGV", ".ts": "TS", ".vob": "VOB",
    ".m2ts": "M2TS", ".dv": "DV", ".asf": "ASF",
}


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return dict(default) if isinstance(default, dict) else list(default)


def save_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_icon(name, size=(18, 18)):
    fp = os.path.join(ICONS_DIR, f"{name}.png")
    try:
        if os.path.exists(fp):
            return ctk.CTkImage(Image.open(fp), size=size)
    except Exception:
        pass
    return None


def format_size(n_bytes):
    for unit in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unit}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} TB"
