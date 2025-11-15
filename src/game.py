import pygame
import os
import sys

# 直接定义所有常量
SCREEN_WIDTH = 320  # 保持宽度
SCREEN_HEIGHT = 700  # 保持高度
BLOCK_SIZE = 28     # 合适的方块尺寸
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 颜色定义 - 专业美观的配色
PURE_WHITE = (255, 255, 255)
LIGHT_GRAY = (248, 248, 248)
DARK_GRAY = (120, 120, 120)
BLACK = (50, 50, 50)  # 深灰色
ACCENT_BLUE = (80, 140, 240)  # 专业蓝色
ACCENT_RED = (230, 90, 90)    # 专业红色
ACCENT_GREEN = (70, 180, 70)  # 专业绿色

# 方块颜色 - 专业配色
COLORS = [
    (0, 200, 200),   # I - 青色
    (80, 120, 240),  # J - 蓝色
    (240, 160, 40),  # L - 橙色
    (220, 200, 40),  # O - 黄色
    (80, 200, 80),   # S - 绿色
    (170, 100, 200), # T - 紫色
    (220, 80, 80)    # Z - 红色
]

# 游戏设置
INITIAL_FALL_SPEED = 0.5
SPEED_INCREASE_PER_LEVEL = 0.05
FAST_DROP_MULTIPLIER = 10

# 直接导入其他类
try:
    from tetromino import Tetromino
    from board import Board
except ImportError:
    # 如果导入失败，说明是直接运行，添加路径
    import os
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from tetromino import Tetromino
    from board import Board

