from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


# 玩家职业定义，player_classes是一个字典，请仔细阅读并理解
player_classes = {
    '猎人': {'health': 120, 'hunger': 40, 'thirst': 40, 'energy': 60, 'resources':
             {'food': 3, 'water': 2, 'wood': 1}, 'skill': '捕猎'},
    '农夫': {'health': 100, 'hunger': 30, 'thirst': 50, 'energy': 50, 'resources':
             {'food': 4, 'water': 2, 'wood': 0}, 'skill': '种植'},
    '科学家': {'health': 90, 'hunger': 50, 'thirst': 50, 'energy': 70,
                'resources': {'food': 2, 'water': 2, 'wood': 0, 'tools': 1}, 'skill': '发明工具'}
}

# 探索事件字典
explore_events = {
    'event_1': "暴风雨来袭，木材被摧毁！",
    'event_2': "野兽袭击，生命值减少20！",
    'event_3': "天气晴朗，额外获得一份食物和水！",
    'event_4': "找到隐藏的宝箱，获得5木材！",
    'event_5': "资源稀缺，食物和水减少一半！"
}


class Player:
    def __init__(self, class_name):
        if class_name in player_classes:
            self.__dict__.update(player_classes[class_name])
            self.player_class = class_name
        else:
            raise ValueError("无效的职业！")

    def eat_food(self):
        if self.resources['food'] > 0:
            self.hunger -= 20
            self.resources['food'] -= 1
        else:
            print("没有食物可以吃！")

    def drink_water(self):
        if self.resources['water'] > 0:
            self.thirst -= 20
            self.resources['water'] -= 1
        else:
            print("没有水可以喝！")

    def rest(self):
        self.energy += 20

    def gather_resources(self):
        self.resources['food'] += 2
        self.resources['water'] += 1
        self.resources['wood'] += 1

    def explore(self, event):
        print("你决定去探索...")
        event_item = explore_events[event]
        print(f"探索事件发生: {event_item}")
        if "暴风雨" in event_item:
            self.resources['wood'] = max(0, self.resources['wood'] - 1)
        elif "野兽袭击" in event:
            self.health -= 20
        elif "天气晴朗" in event_item:
            self.resources['food'] += 1
            self.resources['water'] += 1
        elif "宝箱" in event_item:
            self.resources['wood'] += 5
        elif "资源稀缺" in event_item:
            self.resources['food'] = max(0, self.resources['food'] // 2)
            self.resources['water'] = max(0, self.resources['water'] // 2)

    def use_skill(self):
        if self.skill == '捕猎':
            self.resources['food'] += 3
        elif self.skill == '种植':
            self.resources['food'] += 1
        elif self.skill == '发明工具':
            self.resources['tools'] += 1

    def update_status(self):
        try:
            self.hunger += 5
            self.thirst += 5
            self.energy -= 10
            if self.hunger > 100:
                self.health -= 10
            if self.thirst > 100:
                self.health -= 10
            if self.energy < 0:
                print("你累倒了，游戏结束！")
        except Exception as e:
            print(f"更新状态出错: {e}")


    def get_status(self):
        status = f"职业: {self.player_class} (技能: {self.skill})\n"
        status += f"生命值: {self.health}\n"
        status += f"饥饿值: {self.hunger}\n"
        status += f"口渴值: {self.thirst}\n"
        status += f"能量值: {self.energy}\n"
        status += f"资源: {self.resources}\n"
        return status


class GameLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.player = None

        # 左半部分
        self.left_panel = BoxLayout(orientation="vertical")
        self.status_label = Label(text="")
        self.left_panel.add_widget(self.status_label)
        self.add_widget(self.left_panel)

        # 右半部分
        self.right_panel = BoxLayout(orientation="vertical")
        self.create_player_input = TextInput(hint_text="请选择职业（猎人、农夫、科学家）")
        self.start_button = Button(text="开始游戏", on_release=self.start_game)
        self.right_panel.add_widget(self.create_player_input)
        self.right_panel.add_widget(self.start_button)

        self.action_input = TextInput(hint_text="你想做什么？(吃食物/喝水/休息/采集资源/探索:event1-5/使用技能/退出)")
        self.action_button = Button(text="执行", on_release=self.perform_action)
        self.right_panel.add_widget(self.action_input)
        self.right_panel.add_widget(self.action_button)

        self.output_label = Label(text="")
        self.right_panel.add_widget(self.output_label)
        self.add_widget(self.right_panel)

    def start_game(self, instance):
        try:
            class_name = self.create_player_input.text
            self.player = Player(class_name)
            self.update_status()
        except ValueError as e:
            self.status_label.text = str(e)

    def perform_action(self, instance):
        if self.player:
            action = self.action_input.text
            if action == "吃食物":
                self.player.eat_food()
            elif action == "喝水":
                self.player.drink_water()
            elif action == "休息":
                self.player.rest()
            elif action == "采集资源":
                self.player.gather_resources()
            elif action in ['event_1', 'event_2', 'event_3', 'event_4', 'event_5']:
                self.player.explore(action)
            elif action == "使用技能":
                self.player.use_skill()
            elif action == "退出":
                self.output_label.text += "退出游戏。\n"
                return
            else:
                self.output_label.text += "无效的操作！\n"
            self.player.update_status()
            self.update_status()
            self.output_label.text += self.player.get_status() + "\n"
            self.action_input.text = ""

    def update_status(self):
        if self.player:
            self.status_label.text = self.player.get_status()


class SurvivalGameApp(App):
    def build(self):
        return GameLayout()

    def on_start(self):
        pass


if __name__ == "__main__":
    SurvivalGameApp().run()