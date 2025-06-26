#!/usr/bin/env python3
"""
创建发布包脚本
"""

import os
import sys
import shutil
import zipfile
import platform
from pathlib import Path
from datetime import datetime


def get_version():
    """获取版本号"""
    try:
        from keyboard_automation import __version__
        return __version__
    except:
        return "1.0.0"


def create_release_package():
    """创建发布包"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    version = get_version()
    timestamp = datetime.now().strftime("%Y%m%d")
    
    # 发布包名称
    release_name = f"KeyboardAutomation-{version}-{system}-{arch}-{timestamp}"
    release_dir = Path("releases") / release_name
    
    print(f"Creating release package: {release_name}")
    
    # 清理并创建发布目录
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制应用程序
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("dist directory not found, please run build script first")
        return False
    
    print("Copying application files...")
    if system == "darwin":
        # macOS应用包
        app_path = dist_dir / "KeyboardAutomation.app"
        if app_path.exists():
            shutil.copytree(app_path, release_dir / "KeyboardAutomation.app")
            print("Copied KeyboardAutomation.app")
        else:
            print("KeyboardAutomation.app not found")
            return False
    else:
        # Windows/Linux可执行文件
        exe_name = "KeyboardAutomation.exe" if system == "windows" else "KeyboardAutomation"
        exe_path = dist_dir / exe_name
        if exe_path.exists():
            shutil.copy2(exe_path, release_dir / exe_name)
            print(f"Copied {exe_name}")
        else:
            print(f"{exe_name} not found")
            return False
    
    # 复制文档和配置
    print("Copying documentation and configuration files...")
    files_to_copy = [
        "README.md",
        "使用指南.md", 
        "打包说明.md",
        "configs"
    ]
    
    for item in files_to_copy:
        src_path = Path(item)
        if src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, release_dir / item)
            else:
                shutil.copy2(src_path, release_dir / item)
            print(f"Copied {item}")
        else:
            print(f"Warning: {item} not found")
    
    # 创建启动脚本
    print("Creating launch scripts...")
    create_launch_scripts(release_dir, system)

    # 创建安装说明
    print("Creating installation instructions...")
    create_install_readme(release_dir, system, version)

    # 创建压缩包
    print("Creating archive...")
    if system == "windows":
        archive_path = f"releases/{release_name}.zip"
        create_zip_archive(release_dir, archive_path)
    else:
        archive_path = f"releases/{release_name}.tar.gz"
        create_tar_archive(release_dir, archive_path)
    
    print(f"Release package creation completed!")
    print(f"Directory: {release_dir}")
    print(f"Archive: {archive_path}")
    
    return True


def create_launch_scripts(release_dir, system):
    """创建启动脚本"""
    if system == "darwin":
        # macOS启动脚本
        script_content = '''#!/bin/bash
# macOS 启动脚本

echo "启动键盘自动化软件..."
echo "如果是首次运行，请按照提示设置权限"
echo ""

# 检查应用程序是否存在
if [ ! -d "KeyboardAutomation.app" ]; then
    echo "❌ 未找到 KeyboardAutomation.app"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

# 启动应用程序
open KeyboardAutomation.app

echo "✅ 应用程序已启动"
echo "如果遇到权限问题，请查看使用指南.md"
'''
        
        script_path = release_dir / "启动应用.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
    elif system == "windows":
        # Windows启动脚本
        script_content = '''@echo off
REM Windows 启动脚本

echo 启动键盘自动化软件...
echo 如果是首次运行，请按照提示设置权限
echo.

REM 检查可执行文件是否存在
if not exist "KeyboardAutomation.exe" (
    echo ❌ 未找到 KeyboardAutomation.exe
    echo 请确保在正确的目录中运行此脚本
    pause
    exit /b 1
)

REM 启动应用程序
echo 正在启动应用程序...
start KeyboardAutomation.exe

echo ✅ 应用程序已启动
echo 如果遇到权限问题，请查看使用指南.md
pause
'''
        
        script_path = release_dir / "启动应用.bat"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
    
    else:
        # Linux启动脚本
        script_content = '''#!/bin/bash
# Linux 启动脚本

echo "启动键盘自动化软件..."
echo "如果是首次运行，请按照提示设置权限"
echo ""

# 检查可执行文件是否存在
if [ ! -f "KeyboardAutomation" ]; then
    echo "❌ 未找到 KeyboardAutomation"
    echo "请确保在正确的目录中运行此脚本"
    exit 1
fi

# 设置执行权限
chmod +x KeyboardAutomation

# 启动应用程序
./KeyboardAutomation

echo "✅ 应用程序已启动"
echo "如果遇到权限问题，请查看使用指南.md"
'''
        
        script_path = release_dir / "启动应用.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)


def create_install_readme(release_dir, system, version):
    """创建安装说明"""
    if system == "darwin":
        readme_content = f"""# 键盘自动化软件 v{version} - macOS版

