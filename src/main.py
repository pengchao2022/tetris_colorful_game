#!/usr/bin/env python3
"""
俄罗斯方块游戏 - 主入口文件
"""

import os
import sys

# 添加 src 目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from game import TetrisGame

def main():
    print("🎮 俄罗斯方块游戏 - 专业版")
    print("=" * 40)
    print("游戏特色:")
    print("• 完整的得分统计系统")
    print("• 等级系统（消除行数越多速度越快）")
    print("• 下一个方块预览")
    print("• 背景音乐")
    print("• 中文字体支持")
    print("• 专业的游戏界面")
    print("=" * 40)
    print("游戏控制:")
    print("← → : 左右移动方块")
    print("↑ : 旋转方块")
    print("↓ : 快速下落（按住）")
    print("空格 : 硬降落（直接落到底部）")
    print("P : 暂停游戏")
    print("M : 开启/关闭音效")
    print("R : 重新开始游戏")
    print("ESC : 退出游戏")
    print("=" * 40)
    
    try:
        game = TetrisGame()
        game.run()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()