#!/usr/bin/env python3
"""
创建源代码包，用户可以在任何平台上自行打包
"""

import os
import shutil
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime


def create_source_package():
    """创建源代码包"""
    print("📦 创建跨平台源代码包")
    print("=" * 40)
    
    # 包名
    timestamp = datetime.now().strftime("%Y%m%d")
    package_name = f"KeyboardAutomation-Source-{timestamp}"
    package_dir = Path("releases") / package_name
    
    # 清理并创建目录
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # 要包含的文件和目录
    include_items = [
        # 源代码
        "main.py",
        "main_app.py", 
        "main_simple.py",
        "keyboard_automation/",
        
        # 配置和资源
        "configs/",
        "assets/",
        "requirements.txt",
        
        # 打包脚本
        "build_app.py",
        "create_icon.py",
        "create_release.py",
        "KeyboardAutomation.spec",
        
        # 平台特定脚本
        "build_macos.sh",
        "build_windows.bat", 
        "build_linux.sh",
        "cloud_build_setup.sh",
        
        # 文档
        "README.md",
        "使用指南.md",
        "打包说明.md",
        "跨平台打包说明.md",
        "应用包问题解决方案.md",
        
        # 测试脚本
        "test_basic.py",
    ]
    
    # 复制文件
    print("📁 复制源代码文件...")
    for item in include_items:
        src_path = Path(item)
        if src_path.exists():
            dst_path = package_dir / item
            
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
                print(f"✓ 已复制目录: {item}")
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                print(f"✓ 已复制文件: {item}")
        else:
            print(f"⚠️ 未找到: {item}")
    
    # 创建平台特定的快速启动脚本
    create_quick_start_scripts(package_dir)
    
    # 创建总体说明文件
    create_package_readme(package_dir)
    
    # 创建压缩包
    print("\n🗜️ 创建压缩包...")
    
    # ZIP格式（Windows友好）
    zip_path = f"releases/{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir.parent)
                zipf.write(file_path, arc_name)
    
    # TAR.GZ格式（Unix友好）
    tar_path = f"releases/{package_name}.tar.gz"
    with tarfile.open(tar_path, 'w:gz') as tarf:
        tarf.add(package_dir, arcname=package_name)
    
    print(f"✅ 源代码包创建完成！")
    print(f"📁 目录: {package_dir}")
    print(f"📦 ZIP包: {zip_path}")
    print(f"📦 TAR包: {tar_path}")
    
    return True


def create_quick_start_scripts(package_dir):
    """创建快速启动脚本"""
    print("🚀 创建快速启动脚本...")
    
    # Windows快速启动
    windows_script = '''@echo off
echo 键盘自动化软件 - Windows快速启动
echo ================================

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 安装依赖包...
pip install -r requirements.txt

echo 创建图标...
python create_icon.py

echo 构建应用程序...
python build_app.py

echo 创建发布包...
python create_release.py

echo ✅ 构建完成！
echo 可执行文件位于: dist\\KeyboardAutomation.exe
echo 发布包位于: releases\\

pause
'''
    
    with open(package_dir / "快速构建-Windows.bat", 'w', encoding='utf-8') as f:
        f.write(windows_script)
    
    # Linux/macOS快速启动
    unix_script = '''#!/bin/bash
echo "键盘自动化软件 - Unix快速启动"
echo "=============================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "安装依赖包..."
pip3 install -r requirements.txt

echo "创建图标..."
python3 create_icon.py

echo "构建应用程序..."
python3 build_app.py

echo "创建发布包..."
python3 create_release.py

echo "✅ 构建完成！"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "应用程序位于: dist/KeyboardAutomation.app"
else
    echo "可执行文件位于: dist/KeyboardAutomation"
fi
echo "发布包位于: releases/"
'''
    
    script_path = package_dir / "快速构建-Unix.sh"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(unix_script)
    
    # 设置执行权限
    os.chmod(script_path, 0o755)
    
    print("✓ 已创建快速启动脚本")


def create_package_readme(package_dir):
    """创建包说明文件"""
    readme_content = '''# 键盘自动化软件 - 源代码包

## 🚀 快速开始

### Windows用户
1. 双击运行 `快速构建-Windows.bat`
2. 等待构建完成
3. 运行 `dist/KeyboardAutomation.exe`

### macOS/Linux用户
1. 运行 `./快速构建-Unix.sh`
2. 等待构建完成
3. 运行生成的应用程序

## 📋 手动构建步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 创建图标
```bash
python create_icon.py
```

### 3. 构建应用
```bash
python build_app.py
```

### 4. 创建发布包
```bash
python create_release.py
```

## 🎯 输出文件

构建完成后，你将得到：
- `dist/` - 可执行文件目录
- `releases/` - 发布包目录

## 📚 详细文档

- `README.md` - 项目总体说明
- `使用指南.md` - 详细使用说明
- `打包说明.md` - 打包详细说明
- `跨平台打包说明.md` - 跨平台解决方案

## ⚠️ 注意事项

1. **Python版本**: 需要Python 3.8或更高版本
2. **系统权限**: 运行时需要设置辅助功能权限
3. **杀毒软件**: 可能需要添加到白名单

## 🆘 遇到问题？

1. 查看对应的文档文件
2. 检查Python和依赖包版本
3. 确认系统权限设置

---

**这是一个完整的源代码包，包含了所有必要的文件和脚本，可以在任何支持Python的平台上构建应用程序。**
'''
    
    with open(package_dir / "构建说明.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✓ 已创建包说明文件")


def main():
    """主函数"""
    print("键盘自动化软件 - 源代码包创建工具")
    print("=" * 50)
    
    if create_source_package():
        print("\n🎉 源代码包创建成功！")
        print("\n📋 使用说明:")
        print("1. 将压缩包发送给需要的用户")
        print("2. 用户解压后运行快速构建脚本")
        print("3. 或者按照构建说明.md手动构建")
        print("\n💡 这样用户可以在任何平台上自行打包exe、app等格式")
    else:
        print("\n❌ 源代码包创建失败")


if __name__ == "__main__":
    main()
