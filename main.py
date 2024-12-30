import tkinter as tk
import random

# 常量设置
WIDTH, HEIGHT = 10, 20  # 场地宽10，场地高20
BLOCK_SIZE = 30  # 方块大小
FIELD_COLOR = 'black'
GRID_COLOR = 'gray'
LINE_CLEAR_SCORE = {1: 100, 2: 300, 3: 500, 4: 800}  # 消行得分规则

# 形状和颜色绑定
BLOCKS = [
    {'shape': [['0000', '1111', '0000', '0000']], 'color': 'cyan'},  # I
    {'shape': [['0110', '1110', '0000', '0000']], 'color': 'blue'},  # J
    {'shape': [['1100', '1110', '0000', '0000']], 'color': 'orange'},  # L
    {'shape': [['1100', '1100']], 'color': 'yellow'},  # O
    {'shape': [['0110', '1110']], 'color': 'green'},  # S
    {'shape': [['1100', '0110']], 'color': 'red'},  # Z
    {'shape': [['0100', '1110', '0000', '0000']], 'color': 'purple'},  # T
]

class TetrisGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Tetris')
        self.canvas = tk.Canvas(master, width=WIDTH * BLOCK_SIZE, height=HEIGHT * BLOCK_SIZE)
        self.canvas.pack()
        self.score = 0
        self.game_over = False

        # 初始化场地
        self.field = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_block = None
        self.next_block = None
        self.update_display()

        # 绑定按键
        self.master.bind("<Left>", self.on_key_press)
        self.master.bind("<Right>", self.on_key_press)
        self.master.bind("<Down>", self.on_key_press)
        self.master.bind("<Up>", self.on_key_press)
        self.master.bind("<space>", self.on_key_press)

        # 启动游戏
        self.new_block()
        self.fall()

    def update_display(self):
        # 清空画布
        self.canvas.delete('all')

        # 绘制网格
        for row in range(HEIGHT):
            for col in range(WIDTH):
                x1, y1 = col * BLOCK_SIZE, row * BLOCK_SIZE
                x2, y2 = x1 + BLOCK_SIZE, y1 + BLOCK_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline=GRID_COLOR)

        # 绘制已经锁定的方块
        for r in range(HEIGHT):
            for c in range(WIDTH):
                if self.field[r][c]:
                    color = BLOCKS[self.field[r][c] - 1]['color']
                    x1, y1 = c * BLOCK_SIZE, r * BLOCK_SIZE
                    x2, y2 = x1 + BLOCK_SIZE, y1 + BLOCK_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=FIELD_COLOR)

        # 绘制当前方块
        if self.current_block:
            for r, row in enumerate(self.current_block['shape']):
                for c, cell in enumerate(row):
                    if cell:
                        color = self.current_block['color']
                        x1, y1 = (self.current_block['x'] + c) * BLOCK_SIZE, (self.current_block['y'] + r) * BLOCK_SIZE
                        x2, y2 = x1 + BLOCK_SIZE, y1 + BLOCK_SIZE
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=FIELD_COLOR)

        # 显示分数
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", anchor=tk.NW, fill='white', font=('Arial', 16))

    def new_block(self):
        # 从BLOCKS中随机选择形状和颜色
        block = random.choice(BLOCKS)
        self.current_block = {
            'shape': block['shape'],
            'color': block['color'],
            'x': WIDTH // 2 - 2,
            'y': 0,
        }
        self.next_block = random.choice(BLOCKS)

    def fall(self):
        if not self.game_over:
            if self.valid_move(self.current_block, 0, 1):
                self.current_block['y'] += 1
            else:
                self.lock_block()
                if self.game_over:
                    self.end_game()
                    return
                self.new_block()
            self.update_display()
            self.master.after(500, self.fall)

    def valid_move(self, block, dx, dy):
        for r, row in enumerate(block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = block['x'] + c + dx
                    y = block['y'] + r + dy
                    if x < 0 or x >= WIDTH or y >= HEIGHT or self.field[y][x]:
                        return False
        return True

    def lock_block(self):
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.current_block['x'] + c
                    y = self.current_block['y'] + r
                    self.field[y][x] = BLOCKS.index({'shape': self.current_block['shape'], 'color': self.current_block['color']}) + 1

        self.clear_lines()

    def clear_lines(self):
        lines_to_clear = []
        for i, row in enumerate(self.field):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)

        for i in lines_to_clear:
            del self.field[i]
            self.field.insert(0, [0] * WIDTH)

        self.score += LINE_CLEAR_SCORE.get(len(lines_to_clear), 0)

    def on_key_press(self, event):
        if self.game_over:
            return

        if event.keysym == 'Left':
            if self.valid_move(self.current_block, -1, 0):
                self.current_block['x'] -= 1
        elif event.keysym == 'Right':
            if self.valid_move(self.current_block, 1, 0):
                self.current_block['x'] += 1
        elif event.keysym == 'Down':
            if self.valid_move(self.current_block, 0, 1):
                self.current_block['y'] += 1
        elif event.keysym == 'Up':
            self.rotate_block()
        elif event.keysym == 'space':
            self.hard_drop()

        self.update_display()

    def rotate_block(self):
        shape = self.current_block['shape']
        self.current_block['shape'] = [list(x) for x in zip(*shape[::-1])]
        if not self.valid_move(self.current_block, 0, 0):
            self.current_block['shape'] = shape

    def hard_drop(self):
        while self.valid_move(self.current_block, 0, 1):
            self.current_block['y'] += 1
        self.lock_block()

    def end_game(self):
        self.canvas.create_text(WIDTH * BLOCK_SIZE // 2, HEIGHT * BLOCK_SIZE // 2,
                                text="Game Over", fill='red', font=('Arial', 24))
        self.game_over = True

def main():
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
