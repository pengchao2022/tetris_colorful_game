# 直接定义常量
GRID_WIDTH = 10
GRID_HEIGHT = 20

SCORE_SINGLE = 100      # 单行消除
SCORE_DOUBLE = 300      # 双行消除
SCORE_TRIPLE = 500      # 三行消除
SCORE_TETRIS = 800      # 四行消除

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.total_lines = 0
    
    def is_valid_position(self, tetromino, x_offset=0, y_offset=0):
        """检查位置是否有效"""
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = tetromino.x + x + x_offset
                    new_y = tetromino.y + y + y_offset
                    
                    # 检查边界
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    
                    # 检查碰撞（只检查网格内的位置）
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return False
        return True
    
    def place_tetromino(self, tetromino):
        """将方块放置到板上"""
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    board_y = tetromino.y + y
                    if board_y >= 0:  # 确保不在顶部之外
                        self.grid[board_y][tetromino.x + x] = tetromino.color
        
        # 检查并清除完整的行
        lines_cleared = self.clear_lines()
        
        # 更新统计信息
        self.update_stats(lines_cleared)
        
        return lines_cleared
    
    def clear_lines(self):
        """清除完整的行并返回清除的行数"""
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        # 从下往上清除行
        for line in sorted(lines_to_clear, reverse=True):
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        return len(lines_to_clear)
    
    def update_stats(self, lines_cleared):
        """更新分数和等级"""
        self.total_lines += lines_cleared
        
        # 根据消除行数计算得分
        if lines_cleared == 1:
            self.score += SCORE_SINGLE * self.level
        elif lines_cleared == 2:
            self.score += SCORE_DOUBLE * self.level
        elif lines_cleared == 3:
            self.score += SCORE_TRIPLE * self.level
        elif lines_cleared == 4:
            self.score += SCORE_TETRIS * self.level
        
        # 更新等级（每清除10行升一级）
        new_level = self.total_lines // 10 + 1
        if new_level > self.level:
            self.level = new_level
    
    def add_soft_drop_score(self, distance):
        """添加软降得分"""
        self.score += distance
    
    def add_hard_drop_score(self, distance):
        """添加硬降得分"""
        self.score += distance * 2
    
    def is_game_over(self, tetromino):
        """检查游戏是否结束"""
        return not self.is_valid_position(tetromino)
    
    def reset(self):
        """重置游戏板"""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.total_lines = 0