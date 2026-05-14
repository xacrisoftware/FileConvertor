import os
import csv
import json
import io


DATA_FORMATS = {"CSV", "JSON"}

EXT_MAP = {".csv": "CSV", ".json": "JSON"}


class DataConvertError(Exception):
    pass


def get_format_from_ext(path):
    ext = os.path.splitext(path)[1].lower()
    return EXT_MAP.get(ext)


def convert_data(input_path, output_path, output_format):
    in_fmt = get_format_from_ext(input_path)
    out_fmt = output_format.upper()

    if not in_fmt:
        raise DataConvertError("Неизвестный формат входного файла")

    if in_fmt == out_fmt:
        raise DataConvertError("Входной и выходной формат совпадают")

    if out_fmt not in DATA_FORMATS:
        raise DataConvertError(f"Неподдерживаемый формат: {output_format}")

    if in_fmt == "CSV" and out_fmt == "JSON":
        return _csv_to_json(input_path, output_path)
    elif in_fmt == "JSON" and out_fmt == "CSV":
        return _json_to_csv(input_path, output_path)

    raise DataConvertError(f"Конвертация {in_fmt} → {out_fmt} не поддерживается")


def _csv_to_json(input_path, output_path):
    rows = []
    with open(input_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    return output_path


def _json_to_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        raise DataConvertError("JSON не содержит данных")

    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list):
        raise DataConvertError("JSON должен быть массивом или объектом")

    keys = list(data[0].keys()) if data else []
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for row in data:
            writer.writerow([row.get(k, "") for k in keys])

    return output_path
