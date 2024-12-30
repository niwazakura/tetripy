import pygame
import time
import tkinter as tk
import random

# 游戏参数
BLOCK_SIZE = 30
WIDTH = 10
HEIGHT = 20
LINE_CLEAR_SCORE = {1: 100, 2: 300, 3: 500, 4: 800}

MOVE_LEFT = (-1, 0)
MOVE_RIGHT = (1, 0)
MOVE_DOWN = (0, 1)

class TetrisGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris Game")
        
        # 游戏状态
        self.game_over_flag = False
        self.score = 0
        
        # 游戏场地
        self.width = WIDTH
        self.height = HEIGHT
        self.field = [[0] * self.width for _ in range(self.height)]
        
        # 当前方块
        self.current_block = None
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, width=self.width * BLOCK_SIZE, height=self.height * BLOCK_SIZE)
        self.canvas.pack()
        
        # 绑定按键事件
        self.root.bind("<KeyPress>", self.on_key_press)
        
        # 启动游戏
        self.new_block()
        self.drop_block()
        self.root.after(500, self.game_loop)  # 启动游戏循环
        self.root.mainloop()

    def game_loop(self):
        """每隔一定时间自动下落"""
        if not self.game_over_flag:
            self.drop_block()
            self.root.after(max(100, 500 - self.score // 10), self.game_loop)  # 根据分数逐渐加速

    def new_block(self):
        """生成新的方块"""
        shapes = [
            [[1, 1, 1, 1]],  # I形
            [[1, 1], [1, 1]],  # O形
            [[0, 1, 0], [1, 1, 1]],  # T形
            [[1, 1, 0], [0, 1, 1]],  # S形
            [[0, 1, 1], [1, 1, 0]],  # Z形
            [[1, 0, 0], [1, 1, 1]],  # L形
            [[0, 0, 1], [1, 1, 1]]   # J形
        ]
        shape = random.choice(shapes)
        color = random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'cyan', 'orange'])
        self.current_block = {
            'shape': shape,
            'color': color,
            'x': self.width // 2 - len(shape[0]) // 2,
            'y': 0
        }

    def can_move(self, direction):
        """检查是否可以移动方块"""
        dx, dy = direction
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.current_block['x'] + c + dx
                    y = self.current_block['y'] + r + dy
                    if x < 0 or x >= self.width or y >= self.height or self.field[y][x] != 0:
                        return False
        return True

    def move_block(self, direction):
        """移动方块"""
        if self.can_move(direction):
            dx, dy = direction
            self.current_block['x'] += dx
            self.current_block['y'] += dy
            self.update_display()

    def lock_block(self):
        """锁定当前方块"""
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    self.field[self.current_block['y'] + r][self.current_block['x'] + c] = self.current_block['color']
        self.clear_lines()
        self.new_block()

    def clear_lines(self):
        """清除已满的行"""
        lines_to_clear = []
        for y in range(self.height):
            if all(self.field[y]):
                lines_to_clear.append(y)

        if lines_to_clear:
            for line in lines_to_clear:
                self.field.pop(line)
                self.field.insert(0, [0] * self.width)

            self.score += LINE_CLEAR_SCORE[len(lines_to_clear)]
            self.root.title("Tetris Game：SCORES: %s"  % self.score)
        
        self.update_display()

    def update_display(self):
        """更新界面"""
        self.canvas.delete("all")
        self.draw_grid()

        # 绘制场地
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x]:
                    color = self.field[y][x]
                    self.canvas.create_rectangle(
                        x * BLOCK_SIZE, y * BLOCK_SIZE,
                        (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                        outline='gray', width=1, fill=color
                    )

        # 绘制当前方块
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.current_block['x'] + c
                    y = self.current_block['y'] + r
                    color = self.current_block['color']
                    self.canvas.create_rectangle(
                        x * BLOCK_SIZE, y * BLOCK_SIZE,
                        (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                        outline='gray', width=1, fill=color
                    )

    def draw_grid(self):
        """绘制背景网格"""
        for y in range(self.height):
            for x in range(self.width):
                color = 'light gray' if (x + y) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    x * BLOCK_SIZE, y * BLOCK_SIZE,
                    (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                    outline='gray', width=1, fill=color
                )

    def on_key_press(self, event):
        """处理键盘输入"""
        if event.keysym == 'Left':
            self.move_block(MOVE_LEFT)
        elif event.keysym == 'Right':
            self.move_block(MOVE_RIGHT)
        elif event.keysym == 'Down':
            self.drop_block()
        elif event.keysym == 'Up':
            self.rotate_block()
        elif event.keysym == 'space':
            self.drop_block_immediately()

    def rotate_block(self):
        """旋转方块"""
        if not self.game_over_flag:
            old_shape = self.current_block['shape']
            self.current_block['shape'] = [list(row) for row in zip(*self.current_block['shape'][::-1])]
            if not self.can_move(MOVE_DOWN) and not self.can_move(MOVE_LEFT) and not self.can_move(MOVE_RIGHT):
                self.current_block['shape'] = old_shape
            self.update_display()

    def drop_block(self):
        """控制方块下落"""
        if not self.game_over_flag:
            if self.can_move(MOVE_DOWN):
                self.current_block['y'] += 1
            else:
                self.lock_block()
            self.update_display()

    def drop_block_immediately(self):
        """立即将方块下落到底部"""
        while self.can_move(MOVE_DOWN):
            self.current_block['y'] += 1
        self.lock_block()
        self.update_display()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()


    pygame.mixer_music.load("https://cdn.freesound.org/previews/779/779827_5674468-lq.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer .music.play(-1)
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    win. Fill((0,0,0))
    draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
    pygame.display.update()
    time.sleep(2)
    pygame.display.quit()
    TetrisGame()
