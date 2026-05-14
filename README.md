# FILE CONVERTOR

> Универсальный конвертер файлов с минималистичным дизайном.  
> Изображения, документы, видео, аудио, архивы, данные — всё в одном окне.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Возможности

| Категория | Форматы | Библиотека |
|-----------|---------|------------|
| **Изображения** | **29 форматов**: PNG, JPEG, WEBP, BMP, GIF, TIFF, ICO, AVIF, JPEG2000, PPM, PCX, TGA, XBM, QOI, DDS, SGI, PDF и другие | Pillow |
| **Документы** | TXT ↔ PDF ↔ DOCX | fpdf2, python-docx, PyMuPDF |
| **Видео** | **17 форматов**: MP4, AVI, MOV, MKV, WEBM, GIF, FLV, WMV, M4V, MPEG, 3GP, OGV и другие | moviepy |
| **Аудио** | **12 форматов**: MP3, WAV, OGG, FLAC, M4A, AAC, OPUS, AIFF, AC3, WMA и другие | pydub |
| **Архивы** | ZIP / TAR / TAR.GZ (создание и распаковка) | zipfile, tarfile |
| **Данные** | CSV ⟷ JSON | csv, json |

### Особенности
- Тёмная тема с минималистичным интерфейсом
- Drag & drop (главный экран)
- Выбор имени выходного файла до конвертации
- Swap форматов одним кликом `⇄`
- История конвертаций
- Настройки качества, битрейта
- Работает полностью локально — без интернета

---

## Установка

### Вариант 1 — Готовый установщик
1. Скачай `FileConvertor_Setup.exe` из [релизов](https://github.com/username/FileConvertor/releases)
2. Запусти — установка в один клик
3. Ярлык на рабочем столе и в меню Пуск

### Вариант 2 — Portable (.exe)
1. Скачай `FileConvertor.exe` из [релизов](https://github.com/username/FileConvertor/releases)
2. Запусти — ничего устанавливать не нужно

### Вариант 3 — Из исходников
```bash
git clone https://github.com/username/FileConvertor.git
cd FileConvertor

# Установка зависимостей
pip install -r requirements.txt

# Генерация иконок
python gen_icons.py

# Запуск
python main.py
```

### Зависимости
- Python 3.10+
- FFmpeg (для видео и аудио) — [скачать](https://ffmpeg.org/)
  - Или через `winget install ffmpeg` / `choco install ffmpeg`

---

## Структура проекта

```
FileConvertor/
├── FileConvertor.exe         # ✅ Готовый .exe — запускай сразу
├── run.bat                   # Быстрый запуск (двойной клик)
├── run.ps1                   # PowerShell запуск
│
├── src/                      # Исходный код
│   ├── main.py               # Точка входа
│   ├── app.py                # Окно приложения
│   ├── config.py             # Конфиги
│   ├── gen_icons.py          # Генератор иконок
│   ├── icons/                # Иконки (генерируются)
│   ├── icon.ico              # Иконка приложения
│   ├── converters/           # Логика конвертации
│   │   ├── image_conv.py
│   │   ├── document_conv.py
│   │   ├── video_conv.py
│   │   ├── audio_conv.py
│   │   ├── archive_conv.py
│   │   └── data_conv.py
│   └── ui/                   # Интерфейс
│       ├── sidebar.py
│       ├── content.py
│       ├── home_view.py
│       ├── image_view.py
│       ├── document_view.py
│       ├── video_view.py
│       ├── audio_view.py
│       ├── archive_view.py
│       └── data_view.py
│
├── FileConvertor.spec        # PyInstaller spec
├── requirements.txt          # Зависимости
├── README.md
├── LICENSE
├── .gitignore
│
├── installer/
│   └── setup.iss             # Inno Setup скрипт
├── dist/                     # Сборка PyInstaller
└── build/                    # Временные файлы сборки
```

---

## Сборка .exe самостоятельно

```bash
# Установка PyInstaller
pip install pyinstaller

# Генерация иконок (если ещё нет)
python gen_icons.py

# Сборка
pyinstaller FileConvertor.spec --clean
```

Готовый `.exe` появится в `dist/FileConvertor.exe`

---

## Создание установщика

Установщик делается через [Inno Setup](https://jrsoftware.org/isinfo.php):

1. Установи Inno Setup
2. Собери `.exe` через PyInstaller (шаг выше)
3. Открой `installer/setup.iss` в Inno Setup
4. Нажми **Compile** — получишь `FileConvertor_Setup.exe`

Или запусти из командной строки:
```bash
iscc installer\setup.iss
```

---

## GitHub — выкладываем релиз

```bash
# 1. Создай репозиторий на github.com (например, FileConvertor)
# 2. В корне проекта:
git init
git add .
git commit -m "Initial release v1.0"

# 3. Привяжи удалённый репозиторий
git remote add origin https://github.com/username/FileConvertor.git

# 4. Залей код
git push -u origin main

# 5. Создай релиз через GitHub UI:
#    — Tag: v1.0.0
#    — Title: "FILE CONVERTOR v1.0.0"
#    — Description: вставь содержимое README.md
#    — Assets: прикрепи FileConvertor.exe (portable)
#      и FileConvertor_Setup_v1.0.0.exe (установщик)

# Файлы для релиза лежат в корне проекта:
#   FileConvertor.exe          ← Portable (90 MB)
#   FileConvertor_Setup_v1.0.0.exe  ← Установщик (91 MB)
```

---

## Лицензия

MIT — делай что хочешь, но без гарантий.
