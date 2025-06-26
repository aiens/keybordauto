#!/usr/bin/env python3
"""
GitHub Actions配置测试脚本
模拟CI环境进行本地测试
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def simulate_ci_environment():
    """模拟CI环境变量"""
    os.environ['CI'] = 'true'
    os.environ['GITHUB_ACTIONS'] = 'true'
    os.environ['RUNNER_OS'] = platform.system()
    print(f"✓ 模拟CI环境: {platform.system()}")


def test_python_setup():
    """测试Python环境"""
    print("🐍 测试Python环境...")
    
    # 检查Python版本
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 8:
        print("❌ Python版本过低，需要3.8+")
        return False
    
    print("✓ Python版本符合要求")
    return True


def test_dependencies():
    """测试依赖安装"""
    print("📦 测试依赖安装...")
    
    try:
        # 测试requirements.txt
        if not Path('requirements.txt').exists():
            print("❌ 未找到requirements.txt")
            return False
        
        # 尝试安装依赖
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 依赖安装失败")
            print(result.stderr)
            return False
        
        print("✓ 依赖安装成功")
        return True
        
    except Exception as e:
        print(f"❌ 依赖测试失败: {e}")
        return False


def test_icon_creation():
    """测试图标创建"""
    print("🎨 测试图标创建...")
    
    try:
        result = subprocess.run([
            sys.executable, 'create_icon.py'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 图标创建失败")
            print(result.stderr)
            return False
        
        # 检查图标文件
        assets_dir = Path('assets')
        if not assets_dir.exists():
            print("❌ assets目录未创建")
            return False
        
        icon_files = list(assets_dir.glob('icon.*'))
        if not icon_files:
            print("❌ 未找到图标文件")
            return False
        
        print(f"✓ 图标创建成功: {[f.name for f in icon_files]}")
        return True
        
    except Exception as e:
        print(f"❌ 图标创建测试失败: {e}")
        return False


def test_build_process():
    """测试构建过程"""
    print("🔨 测试构建过程...")
    
    try:
        # 设置虚拟显示器（Linux）
        if platform.system() == 'Linux':
            print("设置虚拟显示器...")
            os.environ['DISPLAY'] = ':99'
            # 注意：这里不启动Xvfb，因为可能没有安装
        
        result = subprocess.run([
            sys.executable, 'build_app.py'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 构建失败")
            print("STDERR:", result.stderr)
            print("STDOUT:", result.stdout)
            return False
        
        # 检查输出文件
        dist_dir = Path('dist')
        if not dist_dir.exists():
            print("❌ dist目录未创建")
            return False
        
        output_files = list(dist_dir.iterdir())
        if not output_files:
            print("❌ 未找到构建输出")
            return False
        
        print(f"✓ 构建成功: {[f.name for f in output_files]}")
        return True
        
    except Exception as e:
        print(f"❌ 构建测试失败: {e}")
        return False


def test_release_creation():
    """测试发布包创建"""
    print("📦 测试发布包创建...")
    
    try:
        result = subprocess.run([
            sys.executable, 'create_release.py'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 发布包创建失败")
            print(result.stderr)
            return False
        
        # 检查发布包
        releases_dir = Path('releases')
        if not releases_dir.exists():
            print("❌ releases目录未创建")
            return False
        
        release_files = list(releases_dir.glob('*.tar.gz')) + list(releases_dir.glob('*.zip'))
        if not release_files:
            print("❌ 未找到发布包文件")
            return False
        
        print(f"✓ 发布包创建成功: {[f.name for f in release_files]}")
        return True
        
    except Exception as e:
        print(f"❌ 发布包创建测试失败: {e}")
        return False


def test_yaml_syntax():
    """测试YAML文件语法"""
    print("📄 测试YAML文件语法...")
    
    try:
        import yaml
    except ImportError:
        print("⚠️ 未安装PyYAML，跳过YAML语法检查")
        return True
    
    yaml_files = [
        '.github/workflows/build.yml',
        '.github/workflows/build-simple.yml'
    ]
    
    for yaml_file in yaml_files:
        if not Path(yaml_file).exists():
            print(f"⚠️ 未找到 {yaml_file}")
            continue
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"✓ {yaml_file} 语法正确")
        except yaml.YAMLError as e:
            print(f"❌ {yaml_file} 语法错误: {e}")
            return False
    
    return True


def cleanup_test_files():
    """清理测试文件"""
    print("🧹 清理测试文件...")
    
    cleanup_dirs = ['build', 'dist', '__pycache__']
    for dir_name in cleanup_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"✓ 已清理 {dir_name}")


def main():
    """主测试函数"""
    print("🧪 GitHub Actions配置测试")
    print("=" * 50)
    
    # 模拟CI环境
    simulate_ci_environment()
    
    # 运行测试
    tests = [
        ("Python环境", test_python_setup),
        ("YAML语法", test_yaml_syntax),
        ("依赖安装", test_dependencies),
        ("图标创建", test_icon_creation),
        ("构建过程", test_build_process),
        ("发布包创建", test_release_creation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                failed += 1
                print(f"❌ {test_name} 失败")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} 异常: {e}")
    
    # 清理
    cleanup_test_files()
    
    # 总结
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有测试通过！GitHub Actions配置应该可以正常工作")
        print("\n📋 下一步:")
        print("1. 将代码推送到GitHub仓库")
        print("2. 检查Actions页面的构建状态")
        print("3. 在Releases页面下载构建好的文件")
    else:
        print("⚠️ 有测试失败，请检查配置")
        print("\n🔧 建议:")
        print("1. 检查失败的测试项")
        print("2. 修复相关问题")
        print("3. 重新运行测试")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
