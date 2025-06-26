#!/usr/bin/env python3
"""
键盘自动化软件主程序 - 简化版
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_automation import KeyboardGUI


def main():
    """主函数"""
    try:
        # 直接启动GUI，不进行复杂的权限检查
        app = KeyboardGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        # 在应用包中，将错误写入日志文件
        if os.environ.get('RESOURCEPATH'):
            try:
                log_path = os.path.expanduser("~/Library/Logs/KeyboardAutomation.log")
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, 'a', encoding='utf-8') as f:
                    import traceback
                    from datetime import datetime
                    f.write(f"\n{datetime.now()}: {e}\n")
                    f.write(traceback.format_exc())
            except:
                pass
        else:
            print(f"程序运行出错: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
