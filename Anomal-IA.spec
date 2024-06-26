# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Anomal-IA.py'],
    pathex=[],
    binaries=[],
    datas=[('config.json', '.'), ('templates', 'templates'), ('static', 'static'), ('app.py', '.'), ('Funciones_Cluster.py', '.'), ('Funciones_Procesamiento.py', '.'), ('rutas.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Anomal-IA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Anomal-IA',
)
