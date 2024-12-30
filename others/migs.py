import pygame

# 全局变量
has_key = False  # 玩家是否有钥匙
lives = 3  # 初始生命值为3
CELL_SIZE = 50
WALL_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)
PLAYER_COLOR = (0, 0, 255)
KEY_COLOR = (255, 215, 0)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)


def input_maze():
    maze = []
    print("请输入迷宫地图（#代表墙,.代表空地, S代表起点, E代表终点, K代表钥匙）：")
    print("请按行输入地图，或输入 'done' 结束输入：")
    while True:
        row = input().split()
        if row == ["done"]:
            break
        maze.append(list(row))

    if not validate_maze(maze):
        print("迷宫必须有起点(S)和终点(E)，请重新输入。")
        maze.clear()
        return input_maze()
    return maze


def validate_maze(maze):
    start_exist = any('S' in row for row in maze)
    end_exist = any('E' in row for row in maze)
    return start_exist and end_exist


def find_start_exit_pos(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == 'S':
                start_pos = (row, col)
            if maze[row][col] == 'E':
                exit_pos = (row, col)
    return start_pos, exit_pos


def draw_maze(screen, maze, player_pos):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if maze[row][col] == "#":
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif maze[row][col] == "S":
                pygame.draw.rect(screen, START_COLOR, rect)
            elif maze[row][col] == "E":
                pygame.draw.rect(screen, END_COLOR, rect)
            elif maze[row][col] == "K":
                pygame.draw.rect(screen, KEY_COLOR, rect)
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)

    player_x = player_pos[1] * CELL_SIZE
    player_y = player_pos[0] * CELL_SIZE
    player_rect = pygame.Rect(player_x, player_y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)


def move_player(maze, directionlst, now_pos):
    global lives
    before_pos = now_pos
    for dr in directionlst:
        row = now_pos[0]
        col = now_pos[1]
        if dr == "w":
            new_row = row - 1
            new_col = col
        elif dr == "s":
            new_row = row + 1
            new_col = col
        elif dr == "a":
            new_row = row
            new_col = col - 1
        elif dr == "d":
            new_row = row
            new_col = col + 1
        else:
            print("无效的移动指令，请输入 'w', 'a', 's', 'd' 来移动。")
            return

        now_pos = (new_row, new_col)

    if is_valid_move(now_pos, maze):
        get_key(maze, now_pos)
        return now_pos
    else:
        lives -= 1
        print(f"撞墙了！当前生命值为{lives}")
        if lives <= 0:
            print("你用尽了所有生命，游戏结束")
            pygame.quit()
            exit()
        print("无法移动到该位置！已回到上一次的位置。")
        return before_pos


def is_valid_move(position, maze):
    row, col = position
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col]!= "#"


def get_key(maze, new_pos):
    global has_key
    if maze[new_pos[0]][new_pos[1]] == "K":
        print("你找到了钥匙！")
        has_key = True


def main():
    pygame.init()
    maze = input_maze()
    start_pos, exit_pos = find_start_exit_pos(maze)
    screen_width = len(maze[0]) * CELL_SIZE
    screen_height = len(maze) * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Maze Game')
    clock = pygame.time.Clock()
    before_pos = start_pos
    now_pos = None

    print("迷宫已生成，目标是从 S 走到E，要求先拿到K，才可以打开出口大门，成功的走出迷宫。")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_maze(screen, maze, before_pos)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        direction = ""
        if keys[pygame.K_w]:
            direction += "w"
        elif keys[pygame.K_s]:
            direction += "s"
        elif keys[pygame.K_a]:
            direction += "a"
        elif keys[pygame.K_d]:
            direction += "d"

        if direction:
            now_pos = move_player(maze, direction, before_pos)
            if now_pos == exit_pos and has_key:
                print("恭喜你！成功走出了迷宫！")
                running = False
            elif now_pos == exit_pos and not has_key:
                now_pos = before_pos
                print("你需要钥匙才能进入终点！")
                print("已经退回上一步位置！")
            before_pos = now_pos

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()