class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        
        # 初始化字体 - 使用中文字体，调小字体大小
        self._init_fonts()
        
        # 初始化游戏状态
        self.board = Board()
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.fall_time = 0
        self.fast_drop = False
        self.game_over = False
        self.paused = False
        
        # 初始化音效
        self.sound_enabled = True
        self._init_sounds()
    
    def _init_fonts(self):
        """初始化中文字体"""
        try:
            # 获取字体路径
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            font_path = os.path.join(base_path, 'assets', 'fonts', 'wqy-microhei-lite.ttc')
            
            if os.path.exists(font_path):
                # 使用中文字体，调小字体大小
                self.large_font = pygame.font.Font(font_path, 18)  # 从20调小到18
                self.medium_font = pygame.font.Font(font_path, 14)  # 从16调小到14
                self.small_font = pygame.font.Font(font_path, 12)   # 从14调小到12
                print("✅ 中文字体加载成功")
            else:
                print("⚠️ 中文字体文件未找到，使用默认字体")
                self.large_font = pygame.font.Font(None, 18)
                self.medium_font = pygame.font.Font(None, 14)
                self.small_font = pygame.font.Font(None, 12)
                
        except Exception as e:
            print(f"❌ 字体加载失败: {e}，使用默认字体")
            self.large_font = pygame.font.Font(None, 18)
            self.medium_font = pygame.font.Font(None, 14)
            self.small_font = pygame.font.Font(None, 12)
    
    def _init_sounds(self):
        """初始化音效"""
        try:
            # 获取资源路径
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # 使用您的 snowpanic.mp3 文件
            sound_path = os.path.join(base_path, 'assets', 'sounds', 'snowpanic.mp3')
            
            if os.path.exists(sound_path):
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)  # 循环播放
                print("✅ 背景音乐加载成功")
            else:
                print("⚠️ 背景音乐文件未找到")
                
        except Exception as e:
            print(f"❌ 音效加载失败: {e}")
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
    
    def toggle_pause(self):
        """切换暂停状态"""
        self.paused = not self.paused
    
    def get_fall_speed(self):
        """获取当前下落速度"""
        base_speed = max(0.05, INITIAL_FALL_SPEED - (self.board.level - 1) * SPEED_INCREASE_PER_LEVEL)
        return base_speed / FAST_DROP_MULTIPLIER if self.fast_drop else base_speed
    
    def handle_input(self):
        """处理用户输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_p:
                    self.toggle_pause()
                
                elif event.key == pygame.K_m:
                    self.toggle_sound()
                
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                if not self.game_over and not self.paused:
                    if event.key == pygame.K_LEFT:
                        if self.board.is_valid_position(self.current_piece, x_offset=-1):
                            self.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.board.is_valid_position(self.current_piece, x_offset=1):
                            self.current_piece.x += 1
                    elif event.key == pygame.K_DOWN:
                        self.fast_drop = True
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.hard_drop()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.fast_drop = False
        
        return True
    
    def rotate_piece(self):
        """旋转当前方块"""
        original_shape = self.current_piece.shape
        self.current_piece.shape = self.current_piece.get_rotated()
        
        # 如果旋转后位置无效，恢复原状
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.shape = original_shape
    
    def hard_drop(self):
        """硬降 - 直接落到底部"""
        distance = 0
        while self.board.is_valid_position(self.current_piece, y_offset=1):
            self.current_piece.y += 1
            distance += 1
        
        if distance > 0:
            self.board.add_hard_drop_score(distance)
            self.lock_piece()
    
    def lock_piece(self):
        """锁定当前方块并生成新方块"""
        self.board.place_tetromino(self.current_piece)
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        # 检查游戏是否结束
        if self.board.is_game_over(self.current_piece):
            self.game_over = True
    
    def update(self, delta_time):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        self.fall_time += delta_time
        fall_speed = self.get_fall_speed()
        
        if self.fall_time >= fall_speed:
            if self.board.is_valid_position(self.current_piece, y_offset=1):
                self.current_piece.y += 1
                if self.fast_drop:
                    self.board.add_soft_drop_score(1)
            else:
                self.lock_piece()
            self.fall_time = 0
    
    def draw(self):
        """绘制游戏界面"""
        # 绘制纯白色背景
        self.screen.fill(PURE_WHITE)
        
        # 绘制信息区域（在游戏区域上方）
        self.draw_info_area()
        
        # 计算游戏区域居中位置
        game_area_width = GRID_WIDTH * BLOCK_SIZE
        game_area_height = GRID_HEIGHT * BLOCK_SIZE
        game_area_x = (SCREEN_WIDTH - game_area_width) // 2  # 水平居中
        game_area_y = 120  # 信息区域下方
        
        # 绘制游戏区域背景 - 带圆角和阴影效果
        game_area_rect = pygame.Rect(game_area_x, game_area_y, game_area_width, game_area_height)
        pygame.draw.rect(self.screen, LIGHT_GRAY, game_area_rect, border_radius=8)
        pygame.draw.rect(self.screen, DARK_GRAY, game_area_rect, 2, border_radius=8)
        
        # 绘制已落下的方块
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board.grid[y][x]:
                    rect = pygame.Rect(
                        game_area_x + x * BLOCK_SIZE, 
                        game_area_y + y * BLOCK_SIZE, 
                        BLOCK_SIZE - 2, 
                        BLOCK_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, self.board.grid[y][x], rect, border_radius=3)
                    # 添加内阴影效果
                    pygame.draw.rect(self.screen, (255, 255, 255, 50), rect, 1, border_radius=3)
        
        # 绘制当前方块
        if not self.game_over:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            game_area_x + (self.current_piece.x + x) * BLOCK_SIZE,
                            game_area_y + (self.current_piece.y + y) * BLOCK_SIZE,
                            BLOCK_SIZE - 2,
                            BLOCK_SIZE - 2
                        )
                        pygame.draw.rect(self.screen, self.current_piece.color, rect, border_radius=3)
                        pygame.draw.rect(self.screen, (255, 255, 255, 100), rect, 1, border_radius=3)
        
        # 绘制网格线 - 细线
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, (200, 200, 200), 
                           (game_area_x + x * BLOCK_SIZE, game_area_y), 
                           (game_area_x + x * BLOCK_SIZE, game_area_y + GRID_HEIGHT * BLOCK_SIZE), 1)
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, (200, 200, 200),
                           (game_area_x, game_area_y + y * BLOCK_SIZE),
                           (game_area_x + GRID_WIDTH * BLOCK_SIZE, game_area_y + y * BLOCK_SIZE), 1)
        
        # 绘制游戏状态
        if self.paused:
            self.draw_pause_screen()
        elif self.game_over:
            self.draw_game_over_screen()
        
        pygame.display.flip()
    
    def draw_info_area(self):
        """绘制信息区域（在游戏区域上方）"""
        # 绘制下一个方块预览区域
        preview_rect = pygame.Rect(20, 20, 120, 80)  # 调小高度
        pygame.draw.rect(self.screen, LIGHT_GRAY, preview_rect, border_radius=6)
        pygame.draw.rect(self.screen, DARK_GRAY, preview_rect, 2, border_radius=6)
        
        # 绘制"下一个"标签 - 使用更小的字体
        next_text = self.medium_font.render("下一个方块", True, ACCENT_BLUE)
        self.screen.blit(next_text, (25, 5))
        
        # 绘制下一个方块 - 居中显示
        preview_x = 20 + 60 - (len(self.next_piece.shape[0]) * BLOCK_SIZE) // 2
        preview_y = 60 - (len(self.next_piece.shape) * BLOCK_SIZE) // 2  # 调整Y坐标
        
        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        preview_x + x * BLOCK_SIZE,
                        preview_y + y * BLOCK_SIZE,
                        BLOCK_SIZE - 2,
                        BLOCK_SIZE - 2
                    )
                    pygame.draw.rect(self.screen, self.next_piece.color, rect, border_radius=3)
                    pygame.draw.rect(self.screen, (255, 255, 255, 100), rect, 1, border_radius=3)
        
        # 绘制统计信息区域
        stats_rect = pygame.Rect(160, 20, 140, 80)  # 调小高度
        pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect, border_radius=6)
        pygame.draw.rect(self.screen, DARK_GRAY, stats_rect, 2, border_radius=6)
        
        # 绘制统计信息 - 使用更小的字体
        stats_title = self.medium_font.render("游戏统计", True, ACCENT_BLUE)
        self.screen.blit(stats_title, (165, 5))
        
        stats = [
            (f"分数: {self.board.score}", self.small_font),  # 使用small_font
            (f"等级: {self.board.level}", self.small_font),  # 使用small_font
            (f"消除: {self.board.total_lines}", self.small_font)  # 使用small_font
        ]
        
        for i, (text, font) in enumerate(stats):
            text_surface = font.render(text, True, BLACK)
            self.screen.blit(text_surface, (170, 25 + i * 20))  # 调整行间距
    
    def draw_pause_screen(self):
        """绘制暂停界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停提示框
        pause_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60, 200, 120)
        pygame.draw.rect(self.screen, LIGHT_GRAY, pause_rect, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_BLUE, pause_rect, 3, border_radius=10)
        
        pause_text = self.large_font.render("游戏暂停", True, ACCENT_BLUE)
        continue_text = self.small_font.render("按 P 键继续游戏", True, BLACK)
        
        pause_rect_pos = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        
        self.screen.blit(pause_text, pause_rect_pos)
        self.screen.blit(continue_text, continue_rect)
    
    def draw_game_over_screen(self):
        """绘制游戏结束界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束提示框
        game_over_rect = pygame.Rect(SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 80, 240, 160)
        pygame.draw.rect(self.screen, LIGHT_GRAY, game_over_rect, border_radius=10)
        pygame.draw.rect(self.screen, ACCENT_RED, game_over_rect, 3, border_radius=10)
        
        game_over_text = self.large_font.render("游戏结束", True, ACCENT_RED)
        score_text = self.medium_font.render(f"最终分数: {self.board.score}", True, BLACK)
        restart_text = self.small_font.render("按 R 键重新开始", True, BLACK)
        
        game_over_rect_pos = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        
        self.screen.blit(game_over_text, game_over_rect_pos)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        """重置游戏"""
        self.board.reset()
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.fall_time = 0
        self.fast_drop = False
        self.game_over = False
        self.paused = False
    
    def run(self):
        """运行游戏主循环"""
        last_time = pygame.time.get_ticks()
        
        while True:
            current_time = pygame.time.get_ticks()
            delta_time = (current_time - last_time) / 1000.0
            last_time = current_time
            
            if not self.handle_input():
                break
            
            self.update(delta_time)
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    # 支持直接运行 game.py
    print("🎮 俄罗斯方块游戏")
    print("=" * 40)
    print("游戏特色:")
    print("• 完整的得分统计系统")
    print("• 等级系统（消除行数越多速度越快）")
    print("• 下一个方块预览")
    print("• 背景音乐")
    print("• 中文字体支持")
    print("• 简洁的游戏界面")
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