## 🚀 快速开始

### 1. 安装
1. 解压下载的文件
2. 将 `KeyboardAutomation.app` 拖拽到应用程序文件夹（可选）

### 2. 运行
- 双击 `KeyboardAutomation.app` 启动
- 或运行 `启动应用.sh` 脚本

### 3. 权限设置（重要）
首次运行需要设置辅助功能权限：

1. 打开"系统偏好设置" > "安全性与隐私" > "隐私"
2. 选择左侧的"辅助功能"
3. 点击锁图标，输入管理员密码
4. 点击"+"添加 KeyboardAutomation.app
5. 确保勾选了对应的复选框

## ⚠️ 注意事项
- 需要 macOS 10.13 或更高版本
- 首次运行可能显示"无法验证开发者"，请在系统偏好设置中允许
- 如果遇到问题，请查看"使用指南.md"

## 📞 技术支持
如有问题，请查看使用指南或联系技术支持。
"""

    elif system == "windows":
        readme_content = f"""# 键盘自动化软件 v{version} - Windows版

## 🚀 快速开始

### 1. 安装
1. 解压下载的文件到任意目录
2. 建议创建桌面快捷方式

### 2. 运行
- 双击 `KeyboardAutomation.exe` 启动
- 或运行 `启动应用.bat` 脚本
- 建议以管理员身份运行

### 3. 权限设置
- Windows可能显示安全警告，选择"仍要运行"
- 杀毒软件可能误报，请添加到白名单
- 防火墙可能询问网络访问，可以拒绝（本软件不需要网络）

## ⚠️ 注意事项
- 需要 Windows 7 或更高版本
- 某些杀毒软件可能误报为恶意软件
- 如果被阻止运行，请检查Windows Defender设置
- 建议在首次运行前临时关闭实时保护

## 🛡️ 安全说明
本软件是开源的键盘自动化工具，不包含任何恶意代码。
杀毒软件的误报是因为软件具有键盘控制功能。

## 📞 技术支持
如有问题，请查看使用指南或联系技术支持。
"""

    else:
        readme_content = f"""# 键盘自动化软件 v{version} - Linux版

## 🚀 快速开始

### 1. 安装
1. 解压下载的文件到任意目录
2. 确保系统已安装必要的依赖

### 2. 系统依赖
```bash
# Ubuntu/Debian
sudo apt install python3-tk python3-dev libx11-dev

# CentOS/RHEL
sudo yum install tkinter python3-devel libX11-devel

# Arch Linux
sudo pacman -S tk python libx11
```

### 3. 运行
```bash
# 设置执行权限
chmod +x KeyboardAutomation

# 运行应用程序
./KeyboardAutomation

# 或使用启动脚本
./启动应用.sh
```

### 4. 权限设置
- 确保运行在X11环境（不支持Wayland）
- 检查DISPLAY环境变量
- 可能需要将用户添加到input组

## ⚠️ 注意事项
- 需要X11显示服务器
- 不支持Wayland（可以在Wayland下使用XWayland）
- 某些发行版可能需要额外配置

## 📞 技术支持
如有问题，请查看使用指南或联系技术支持。
"""

    readme_path = release_dir / "安装说明.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)


def create_zip_archive(source_dir, archive_path):
    """创建ZIP压缩包"""
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, source_dir.parent)
                zipf.write(file_path, arc_name)


def create_tar_archive(source_dir, archive_path):
    """创建TAR.GZ压缩包"""
    import tarfile
    with tarfile.open(archive_path, 'w:gz') as tarf:
        tarf.add(source_dir, arcname=source_dir.name)


def main():
    """主函数"""
    print("Keyboard Automation Software - Release Package Creation Tool")
    print("=" * 40)

    # 检查是否已打包
    if not Path("dist").exists():
        print("dist directory not found")
        print("Please run build script first: python3 build_app.py")
        return False
    
    # 创建发布包
    if create_release_package():
        print("\nRelease package created successfully!")
        print("You can distribute the archive to users.")
        return True
    else:
        print("\nRelease package creation failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
