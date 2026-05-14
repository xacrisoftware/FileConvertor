import os
import zipfile
import tarfile


CREATE_FORMATS = {".zip", ".tar", ".tar.gz", ".tgz"}
EXTRACT_FORMATS = {".zip", ".tar", ".tar.gz", ".tgz"}

EXT_MAP = {
    ".zip": "ZIP",
    ".tar": "TAR",
    ".tar.gz": "TAR.GZ",
    ".tgz": "TAR.GZ",
    ".gz": "GZIP",
}


class ArchiveError(Exception):
    pass


def get_format_from_ext(path):
    p = path.lower()
    if p.endswith(".tar.gz"):
        return "TAR.GZ"
    if p.endswith(".tgz"):
        return "TAR.GZ"
    ext = os.path.splitext(p)[1]
    return EXT_MAP.get(ext)


def create_archive(output_path, files, archive_format="ZIP"):
    fmt = archive_format.upper()
    dir_path = os.path.dirname(output_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    if fmt == "ZIP":
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for fp in files:
                arcname = os.path.basename(fp)
                zf.write(fp, arcname)
    elif fmt in ("TAR", "TAR.GZ"):
        mode = "w:gz" if fmt == "TAR.GZ" else "w"
        with tarfile.open(output_path, mode) as tf:
            for fp in files:
                tf.add(fp, arcname=os.path.basename(fp))
    else:
        raise ArchiveError(f"Неподдерживаемый формат архива: {archive_format}")

    return output_path


def extract_archive(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    p = input_path.lower()

    if p.endswith(".zip"):
        with zipfile.ZipFile(input_path, "r") as zf:
            zf.extractall(output_dir)
    elif p.endswith(".tar.gz") or p.endswith(".tgz"):
        with tarfile.open(input_path, "r:gz") as tf:
            tf.extractall(output_dir)
    elif p.endswith(".tar"):
        with tarfile.open(input_path, "r:") as tf:
            tf.extractall(output_dir)
    else:
        raise ArchiveError(f"Неподдерживаемый формат архива: {os.path.splitext(input_path)[1]}")

    return output_dir


def get_archive_members(input_path):
    members = []
    p = input_path.lower()

    try:
        if p.endswith(".zip"):
            with zipfile.ZipFile(input_path, "r") as zf:
                members = [{"name": m.filename, "size": m.file_size} for m in zf.infolist() if not m.is_dir()]
        elif p.endswith((".tar.gz", ".tgz", ".tar")):
            mode = "r:gz" if p.endswith((".tar.gz", ".tgz")) else "r:"
            with tarfile.open(input_path, mode) as tf:
                members = [{"name": m.name, "size": m.size} for m in tf.getmembers() if m.isfile()]
    except Exception:
        pass

    return members
