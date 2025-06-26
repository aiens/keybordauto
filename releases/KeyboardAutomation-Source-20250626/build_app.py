#!/usr/bin/env python3
"""
应用程序打包脚本
支持macOS和Windows平台
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path


def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == 'darwin':
        return 'macos', arch
    elif system == 'windows':
        return 'windows', arch
    elif system == 'linux':
        return 'linux', arch
    else:
        return system, arch


def create_spec_file():
    """创建PyInstaller spec文件"""
    system, arch = get_platform_info()
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
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
'''

    if system == 'macos':
        spec_content += '''    icon='assets/icon.icns',
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
)'''
    elif system == 'windows':
        spec_content += '''    icon='assets/icon.ico',
)'''
    else:
        spec_content += '''    icon='assets/icon.png',
)'''
    
    with open('KeyboardAutomation.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✓ 已创建 {system} 平台的spec文件")


def create_assets():
    """创建资源文件"""
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # 创建简单的图标文件（这里用文本描述，实际应该是图标文件）
    icon_info = """
# 图标文件说明
请将以下图标文件放置在 assets/ 目录中：

macOS: icon.icns (512x512 像素的 .icns 文件)
Windows: icon.ico (256x256 像素的 .ico 文件)  
Linux: icon.png (256x256 像素的 .png 文件)

可以使用在线工具将 PNG 图片转换为对应格式：
- https://convertio.co/png-icns/ (PNG to ICNS)
- https://convertio.co/png-ico/ (PNG to ICO)
"""
    
    with open(assets_dir / 'icon_readme.txt', 'w', encoding='utf-8') as f:
        f.write(icon_info)
    
    print("✓ 已创建资源目录和说明文件")


def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import pyinstaller
        print("✓ PyInstaller 已安装")
        return True
    except ImportError:
        print("正在安装 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller==6.3.0'])
            print("✓ PyInstaller 安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ PyInstaller 安装失败: {e}")
            return False


def build_app():
    """构建应用程序"""
    system, arch = get_platform_info()
    
    print(f"开始为 {system}-{arch} 平台构建应用程序...")
    
    # 清理之前的构建
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 已清理 {dir_name} 目录")
    
    # 构建命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'KeyboardAutomation.spec'
    ]
    
    try:
        print("正在构建应用程序...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 应用程序构建成功！")
            
            # 显示输出文件信息
            dist_dir = Path('dist')
            if dist_dir.exists():
                print(f"\n构建输出位于: {dist_dir.absolute()}")
                for item in dist_dir.iterdir():
                    size = get_size_str(item)
                    print(f"  - {item.name} ({size})")
            
            return True
        else:
            print("✗ 应用程序构建失败")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ 构建过程出错: {e}")
        return False


def get_size_str(path):
    """获取文件/目录大小字符串"""
    if path.is_file():
        size = path.stat().st_size
    else:
        size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def create_build_scripts():
    """创建平台特定的构建脚本"""
    system, _ = get_platform_info()
    
    if system == 'macos':
        # macOS 构建脚本
        macos_script = '''#!/bin/bash
# macOS 应用构建脚本

echo "开始构建 macOS 应用程序..."

# 检查依赖
python3 -c "import pyautogui, pynput, PIL" || {
    echo "安装依赖包..."
    pip3 install -r requirements.txt
}

# 构建应用
python3 build_app.py

echo "构建完成！"
echo "应用程序位于: dist/KeyboardAutomation.app"
echo ""
echo "使用说明:"
echo "1. 双击运行 KeyboardAutomation.app"
echo "2. 首次运行需要授权辅助功能权限"
echo "3. 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能"
'''
        
        with open('build_macos.sh', 'w', encoding='utf-8') as f:
            f.write(macos_script)
        os.chmod('build_macos.sh', 0o755)
        
    elif system == 'windows':
        # Windows 构建脚本
        windows_script = '''@echo off
REM Windows 应用构建脚本

echo 开始构建 Windows 应用程序...

REM 检查依赖
python -c "import pyautogui, pynput, PIL" 2>nul || (
    echo 安装依赖包...
    pip install -r requirements.txt
)

REM 构建应用
python build_app.py

echo 构建完成！
echo 应用程序位于: dist\KeyboardAutomation.exe
echo.
echo 使用说明:
echo 1. 双击运行 KeyboardAutomation.exe
echo 2. Windows 可能会显示安全警告，选择"仍要运行"
echo 3. 某些杀毒软件可能会误报，请添加到白名单

pause
'''
        
        with open('build_windows.bat', 'w', encoding='utf-8') as f:
            f.write(windows_script)
    
    print(f"✓ 已创建 {system} 构建脚本")


def main():
    """主函数"""
    print("键盘自动化软件 - 应用打包工具")
    print("=" * 40)
    
    system, arch = get_platform_info()
    print(f"当前平台: {system}-{arch}")
    
    # 安装PyInstaller
    if not install_pyinstaller():
        return False
    
    # 创建资源文件
    create_assets()
    
    # 创建spec文件
    create_spec_file()
    
    # 创建构建脚本
    create_build_scripts()
    
    # 构建应用
    if build_app():
        print("\n🎉 应用程序打包完成！")
        print(f"输出目录: {Path('dist').absolute()}")
        
        if system == 'macos':
            print("\nmacOS 使用说明:")
            print("1. 运行 ./build_macos.sh 或直接运行 dist/KeyboardAutomation.app")
            print("2. 首次运行需要授权辅助功能权限")
            print("3. 系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能")
        elif system == 'windows':
            print("\nWindows 使用说明:")
            print("1. 运行 build_windows.bat 或直接运行 dist/KeyboardAutomation.exe")
            print("2. 可能需要允许防火墙访问")
            print("3. 某些杀毒软件可能误报，请添加到白名单")
        
        return True
    else:
        print("\n❌ 应用程序打包失败")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
