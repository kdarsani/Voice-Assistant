# myapp.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('www/*', 'www'),
        ('engine/samples/*', 'engine/samples'),
        ('engine/cookies.json', 'engine'),
        ('voice_auth_model.pkl', '.'),
        ('D:/zoe/zoe/envzoe/lib/site-packages/pvporcupine/resources/keyword_files/*', 'pvporcupine/resources/keyword_files')
    ],
    hiddenimports=[
        'hugchat', 'pvporcupine', 'pyautogui', 'pyaudio', 'pywhatkit', 'requests', 'wikipedia', 'pyttsx3', 'speech_recognition', 'eel', 'pywin32'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='MyApp',
)
