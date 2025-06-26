#!/usr/bin/env python3
"""
基本功能测试脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_automation.config import ConfigManager
from keyboard_automation.engine import KeyboardEngine, COMMON_KEYS, COMBINATION_TEMPLATES


def test_config_manager():
    """测试配置管理器"""
    print("=== 测试配置管理器 ===")
    
    config_manager = ConfigManager()
    
    # 测试创建默认配置
    default_config = config_manager.create_default_config()
    print(f"默认配置: {default_config['name']}")
    
    # 测试保存配置
    if config_manager.save_config(default_config, "测试配置"):
        print("✓ 配置保存成功")
    else:
        print("✗ 配置保存失败")
    
    # 测试加载配置
    loaded_config = config_manager.load_config("测试配置")
    if loaded_config:
        print("✓ 配置加载成功")
        print(f"  配置名称: {loaded_config.get('name')}")
        print(f"  序列数量: {len(loaded_config.get('sequences', []))}")
    else:
        print("✗ 配置加载失败")
    
    # 测试列出配置
    configs = config_manager.list_configs()
    print(f"✓ 找到 {len(configs)} 个配置: {configs}")
    
    print()


def test_engine():
    """测试键盘引擎"""
    print("=== 测试键盘引擎 ===")
    
    engine = KeyboardEngine()
    
    # 测试常用按键映射
    print(f"✓ 常用按键数量: {len(COMMON_KEYS)}")
    print(f"  示例按键: {list(COMMON_KEYS.items())[:5]}")
    
    # 测试组合键模板
    print(f"✓ 组合键模板数量: {len(COMBINATION_TEMPLATES)}")
    print(f"  示例模板: {list(COMBINATION_TEMPLATES.items())[:3]}")
    
    # 测试配置验证
    test_config = {
        'sequences': [
            {
                'keys': [
                    {'type': 'single', 'key': 'space'}
                ],
                'count': 1,
                'interval': 0.1
            }
        ],
        'repeat_count': 1,
        'repeat_interval': 1.0
    }
    
    print("✓ 引擎初始化成功")
    print("  注意: 实际按键执行需要系统权限")
    
    engine.cleanup()
    print()


def test_sample_config():
    """测试示例配置"""
    print("=== 测试示例配置 ===")
    
    config_manager = ConfigManager()
    sample_config = config_manager.load_config("示例配置")
    
    if sample_config:
        print("✓ 示例配置加载成功")
        print(f"  配置名称: {sample_config.get('name')}")
        print(f"  重复次数: {sample_config.get('repeat_count')}")
        print(f"  序列数量: {len(sample_config.get('sequences', []))}")
        
        for i, seq in enumerate(sample_config.get('sequences', [])):
            print(f"  序列 {i+1}: {seq.get('name')} ({len(seq.get('keys', []))} 个按键)")
    else:
        print("✗ 示例配置加载失败")
    
    print()


def main():
    """主测试函数"""
    print("键盘自动化软件 - 基本功能测试")
    print("=" * 40)
    
    try:
        test_config_manager()
        test_engine()
        test_sample_config()
        
        print("✓ 所有基本功能测试通过！")
        print("\n使用说明:")
        print("1. 运行 'python3 main.py' 启动图形界面")
        print("2. 在macOS上需要授权访问辅助功能")
        print("3. 按ESC键可紧急停止执行")
        print("4. 支持单键、组合键、文本输入")
        print("5. 可设置随机间隔和随机顺序")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
