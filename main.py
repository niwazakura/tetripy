import pygame
import time
import tkinter as tk
import random

# 游戏参数
BLOCK_SIZE = 30
WIDTH = 10
HEIGHT = 20
LINE_CLEAR_SCORE = {1: 100, 2: 300, 3: 500, 4: 800}

s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block

MOVE_LEFT = (-1, 0)
MOVE_RIGHT = (1, 0)
MOVE_DOWN = (0, 1)

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("sans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block

# Define colors for each block type
BLOCK_COLORS = {
    "I": "light blue",  # 淡蓝
    "J": "dark blue",   # 深蓝
    "L": "orange",      # 橙色
    "O": "yellow",      # 黄色
    "S": "green",       # 绿色
    "Z": "red",         # 红色
    "T": "purple"       # 紫色
}

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
        self.block_size = 30  # 每个方块的大小

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
            {"shape": [[1, 1, 1, 1]], "type": "I"},  # I形
            {"shape": [[1, 1], [1, 1]], "type": "O"},  # O形
            {"shape": [[0, 1, 0], [1, 1, 1]], "type": "T"},  # T形
            {"shape": [[1, 1, 0], [0, 1, 1]], "type": "S"},  # S形
            {"shape": [[0, 1, 1], [1, 1, 0]], "type": "Z"},  # Z形
            {"shape": [[1, 0, 0], [1, 1, 1]], "type": "L"},  # L形
            {"shape": [[0, 0, 1], [1, 1, 1]], "type": "J"}   # J形
        ]
        block = random.choice(shapes)
        shape = block["shape"]
        block_type = block["type"]
        color = BLOCK_COLORS[block_type]  # Get the color based on the block type
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

    def check_game_over(self):
        """检查游戏是否结束"""
        for c in range(self.width):
            if self.field[0][c] != 0:
                return True
        return False

    def game_over(self):
        """游戏结束处理"""
        self.game_over_flag = True
        self.canvas.create_text(self.width * self.block_size / 2, self.height * self.block_size / 2,
                                text="Game Over", fill="red", font=('Arial', 24))

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
            self.root.title("SCORES:%s"  % self.score)
        
        self.update_display()

    def update_display(self):
        """更新界面"""
        self.canvas.delete("all")
        self.draw_grid()
        if self.check_game_over():
            self.game_over()

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
    pygame.font.init()
    # pygame.mixer.init()
    # pygame.mixer_music.load("https://cdn.freesound.org/previews/779/779827_5674468-lq.mp3&#34;)  
    # pygame.mixer.music.set_volume(0.3)
    # pygame.mixer .music.play(-1)
    win = pygame.display.set_mode((s_width, HEIGHT * s_height))
    pygame.display.set_caption('Tetris')
    win.fill((0,0,0))
    draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
    pygame.display.update()
    time.sleep(2)
    pygame.display.quit()
    TetrisGame()
