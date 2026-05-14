import os


AUDIO_OUTPUT_FORMATS = {
    "MP3", "WAV", "OGG", "FLAC",
    "M4A", "AAC", "OPUS", "AIFF", "AC3",
    "WMA", "RA", "VOC",
}

EXT_MAP = {
    ".mp3": "MP3", ".wav": "WAV", ".ogg": "OGG",
    ".flac": "FLAC", ".m4a": "M4A", ".aac": "AAC",
    ".opus": "OPUS", ".aiff": "AIFF", ".aif": "AIFF",
    ".ac3": "AC3", ".wma": "WMA", ".ra": "RA",
    ".voc": "VOC",
}

OUTPUT_FORMATS = sorted(AUDIO_OUTPUT_FORMATS, key=lambda f: (
    0 if f in ("MP3", "WAV", "OGG", "FLAC", "M4A", "AAC") else 1, f,
))


class AudioConvertError(Exception):
    pass


def get_format_from_ext(path):
    ext = os.path.splitext(path)[1].lower()
    return EXT_MAP.get(ext)


def convert_audio(input_path, output_path, output_format, bitrate="192k"):
    out_fmt = output_format.upper()
    if out_fmt not in AUDIO_OUTPUT_FORMATS:
        raise AudioConvertError(f"Неподдерживаемый формат: {output_format}")

    try:
        from pydub import AudioSegment
    except ImportError:
        raise AudioConvertError("Установите pydub: pip install pydub")

    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        raise AudioConvertError(f"Не удалось прочитать аудио: {e}")

    ext = os.path.splitext(output_path)[1].lower()
    export_kwargs = {"format": out_fmt.lower()}

    if out_fmt == "MP3":
        export_kwargs["bitrate"] = bitrate
    elif out_fmt == "WMA":
        export_kwargs["format"] = "wma"
    elif out_fmt == "RA":
        export_kwargs["format"] = "rm"
    elif out_fmt == "M4A":
        export_kwargs["format"] = "ipod"

    try:
        audio.export(output_path, **export_kwargs)
    except Exception as e:
        raise AudioConvertError(f"Ошибка экспорта: {e}")

    return output_path
