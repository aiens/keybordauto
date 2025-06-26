# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('configs', 'configs'),
        ('使用指南.md', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'keyboard_automation',
        'keyboard_automation.engine',
        'keyboard_automation.config',
        'keyboard_automation.gui',
        'pynput.keyboard',
        'pynput.mouse',
        'pyautogui',
        'PIL',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeyboardAutomation',
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
    icon='assets/icon.icns',
)

app = BUNDLE(
    exe,
    name='KeyboardAutomation.app',
    icon='assets/icon.icns',
    bundle_identifier='com.keyboardsys.automation',
    info_plist={
        'NSHighResolutionCapable': 'True',
        'NSAppleEventsUsageDescription': '键盘自动化软件需要控制其他应用程序',
        'NSAccessibilityUsageDescription': '键盘自动化软件需要访问辅助功能来模拟键盘输入',
        'LSUIElement': False,
    },
)