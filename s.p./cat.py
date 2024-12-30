import tkinter as tk
from tkinter import messagebox

# 绘制面板, 只有在第一次绘制时才绘制背景色方块
def draw_board(canvas, block_list, isFirst=False):
    # 删掉原来所有的行
    for ri in range(R):
        canvas.delete("row-%s" % ri)

    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]   #取出每个位置的值
            if cell_type:
                draw_cell_by_cr(canvas, ci, ri, SHAPESCOLOR[cell_type], tag_kind="row") #有方块就按照原本颜色画
            elif isFirst:
                draw_cell_by_cr(canvas, ci, ri) #没方块就画成空白格子



draw_board(canvas, block_list, True)

#检查满格行
def check_row_complete(row):
    for cell in row:
        if cell=='':
            return False

    return True


score = 0
win.title("SCORES: %s" % score) # 标题中展示分数


#清除满格行
def check_and_clear():
    has_complete_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0:
                for cur_ri in range(ri, 0, -1):  #从下往上检索行数
                    block_list[cur_ri] = block_list[cur_ri-1][:]    #另每一行等于上一行
                block_list[0] = ['' for j in range(C)]
            else:
                block_list[ri] = ['' for j in range(C)]  #最上面一行新建一个空行
            global score
            score += 10

    if has_complete_row:
        draw_board(canvas, block_list)

        win.title("SCORES: %s" % score)

#在当游戏顶部格子再也放不下时，game over
if not check_move(current_block, [0, 0]):
            messagebox.showinfo("Game Over!", "Your Score is %s" % score)
            win.destroy()
            return

check_and_clear()   #在游戏的主程序中要加上消除满格行的函数