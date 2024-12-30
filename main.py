import tkinter as tk
import random

# 定义方块的形状和颜色
BLOCKS = [
    {'shape': [[1, 1, 1, 1]], 'color': 'cyan'},  # I形
    {'shape': [[1, 1], [1, 1]], 'color': 'yellow'},  # O形
    {'shape': [[1, 1, 0], [0, 1, 1]], 'color': 'green'},  # S形
    {'shape': [[0, 1, 1], [1, 1, 0]], 'color': 'red'},  # Z形
    {'shape': [[1, 1, 1], [0, 1, 0]], 'color': 'blue'},  # T形
    {'shape': [[1, 0, 0], [1, 1, 1]], 'color': 'orange'},  # L形
    {'shape': [[0, 0, 1], [1, 1, 1]], 'color': 'purple'}  # J形
]

# 游戏设置
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right'
MOVE_DOWN = 'down'
MOVE_ROTATE = 'rotate'

LINE_CLEAR_SCORE = {1: 40, 2: 100, 3: 300, 4: 1200}  # 消除行的分数


class TetrisGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris")
        self.canvas = tk.Canvas(self, width=300, height=600, bg='black')
        self.canvas.pack()

        # 游戏初始化
        self.width = 10
        self.height = 20
        self.block_size = 30
        self.field = [[0] * self.width for _ in range(self.height)]
        self.score = 0
        self.game_over_flag = False
        self.current_block = None
        self.next_block = None

        # 启动游戏
        self.spawn_new_block()
        self.update_display()

        # 设置下落速度
        self.after(500, self.drop_block)

    def spawn_new_block(self):
        """生成新方块"""
        self.current_block = self.next_block or random.choice(BLOCKS)
        self.next_block = random.choice(BLOCKS)
        self.current_block['x'] = self.width // 2 - len(self.current_block['shape'][0]) // 2
        self.current_block['y'] = 0

    def update_display(self):
        """更新画布显示"""
        self.canvas.delete('all')

        # 绘制场地
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x] != 0:
                    self.canvas.create_rectangle(x * self.block_size, y * self.block_size,
                                                 (x + 1) * self.block_size, (y + 1) * self.block_size,
                                                 fill=self.field[y][x], outline='black')

        # 绘制当前方块
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = (self.current_block['x'] + c) * self.block_size
                    y = (self.current_block['y'] + r) * self.block_size
                    self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size,
                                                 fill=self.current_block['color'], outline='black')

        # 更新分数
        self.title(f"Tetris - Score: {self.score}")

    def can_move(self, direction):
        """检查方块是否可以移动"""
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.current_block['x'] + c
                    y = self.current_block['y'] + r
                    if direction == MOVE_LEFT:
                        if x <= 0 or self.field[y][x - 1] != 0:
                            return False
                    elif direction == MOVE_RIGHT:
                        if x >= self.width - 1 or self.field[y][x + 1] != 0:
                            return False
                    elif direction == MOVE_DOWN:
                        if y >= self.height - 1 or self.field[y + 1][x] != 0:
                            return False
        return True

    def rotate_block(self):
        """旋转方块"""
        rotated_shape = [list(row) for row in zip(*self.current_block['shape'][::-1])]
        original_shape = self.current_block['shape']
        self.current_block['shape'] = rotated_shape

        if not self.can_move(MOVE_LEFT) and not self.can_move(MOVE_RIGHT):
            self.current_block['shape'] = original_shape  # 恢复旋转前的状态
        else:
            self.update_display()

    def lock_block(self):
        """锁定方块并生成新方块"""
        for r, row in enumerate(self.current_block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.current_block['x'] + c
                    y = self.current_block['y'] + r
                    self.field[y][x] = self.current_block['color']
        self.clear_lines()
        self.spawn_new_block()

    def clear_lines(self):
        """清除满行并计算分数"""
        lines_to_clear = []
        for i, row in enumerate(self.field):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)

        for line in lines_to_clear:
            self.field.pop(line)
            self.field.insert(0, [0] * self.width)

        self.score += LINE_CLEAR_SCORE[len(lines_to_clear)]

    def drop_block(self):
        """控制方块下落"""
        if not self.game_over_flag:
            if self.can_move(MOVE_DOWN):
                self.current_block['y'] += 1
            else:
                self.lock_block()

            self.update_display()
            if not self.game_over_flag:
                self.after(500, self.drop_block)

    def game_over(self):
        """游戏结束"""
        self.game_over_flag = True
        self.canvas.create_text(self.width * self.block_size // 2, self.height * self.block_size // 2,
                                text="Game Over", fill="red", font=('Arial', 24))

    def on_key_press(self, event):
        """按键事件处理"""
        if self.game_over_flag:
            return

        if event.keysym == 'Left':
            if self.can_move(MOVE_LEFT):
                self.current_block['x'] -= 1
            self.update_display()
        elif event.keysym == 'Right':
            if self.can_move(MOVE_RIGHT):
                self.current_block['x'] += 1
            self.update_display()
        elif event.keysym == 'Down':
            if self.can_move(MOVE_DOWN):
                self.current_block['y'] += 1
            self.update_display()
        elif event.keysym == 'Up':
            self.rotate_block()
        elif event.keysym == 'space':
            self.drop_block()

if __name__ == '__main__':
    game = TetrisGame()
    game.bind("<Left>", game.on_key_press)
    game.bind("<Right>", game.on_key_press)
    game.bind("<Down>", game.on_key_press)
    game.bind("<Up>", game.on_key_press)
    game.bind("<space>", game.on_key_press)
    game.mainloop()
