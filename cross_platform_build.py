#!/usr/bin/env python3
"""
跨平台打包脚本
使用不同的方法为各平台打包应用程序
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def build_with_github_actions():
    """使用GitHub Actions进行跨平台打包"""
    print("🚀 使用GitHub Actions进行跨平台打包")
    print("=" * 50)
    
    # 检查是否在Git仓库中
    if not Path('.git').exists():
        print("初始化Git仓库...")
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit'])
    
    print("📋 GitHub Actions设置步骤:")
    print("1. 将代码推送到GitHub仓库")
    print("2. GitHub Actions会自动为Windows、Linux、macOS打包")
    print("3. 在Actions页面下载打包好的文件")
    print("")
    print("推送命令:")
    print("git remote add origin <your-repo-url>")
    print("git push -u origin main")
    print("")
    print("✅ GitHub Actions配置文件已创建: .github/workflows/build.yml")


def build_with_docker():
    """使用Docker进行跨平台打包"""
    print("🐳 使用Docker进行跨平台打包")
    print("=" * 50)
    
    # 检查Docker是否安装
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker未安装，请先安装Docker")
        return False
    
    print("构建Linux版本...")
    try:
        # 构建Linux版本
        subprocess.run([
            'docker', 'build', 
            '-f', 'Dockerfile.linux',
            '-t', 'keyboard-automation-linux',
            '.'
        ], check=True)
        
        # 运行容器并复制文件
        subprocess.run([
            'docker', 'run', '--rm',
            '-v', f'{os.getcwd()}/releases:/app/releases',
            'keyboard-automation-linux'
        ], check=True)
        
        print("✅ Linux版本构建完成")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Linux构建失败: {e}")
        return False
    
    print("📋 Windows版本需要Windows Docker容器支持")
    print("建议使用GitHub Actions或Windows虚拟机")
    
    return True


def build_with_wine():
    """使用Wine在macOS/Linux上构建Windows版本"""
    print("🍷 使用Wine构建Windows版本")
    print("=" * 50)
    
    # 检查Wine是否安装
    try:
        subprocess.run(['wine', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Wine未安装")
        print("安装Wine:")
        if platform.system() == 'Darwin':
            print("brew install wine")
        else:
            print("sudo apt install wine")
        return False
    
    print("⚠️  Wine方案较复杂，建议使用GitHub Actions")
    return False


def create_manual_instructions():
    """创建手动打包说明"""
    instructions = """
# 跨平台打包说明

## Windows打包步骤

### 在Windows系统上：
1. 安装Python 3.8+
2. 克隆项目代码
3. 运行以下命令：
```cmd
pip install -r requirements.txt
python create_icon.py
python build_app.py
python create_release.py
```

### 使用Windows虚拟机：
1. 下载Windows 10/11 ISO
2. 使用VirtualBox/VMware创建虚拟机
3. 在虚拟机中按上述步骤操作

## Linux打包步骤

### 在Linux系统上：
1. 安装依赖：
```bash
sudo apt install python3 python3-pip python3-tk python3-dev
```
2. 运行打包脚本：
```bash
pip3 install -r requirements.txt
python3 create_icon.py
python3 build_app.py
python3 create_release.py
```

### 使用Docker：
```bash
docker build -f Dockerfile.linux -t keyboard-automation-linux .
docker run --rm -v $(pwd)/releases:/app/releases keyboard-automation-linux
```

## 推荐方案排序

1. **GitHub Actions** (最推荐)
   - 自动化程度高
   - 支持所有平台
   - 无需本地环境

2. **云服务器**
   - 租用Windows/Linux云服务器
   - 远程桌面操作
   - 成本较低

3. **虚拟机**
   - 本地控制
   - 一次性设置
   - 占用本地资源

4. **朋友的电脑**
   - 借用Windows/Linux电脑
   - 快速简单
   - 需要人际关系 😄

## 文件分发

打包完成后，你将得到：
- `KeyboardAutomation-windows.zip` (Windows版本)
- `KeyboardAutomation-linux.tar.gz` (Linux版本)  
- `KeyboardAutomation-macos.tar.gz` (macOS版本)

每个包都包含：
- 可执行文件
- 配置示例
- 使用说明
- 启动脚本
"""
    
    with open('跨平台打包说明.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ 已创建详细的手动打包说明: 跨平台打包说明.md")


def main():
    """主函数"""
    print("键盘自动化软件 - 跨平台打包工具")
    print("=" * 50)
    
    current_platform = platform.system().lower()
    print(f"当前平台: {current_platform}")
    print("")
    
    print("可用的跨平台打包方案:")
    print("1. GitHub Actions (推荐)")
    print("2. Docker")
    print("3. 手动打包说明")
    print("4. 退出")
    print("")
    
    while True:
        choice = input("请选择方案 (1-4): ").strip()
        
        if choice == '1':
            build_with_github_actions()
            break
        elif choice == '2':
            build_with_docker()
            break
        elif choice == '3':
            create_manual_instructions()
            break
        elif choice == '4':
            print("退出")
            break
        else:
            print("无效选择，请输入1-4")
    
    print("")
    print("🎯 推荐使用GitHub Actions方案:")
    print("1. 将代码推送到GitHub")
    print("2. 自动为所有平台打包")
    print("3. 在Releases页面下载")
    print("")
    print("📞 如需帮助，请查看'跨平台打包说明.md'")


if __name__ == "__main__":
    main()
