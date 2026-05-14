import os

VIDEO_OUTPUT_FORMATS = {
    "MP4", "AVI", "MOV", "MKV", "WEBM", "GIF",
    "FLV", "WMV", "M4V", "MPEG", "3GP", "OGV",
    "TS", "VOB", "M2TS", "DV", "ASF",
}

EXT_MAP = {
    ".mp4": "MP4", ".avi": "AVI", ".mov": "MOV",
    ".mkv": "MKV", ".webm": "WEBM", ".gif": "GIF",
    ".flv": "FLV", ".wmv": "WMV", ".m4v": "M4V",
    ".mpeg": "MPEG", ".mpg": "MPEG", ".3gp": "3GP",
    ".ogv": "OGV", ".ts": "TS", ".vob": "VOB",
    ".m2ts": "M2TS", ".dv": "DV", ".asf": "ASF",
}

OUTPUT_FORMATS = sorted(VIDEO_OUTPUT_FORMATS, key=lambda f: (
    0 if f in ("MP4", "AVI", "MOV", "MKV", "WEBM", "GIF") else 1, f,
))


class VideoConvertError(Exception):
    pass


def get_format_from_ext(path):
    ext = os.path.splitext(path)[1].lower()
    return EXT_MAP.get(ext)


def convert_video(input_path, output_path, output_format, bitrate=None):
    out_fmt = output_format.upper()
    if out_fmt not in VIDEO_OUTPUT_FORMATS:
        raise VideoConvertError(f"Неподдерживаемый формат: {output_format}")

    try:
        from moviepy import VideoFileClip
    except ImportError:
        raise VideoConvertError(
            "Установите moviepy: pip install moviepy\nТребуется ffmpeg: https://ffmpeg.org/"
        )

    try:
        clip = VideoFileClip(input_path)
    except Exception as e:
        raise VideoConvertError(f"Не удалось прочитать видео: {e}")

    kwargs = {"logger": None}

    try:
        ext = os.path.splitext(output_path)[1].lower()
        if ext in (".gif",):
            clip.write_gif(output_path, logger=None)
        else:
            if out_fmt in ("WEBM",):
                kwargs["codec"] = "libvpx"
            elif out_fmt in ("AVI",):
                kwargs["codec"] = "libxvid"
            elif out_fmt in ("FLV",):
                kwargs["codec"] = "flv"
            elif out_fmt in ("WMV", "ASF"):
                kwargs["codec"] = "wmv2"
            elif out_fmt in ("MPEG",):
                kwargs["codec"] = "mpeg2video"
            elif out_fmt in ("3GP",):
                kwargs["codec"] = "libx264"
                kwargs["ffmpeg_params"] = ["-profile:v", "baseline", "-level", "3.0"]
            else:
                kwargs["codec"] = "libx264"

            if bitrate and out_fmt not in ("WEBM",):
                kwargs["bitrate"] = bitrate

            clip.write_videofile(output_path, **kwargs)
    except Exception as e:
        clip.close()
        raise VideoConvertError(f"Ошибка конвертации: {e}")

    clip.close()
    return output_path
