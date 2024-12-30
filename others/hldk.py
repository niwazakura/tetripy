# 玩家职业定义，player_classes是一个字典，请仔细阅读并理解
player_classes = {
    '猎人': {'health': 120, 'hunger': 40, 'thirst': 40, 'energy': 60, 'resources':
        {'food': 3, 'water': 2, 'wood': 1}, 'skill': '捕猎'},
    '农夫': {'health': 100, 'hunger': 30, 'thirst': 50, 'energy': 50, 'resources':
        {'food': 4, 'water': 2, 'wood': 0}, 'skill': '种植'},
    '科学家': {'health': 90, 'hunger': 50, 'thirst': 50, 'energy': 70,
        'resources': {'food': 2, 'water': 2, 'wood': 0, 'tools': 1}, 'skill': '发明工具'},
}

# 探索事件字典
explore_events = {
    'event_1': "暴风雨来袭，木材被摧毁！",
    'event_2': "野兽袭击，生命值减少20！",
    'event_3': "天气晴朗，额外获得一份食物和水！",
    'event_4': "找到隐藏的宝箱，获得5木材！",
    'event_5': "资源稀缺，食物和水减少一半！"
}

def create_player(class_name):
    """初始化玩家"""
    if class_name in player_classes:
        player = player_classes[class_name]  # 创建玩家属性
        player['class'] = class_name  # 保存玩家职业
        print(f"你选择的职业是: {class_name}")
        return player
    else:
        print("无效的职业！")
        return None

def display_status(player):
    """显示玩家状态"""
    print(f"\n职业: {player['class']} (技能: {player['skill']})")
    print(f"生命值: {player['health']}")
    print(f"饥饿值: {player['hunger']}")
    print(f"口渴值: {player['thirst']}")
    print(f"能量值: {player['energy']}")
    print(f"资源: {player['resources']}\n")

def eat_food(player):
    """吃食物:吃一份食物，资源中food值减1，玩家饥饿值减少20，并输出:你吃了一份食物！饥饿值减少。但如果食物不足，则输出：没有食物可以吃！"""
    if player['resources']['food'] > 0:
        player['hunger'] -= 20
        player['resources']['food'] -= 1
        print("你吃了一份食物！饥饿值减少。")
    else:
        print("没有食物可以吃！")

def drink_water(player):
    """喝水：喝一次水，资源中water值减1，玩家口渴值减少20，并输出:你喝了一杯水！口渴值减少。但如果水不足，则输出：没有水可以喝！"""
    if player['resources']['water'] > 0:
        player['thirst'] -= 20
        player['resources']['water'] -= 1
        print("你喝了一杯水！口渴值减少。")
    else:
        print("没有水可以喝！")

def rest(player):
    """休息恢复能量：玩家能量值+20，并输出：你休息了一会儿，恢复了一些能量。"""
    player['energy'] += 20
    print("你休息了一会儿，恢复了一些能量。")

def gather_resources(player):
    """采集资源：玩家资源中的食物+2，水+1，木材+1，并输出：你采集到了资源：2食物，1水，1木材。"""
    player['resources']['food'] += 2  # 固定数量的食物
    player['resources']['water'] += 1  # 固定数量的水
    player['resources']['wood'] += 1  # 固定数量的木材
    print("你采集到了资源：2食物，1水，1木材。")

def explore(player, event):
    """探索事件"""
    print("你决定去探索...")
    event_item = explore_events[event]
    print(f"探索事件发生: {event_item}")
    # 处理不同的探索事件
    if "暴风雨" in event_item:
        player['resources']['wood'] = max(0, player['resources']['wood'] - 1)
    elif "野兽袭击" in event:
        player['health'] -= 20
    elif "天气晴朗" in event_item:
        player['resources']['food'] += 1
        player['resources']['water'] += 1
    elif "宝箱" in event_item:
        player['resources']['wood'] += 5
    elif "资源稀缺" in event_item:
        player['resources']['food'] = max(0, player['resources']['food'] // 2)
        player['resources']['water'] = max(0, player['resources']['water'] // 2)

def use_skill(player):
    """使用职业技能：不同类型的玩家使用技能获得不同的收入，如猎人的技能是捕猎，可以获得食物+3的奖励，农夫的技能是种植，可以获得食物+1的奖励，科学家的技能是发明工具，能够使得资源中的工具值+1；"""
    if player['skill'] == '捕猎':
        print("你使用猎人的捕猎技能，成功获得额外的食物！")
        player['resources']['food'] += 3
    elif player['skill'] == '种植':
        print("你使用农夫的种植技能，成功种植了食物，未来几轮获得额外资源！")
        player['resources']['food'] += 1
    elif player['skill'] == '发明工具':
        print("你使用科学家的发明技能，成功制造了工具，采集效率提升！")
        player['resources']['tools'] += 1

def main():
    """游戏主循环"""
    print("请选择职业（猎人、农夫、科学家）: ")
    class_name = input()
    player = create_player(class_name)
    if player is None:
        return  # 职业无效，结束程序
    while player['health'] > 0:
        display_status(player)
        print("你想做什么？(吃食物/喝水/休息/采集资源/探索:event1-5/使用技能/退出): ")
        action = input()
        if action == "吃食物":
            eat_food(player)
        elif action == "喝水":
            drink_water(player)
        elif action == "休息":
            rest(player)
        elif action == "采集资源":
            gather_resources(player)
        elif action in ['event_1', 'event_2', 'event_3', 'event_4', 'event_5']:
            explore(player, action)
        elif action == "使用技能":
            use_skill(player)
        elif action == "退出":
            print("退出游戏。")
            break
        else:
            print("无效的操作！")
        # 简单的状态更新
        player['hunger'] += 5
        player['thirst'] += 5
        player['energy'] -= 10
        # 检查状态
        if player['hunger'] > 100:
            player['health'] -= 10
            print("你太饿了！生命值下降。")
        if player['thirst'] > 100:
            player['health'] -= 10
            print("你太渴了！生命值下降。")
        if player['energy'] < 0:
            print("你累倒了，游戏结束！")
            break
    print("游戏结束！")

if __name__ == "__main__":
    main()