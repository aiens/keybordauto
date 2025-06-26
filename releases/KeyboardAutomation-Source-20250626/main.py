#!/usr/bin/env python3
"""
键盘自动化软件主程序
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from keyboard_automation import KeyboardGUI, check_and_request_permissions


def main():
    """主函数"""
    try:
        import os

        # 检查是否在应用包中运行
        is_app_bundle = os.environ.get('RESOURCEPATH') is not None

        if not is_app_bundle:
            print("正在检查系统权限...")

        # 检查并请求权限（在应用包中静默处理）
        if not check_and_request_permissions():
            if not is_app_bundle:
                print("用户取消或权限检查失败，程序退出")
            return

        if not is_app_bundle:
            print("权限检查通过，启动应用程序...")

        # 创建并运行GUI
        app = KeyboardGUI()
        app.run()
    except KeyboardInterrupt:
        if not os.environ.get('RESOURCEPATH'):
            print("\n程序被用户中断")
    except Exception as e:
        # 在应用包中，将错误写入日志文件
        if os.environ.get('RESOURCEPATH'):
            try:
                log_path = os.path.expanduser("~/Library/Logs/KeyboardAutomation.log")
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
