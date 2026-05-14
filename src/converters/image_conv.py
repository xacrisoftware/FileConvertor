import os
from PIL import Image

Image.init()

_PILLOW_SAVE_FORMATS = set(Image.SAVE.keys())

SAVE_FORMAT_EXT = {
    "PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp",
    "BMP": ".bmp", "GIF": ".gif", "TIFF": ".tiff", "ICO": ".ico",
    "AVIF": ".avif", "JPEG2000": ".jp2", "PPM": ".ppm",
    "PCX": ".pcx", "TGA": ".tga", "XBM": ".xbm",
    "QOI": ".qoi", "DDS": ".dds", "SGI": ".sgi", "EPS": ".eps",
    "PDF": ".pdf", "ICNS": ".icns", "DIB": ".dib", "IM": ".im",
    "MSP": ".msp", "PALM": ".palm", "BUFR": ".bufr",
    "GRIB": ".grib", "HDF5": ".h5", "BLP": ".blp",
    "SPIDER": ".spi", "WMF": ".wmf",
}

# Only expose formats Pillow can actually write
OUTPUT_FORMATS = sorted(
    [f for f in SAVE_FORMAT_EXT if f in _PILLOW_SAVE_FORMATS],
    key=lambda f: (0 if f in ("PNG", "JPEG", "WEBP", "BMP", "GIF", "TIFF", "ICO", "AVIF") else 1, f),
)
# Always include JPEG (mapped from JPG)
if "JPEG" not in OUTPUT_FORMATS:
    OUTPUT_FORMATS.append("JPEG")

READ_EXT_MAP = {}
for ext, fmt in Image.registered_extensions().items():
    READ_EXT_MAP[ext.lower()] = fmt
READ_EXT_MAP[".jpg"] = "JPEG"
READ_EXT_MAP[".tif"] = "TIFF"


class ImageConvertError(Exception):
    pass


def get_format_from_ext(path):
    ext = os.path.splitext(path)[1].lower()
    fmt = READ_EXT_MAP.get(ext)
    if fmt in ("CUR",):
        return None
    return fmt


def get_compatible_input_formats():
    return list(OUTPUT_FORMATS)


def convert_image(input_path, output_path, output_format, quality=90):
    output_format = output_format.upper()

    try:
        img = Image.open(input_path)
    except Exception as e:
        raise ImageConvertError(f"Не удалось открыть изображение: {e}")

    exts = os.path.splitext(output_path)[1].lower()
    save_fmt = output_format
    if save_fmt == "JPG":
        save_fmt = "JPEG"

    if save_fmt in ("JPEG", "JPG"):
        if img.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            mask = img.split()[-1] if img.mode == "RGBA" else None
            bg.paste(img, mask=mask)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

    if save_fmt == "ICO":
        img = img.convert("RGBA")

    save_kwargs = {}
    if save_fmt in ("JPEG", "WEBP", "AVIF", "JPEG2000"):
        save_kwargs["quality"] = quality
    if save_fmt == "TIFF":
        save_kwargs["compression"] = "tiff_lzw"

    try:
        img.save(output_path, format=save_fmt, **save_kwargs)
    except Exception as e:
        raise ImageConvertError(f"Ошибка сохранения: {e}")

    return output_path
