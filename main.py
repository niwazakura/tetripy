import pygame
import time
import tkinter as tk
import random


BLOCK_SIZE = 30
WIDTH = 10
HEIGHT = 20
LINE_CLEAR_SCORE = {1: 100, 2: 300, 3: 500, 4: 800}

s_width = 800
s_height = 700
play_width = 300  
play_height = 600  

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
play_width = 300  
play_height = 600  


class TetrisGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris Game")
        
        
        self.game_over_flag = False
        self.score = 0
        
        
        self.width = WIDTH
        self.height = HEIGHT
        self.field = [[0] * self.width for _ in range(self.height)]
        self.block_size = 30  

        
        
        self.current_block = None
        
        
        self.canvas = tk.Canvas(self.root, width=self.width * BLOCK_SIZE, height=self.height * BLOCK_SIZE)
        self.canvas.pack()
        
        
        self.root.bind("<KeyPress>", self.on_key_press)
        
        
        self.new_block()
        self.drop_block()
        self.root.after(500, self.game_loop)  
        self.root.mainloop()

    def game_loop(self):
        shapes = [
            [[1, 1, 1, 1]],  
            [[1, 1], [1, 1]],  
            [[0, 1, 0], [1, 1, 1]],  
            [[1, 1, 0], [0, 1, 1]],  
            [[0, 1, 1], [1, 1, 0]],  
            [[1, 0, 0], [1, 1, 1]],  
            [[0, 0, 1], [1, 1, 1]]   
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
        if self.can_move(direction):
            dx, dy = direction
            self.current_block['x'] += dx
            self.current_block['y'] += dy
            self.update_display()

    def lock_block(self):
        for c in range(self.width):
            if self.field[0][c] != 0:
                return True
        return False

    def game_over(self):
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
        for y in range(self.height):
            for x in range(self.width):
                color = 'light gray' if (x + y) % 2 == 0 else 'gray'
                self.canvas.create_rectangle(
                    x * BLOCK_SIZE, y * BLOCK_SIZE,
                    (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                    outline='gray', width=1, fill=color
                )

    def on_key_press(self, event):
        if not self.game_over_flag:
            old_shape = self.current_block['shape']
            self.current_block['shape'] = [list(row) for row in zip(*self.current_block['shape'][::-1])]
            if not self.can_move(MOVE_DOWN) and not self.can_move(MOVE_LEFT) and not self.can_move(MOVE_RIGHT):
                self.current_block['shape'] = old_shape
            self.update_display()

    def drop_block(self):
        while self.can_move(MOVE_DOWN):
            self.current_block['y'] += 1
        self.lock_block()
        self.update_display()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer_music.load("https://cdn.freesound.org/previews/779/779827_5674468-lq.mp3")  
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer .music.play(-1)
    
    
    
    win = pygame.display.set_mode((s_width, HEIGHT * s_height))
    pygame.display.set_caption('Tetris')
    win.fill((0,0,0))
    draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
    pygame.display.update()
    time.sleep(2)
    pygame.display.quit()
    TetrisGame()
