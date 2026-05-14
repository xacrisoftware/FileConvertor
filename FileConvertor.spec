# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src/icons', 'icons')],
    hiddenimports=[
        'PIL', 'PIL._tkinter_finder',
        'fpdf', 'docx', 'pydub',
        'csv', 'json', 'zipfile', 'tarfile',
        'moviepy',
        'imageio', 'imageio.plugins.ffmpeg',
        'imageio_ffmpeg',
        'proglog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test', 'unittest', 'pdb',
        'email.mime', 'http.cookiejar',
        'matplotlib', 'numpy', 'scipy',
        'curses', 'lib2to3',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FileConvertor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/icon.ico'],
)
