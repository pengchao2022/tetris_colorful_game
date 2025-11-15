import random

# 直接定义常量，避免导入问题
SHAPES = [
    [[1, 1, 1, 1]],                                   # I
    [[1, 0, 0], [1, 1, 1]],                          # J
    [[0, 0, 1], [1, 1, 1]],                          # L
    [[1, 1], [1, 1]],                                # O
    [[0, 1, 1], [1, 1, 0]],                          # S
    [[0, 1, 0], [1, 1, 1]],                          # T
    [[1, 1, 0], [0, 1, 1]]                           # Z
]

COLORS = [
    (0, 255, 255),   # I - 青色
    (0, 0, 255),     # J - 蓝色
    (255, 165, 0),   # L - 橙色
    (255, 255, 0),   # O - 黄色
    (0, 255, 0),     # S - 绿色
    (128, 0, 128),   # T - 紫色
    (255, 0, 0),     # Z - 红色
]

GRID_WIDTH = 10

class Tetromino:
    def __init__(self, x=None, y=None, shape=None):
        if shape is None:
            self.shape_index = random.randint(0, len(SHAPES) - 1)
        else:
            self.shape_index = shape
        
        self.shape = SHAPES[self.shape_index]
        self.color = COLORS[self.shape_index]
        
        # 初始位置在顶部中间
        if x is None:
            x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        if y is None:
            y = 0
            
        self.x = x
        self.y = y
    
    def rotate(self):
        """旋转方块"""
        # 转置矩阵然后反转每一行
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[self.shape[rows-1-y][x] for y in range(rows)] for x in range(cols)]
        
        return rotated
    
    def get_rotated(self):
        """获取旋转后的形状（不改变当前状态）"""
        return self.rotate()
    
    def get_blocks(self):
        """获取方块所有格子的位置"""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks