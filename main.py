import tkinter as tk
import random

# 游戏常量
MOVE_LEFT = 'Left'
MOVE_RIGHT = 'Right'
MOVE_DOWN = 'Down'
ROTATE_CW = 'Up'
ROTATE_CCW = 'z'

LINE_CLEAR_SCORE = {
    1: 100,
    2: 300,
    3: 500,
    4: 800
}

# 方块形状及其颜色
BLOCK_SHAPES = [
    [['1111']],  # I型
    [['11', '11']],  # O型
    [['010', '111']],  # T型
    [['110', '011']],  # L型
    [['011', '110']],  # J型
    [['011', '110']],  # Z型
    [['110', '010']]   # S型
]

BLOCK_COLORS = ['cyan', 'yellow', 'purple', 'orange', 'blue', 'green', 'red']

def generate_block():
    """生成一个新的随机方块"""
    shape = random.choice(BLOCK_SHAPES)
    color = BLOCK_COLORS[BLOCK_SHAPES.index(shape)]
    return {'shape': shape, 'color': color, 'x': 0, 'y': 0}

class TetrisGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tetris')
        self.canvas = tk.Canvas(self, width=300, height=600, bg='black')
        self.canvas.pack()

        # 游戏区参数
        self.width = 10  # 游戏区宽度
        self.height = 20  # 游戏区高度
        self.block_size = 30  # 每个方块的大小
        self.field = [[0] * self.width for _ in range(self.height)]  # 初始化空场地
        self.block = None  # 当前方块
        self.score = 0  # 游戏得分
        self.game_over_flag = False  # 游戏结束标志
        self.gravity_speed = 500  # 下落速度（单位：毫秒）
        self.hard_drop_speed = 50  # 硬降速度（单位：毫秒）

        # 启动游戏
        self.update_display()
        self.spawn_block()
        self.after(self.gravity_speed, self.drop_block)  # 每500毫秒下落一次

    def spawn_block(self):
        """生成一个新的方块"""
        self.block = generate_block()
        self.block['x'] = self.width // 2 - len(self.block['shape'][0]) // 2
        self.block['y'] = 0

    def drop_block(self):
        """控制方块的自动下落"""
        if not self.game_over_flag:
            if not self.move_block(MOVE_DOWN):
                self.lock_block()
                self.clear_lines()
                self.spawn_block()  # 生成新的方块
                if self.check_game_over():
                    self.game_over()
                else:
                    self.update_display()
            self.after(self.gravity_speed, self.drop_block)  # 继续下落

    def move_block(self, direction):
        """移动当前方块"""
        if direction == MOVE_DOWN:
            if self.can_move_down():
                self.block['y'] += 1
                self.update_display()
                return True
            else:
                return False
        elif direction == MOVE_LEFT:
            if self.can_move_left():
                self.block['x'] -= 1
                self.update_display()
                return True
        elif direction == MOVE_RIGHT:
            if self.can_move_right():
                self.block['x'] += 1
                self.update_display()
                return True
        return False

    def hard_drop(self):
        """硬降：将方块迅速下落到底"""
        while self.move_block(MOVE_DOWN):
            pass
        self.lock_block()
        self.clear_lines()
        self.spawn_block()  # 生成新的方块
        if self.check_game_over():
            self.game_over()
        else:
            self.update_display()

    def can_move_down(self):
        """检查方块是否可以向下移动"""
        for r, row in enumerate(self.block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.block['x'] + c
                    y = self.block['y'] + r + 1
                    if y >= self.height or self.field[y][x] != 0:
                        return False
        return True

    def can_move_left(self):
        """检查方块是否可以向左移动"""
        for r, row in enumerate(self.block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.block['x'] + c - 1
                    y = self.block['y'] + r
                    if x < 0 or self.field[y][x] != 0:
                        return False
        return True

    def can_move_right(self):
        """检查方块是否可以向右移动"""
        for r, row in enumerate(self.block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.block['x'] + c + 1
                    y = self.block['y'] + r
                    if x >= self.width or self.field[y][x] != 0:
                        return False
        return True

    def lock_block(self):
        """将当前方块锁定到场地上"""
        for r, row in enumerate(self.block['shape']):
            for c, cell in enumerate(row):
                if cell:
                    x = self.block['x'] + c
                    y = self.block['y'] + r
                    self.field[y][x] = self.block['color']  # 锁定方块颜色
        self.update_display()

    def clear_lines(self):
        """检查并消除满行"""
        lines_to_clear = []
        for i, row in enumerate(self.field):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)

        # 处理消除行
        for line in lines_to_clear:
            self.field.pop(line)
            self.field.insert(0, [0] * self.width)  # 在顶部插入空行

        # 更新得分
        num_lines = len(lines_to_clear)
        if num_lines > 0:
            self.score += LINE_CLEAR_SCORE[num_lines]
        self.update_display()

    def check_game_over(self):
        """检查游戏是否结束"""
        for c in range(self.width):
            if self.field[0][c] != 0:
                return True
        return False

    def game_over(self):
        """游戏结束"""
        self.game_over_flag = True
        self.canvas.create_text(self.width * self.block_size // 2, self.height * self.block_size // 2,
                                text="Game Over", fill="white", font=('Arial', 24))

    def update_display(self):
        """更新显示"""
        self.canvas.delete('all')

        # 绘制场地
        for row in range(self.height):
            for col in range(self.width):
                x = col * self.block_size
                y = row * self.block_size
                color = self.field[row][col] if self.field[row][col] != 0 else 'gray'
                self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=color, outline='black')

        # 绘制当前方块
        if self.block:
            self.render_block(self.block)

        # 绘制得分
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", fill="white", anchor='nw')

    def render_block(self, block):
        """渲染当前方块"""
        shape = block['shape']
        color = block['color']
        for r, row in enumerate(shape):
            for c, cell in enumerate(row):
                if cell:
                    x = (block['x'] + c) * self.block_size
                    y = (block['y'] + r) * self.block_size
                    self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=color, outline='black')

    def on_key_press(self, event):
        """响应键盘事件"""
        if self.game_over_flag:
            return

        if event.keysym == MOVE_LEFT:
            self.move_block(MOVE_LEFT)
        elif event.keysym == MOVE_RIGHT:
            self.move_block(MOVE_RIGHT)
        elif event.keysym == MOVE_DOWN:
            self.move_block(MOVE_DOWN)
        elif event.keysym == ROTATE_CW:
            self.rotate_block_cw()
        elif event.keysym == ROTATE_CCW:
            self.rotate_block_ccw()
        elif event.keysym == 'space':
            self.hard_drop()

    def rotate_block_cw(self):
        """顺时针旋转方块"""
        if self.game_over_flag:
            return
        new_shape = list(zip(*self.block['shape'][::-1]))
        if self.can_rotate(new_shape):
            self.block['shape'] = new_shape
            self.update_display()

    def rotate_block_ccw(self):
        """逆时针旋转方块"""
        if self.game_over_flag:
            return
        new_shape = [list(row) for row in zip(*self.block['shape'])][::-1]
        if self.can_rotate(new_shape):
            self.block['shape'] = new_shape
            self.update_display()

    def can_rotate(self, new_shape):
        """检查方块是否可以旋转"""
        for r, row in enumerate(new_shape):
            for c, cell in enumerate(row):
                if cell:
                    x = self.block['x'] + c
                    y = self.block['y'] + r
                    if x < 0 or x >= self.width or y < 0 or y >= self.height or self.field[y][x] != 0:
                        return False
        return True


if __name__ == "__main__":
    game = TetrisGame()
    game.bind("<Left>", game.on_key_press)
    game.bind("<Right>", game.on_key_press)
    game.bind("<Down>", game.on_key_press)
    game.bind("<Up>", game.on_key_press)
    game.bind("<z>", game.on_key_press)
    game.bind("<space>", game.on_key_press)
    game.mainloop()
