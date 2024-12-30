# 全局变量
has_key = False # 玩家是否有钥匙
lives = 3 # 初始生命值为3

def input_maze():
    maze=[]
    """用户输入自定义迷宫，返回二维列表表示迷宫"""
    print("请输入迷宫地图（#代表墙, .代表空地, S代表起点, E代表终点, K代表钥匙）：")
    print("请按行输入地图，或输入 'done' 结束输入：")
    #begin 按行读入迷宫地图，构建迷宫地图列表矩阵maze
    while True:
        row = input().split()
        if row == ["done"]:
            break
        maze.append(list(row))
    # end
    # 验证迷宫是否有起点和终点
    if not validate_maze(maze):
        print("迷宫必须有起点(S)和终点(E)，请重新输入。")
        maze.clear() # 清空迷宫重输入
        input_maze()
    return maze

"""验证迷宫是否包含起点和终点"""
def validate_maze(maze):
    start_exist = any('S' in row for row in maze)
    end_exist = any('E' in row for row in maze)
    return start_exist and end_exist

"""找到起点、终点的位置"""
def find_start_exit_pos(maze):
    # begin
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 'S':
                start_pos=(row, col)
            if maze[row][col] == 'E':
                exit_pos=(row, col)
    return start_pos,exit_pos
    # end

"""打印当前迷宫和玩家位置"""
def print_maze(maze,player_pos):
    # begin
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if (row, col) == player_pos:
                print("P", end=" ") # P 代表玩家
            elif maze[row][col] == "#":
                print("#", end=" ") # # 代表墙
            elif maze[row][col] == "S":
                print("S", end=" ") # S 代表起点
            elif maze[row][col] == "E":
                print("E", end=" ") # E 代表终点
            elif maze[row][col] == "K":
                print("K", end=" ") # K 代表钥匙
            else:
                print(".", end=" ") # . 代表空地
        print()
    print()
    # end

"""根据玩家的输入移动玩家位置:
如果移动位置合法，则玩家移动到新位置；
如果移动位置撞墙，则玩家回复到移动前的位置，同时玩家生命值减一，提示：撞墙了！当前生命
值为{lives}
如果玩家的生命值为0了，则提示：你用尽了所有生命，游戏结束，用exit()语句退出游戏"""
def move_player(maze,directionlst,now_pos):# maze 游戏当前的地图矩阵，directionlst玩家移动走步的列表，now_pos玩家当前的位置
    global lives #玩家生命值，请注意这个lives变量时global类型的
    before_pos=now_pos # before_pos 开始移动前的玩家的位置
    for dr in directionlst:
        row = now_pos[0]
        col = now_pos[1]
        #begin
        if dr == "w" : # 上
            now_pos = (row - 1, col)
        elif dr == "s": # 下
            now_pos = (row + 1, col)
        elif dr == "a": # 左
            now_pos = (row, col - 1)
        elif dr == "d": # 右
            now_pos = (row, col + 1)
        #end
        else:
            print("无效的移动指令，请输入 'w', 'a', 's', 'd' 来移动。")
            return
    # 如果按照directionlst内容移动的位置有效，则看下是否获取到key，并返回新移动到的位置
    
    if is_valid_move(now_pos,maze):
        get_key(maze,now_pos)
        return now_pos
    else:
        lives-=1
        print(f"撞墙了！当前生命值为{lives}")
        if lives<=0 :
            print("你用尽了所有生命，游戏结束")
            exit()
        print("无法移动到该位置！已回到上一次的位置。")
        return before_pos

"""检查位置是否有效（未越界并且不是墙）"""
def is_valid_move(position,maze):
    # begin
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != "#"
    #end

"""根据游戏地图和玩家位置，判定玩家是否获取钥匙"""
def get_key(maze,new_pos):
    # begin
    global has_key
    if maze[new_pos[0]][new_pos[1]] == "K": # 找到钥匙
        print("你找到了钥匙！")
        has_key = True
        return
    #end

def main():
    # 输入自定义迷宫
    map_maze = input_maze()
    start_pos,exit_pos=find_start_exit_pos(map_maze) # 找到起点,终点位置
    before_pos=start_pos
    now_pos=None
    print("迷宫已生成，目标是从 S 走到E，要求先拿到K，才可以打开出口大门，成功的走出迷宫。")
    # 游戏主循环
    while True:
        print_maze(map_maze,before_pos)
        print("请输入移动方向 w 上, a 左, s 下, d 右：",end="")
        move = input().strip().lower()
        print(move,end="\n")
        now_pos=move_player(map_maze,move,before_pos)
        if now_pos==exit_pos and has_key:
            print("恭喜你！成功走出了迷宫！")
            break
        if now_pos==exit_pos and not has_key :
            now_pos=before_pos
            print("你需要钥匙才能进入终点！")
            print("已经退回上一步位置！")
        before_pos=now_pos

# 运行游戏
if __name__ == "__main__":
    main()