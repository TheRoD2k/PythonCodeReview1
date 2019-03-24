# import tkinter


class PlayerClass:
    def __init__(self):
        self.Name = "Джон"
        self.HP = 100
        self.Mood = 100
        self.Alive = True
        self.KilledMessage = "Вы погибли от полученных ранений"
        self.PsychoMessage = "Вы сошли с ума"

    def recover_stats(self, prev_stats):
        self.HP = int(prev_stats[0])
        self.Mood = int(prev_stats[1])
        self.Alive = bool(prev_stats[2])

    def endgame(self):
        pass

    def name_change(self, new_name):
        self.Name = new_name

    def check_status(self):
        if self.HP <= 0:
            self.Alive = False
            print(self.KilledMessage)
        else:
            if self.Mood <= 0:
                self.Alive = False
                print(self.PsychoMessage)

        if not self.Alive:
            self.endgame()

    def show_status(self):
        print(self.Name)
        print("HP: ", self.HP)
        print("Mood: ", self.Mood)
        if self.HP <= 0:
            print("Мертв")
        else:
            if self.HP <= 25:
                print("При смерти")
            else:
                if self.HP <= 50:
                    print("Сильно ранен")
                else:
                    if self.HP <= 75:
                        print("Ранен")
                    else:
                        print("Здоров")

            if self.Mood <= 0:
                print("Сошел с ума")
            else:
                if self.HP <= 25:
                    print("Ужас")
                else:
                    if self.HP <= 50:
                        print("Паника")
                    else:
                        if self.HP <= 75:
                            print("Испуг")
                        else:
                            print("Разум в норме")

    def take_damage(self, damage):
        self.HP -= damage
        if self.HP < 0:
            self.HP = 0
        self.Mood -= int(0.2*damage)
        if self.Mood < 0:
            self.Mood = 0

    def heal(self, heal):
        self.HP += heal
        if self.HP > 100:
            self.HP = 100
        if self.HP < 0:
            self.HP = 0
        self.Mood += int(0.3*heal)
        if self.Mood > 100:
            self.Mood = 100
        if self.Mood < 0:
            self.Mood = 100


class ChoicePoint:
    def __init__(self, variants_massive, current):
        self.variants = variants_massive

    def show_prelude(self):
        print(self.prelude)

    def list_choice(self):
        for i in self.variants:
            print(i)

    def make_choice(self, choice):
        pass


class DialogueBranch:
    def __init__(self, ways, strings, actions):
        self.prelude = strings[-1]
        self.choices = list(zip(ways, strings))
        self.actions = actions

    def execute_actions(self, Player):
        action_dict = {
            "<DAMAGE>":Player.take_damage,
            "<HEAL>":Player.heal
        }
        for action in self.actions:
            action[2] = action[2].replace('<playername>', Player.Name)
            if action[2] != "<NOMESSAGE>":
                print(action[2])
            action_dict[action[0]](int(action[1]))


    def list_choices(self, Player, exec_action): # NOTE Also executes actions
        temp_prelude = self.prelude
        temp_prelude = temp_prelude.replace('<playername>', Player.Name)
        print(temp_prelude)
        if exec_action:
            self.execute_actions(Player)
        if Player.Alive:
            Player.show_status()
            for i in range(len(self.choices)):
                temp_string = self.choices[i][1]
                temp_string = temp_string.replace('<playername>', Player.Name)
                print(i+1, ") ", temp_string)   # Add choice blockers
            print('s )  Сохраниться')
        print('l )  Загрузиться')
        print('b )  Назад')
        print('e )  Выйти')

    def make_choice(self, choice, cur, Player):
        choice_number = choice - 1
        if choice_number < 0 or choice_number >= len(self.choices) or not Player.Alive:
            print("Неверный вариант ответа!")
            return cur
        return self.choices[choice_number][0]


def build_dialogue_tree(root_to_folder):
    print("Building a dialogue tree...")
    roots = open(root_to_folder + 'roots')
    print("File successfully opened...")
    branches = []
    branches_names = []
    action_set = {
        "<DAMAGE>",
        "<HEAL>"
    }
    for line in roots:
        cur_str = line.split()
        cell_name = cur_str[0]
        branches_names.append(cell_name)
        ways = []
        for i in range(1, len(cur_str)):
            ways.append(cur_str[i])
        strings = []
        actions = []
        cur_file = open(root_to_folder + cell_name)
        count = 0
        prelude = ""
        for cur_line in cur_file:
            cur_line = cur_line.rstrip()
            if count == 0:
                prelude = cur_line
            else:
                if cur_line.split("\t")[0] in action_set:
                    cur_line = cur_line.split("\t")
                    actions.append(cur_line)
                    continue
                else:
                    strings.append(cur_line)
            count += 1
        strings.append(prelude)
        branches.append(DialogueBranch(ways, strings, actions))
    print("Success")
    return dict(zip(branches_names, branches))


def game():

    def save_game(root_to_folder):
        new_file = open(root_to_folder + 'savegame', 'w+')
        for i in temp_save:
            new_file.write(i + " ")
        new_file.write("\n")
        stats_string = str(Player.HP) + "\t" + str(Player.Mood) + "\t" + str(Player.Alive)
        new_file.write("<STATS>\t" + stats_string)


    def load_game(root_to_folder):
        file = open(root_to_folder + 'savegame')
        nonlocal temp_save
        temp_save = file.readline().split()
        nonlocal current_point
        current_point = temp_save[-1]
        stats = file.readline().split("\t")
        stats = stats[1:len(stats)]
        Player.recover_stats(stats)

    def go_back():
        nonlocal current_point
        if len(temp_save) > 1:
            current_point = temp_save[len(temp_save)-2]
            temp_save.pop(len(temp_save)-1)
            Player.recover_stats(prev_stats[-1])
            prev_stats[-1].pop()
        else:
            print("Больше некуда шагать!")

    Player = PlayerClass()
    temp_save = []

    game_lasts = True
    root_to_folder = input("Введите путь до папки с файлом root в формате folder\\ \n")
    DialogueTree = build_dialogue_tree(root_to_folder)
    print("Введите имя")
    name = input()
    Player.name_change(name)
    print(Player.Name, ", ваше путешествие начинается")
    current_point = "0"
    prev_stats = []
    # print(DialogueTree["0"].choices[1])
    while Player.Alive and game_lasts:
        exec_action = True
        if len(temp_save) > 0 and temp_save[len(temp_save) - 1] == current_point:
            exec_action = False
        if len(temp_save) == 0 or temp_save[len(temp_save) - 1] != current_point:
            temp_save.append(current_point)
        DialogueTree[current_point].list_choices(Player,  exec_action)
        choice = input()
        if choice == 's' and Player.Alive:
            save_game(root_to_folder)
            continue
        if choice == 'l':
            load_game(root_to_folder)
            continue
        if choice == 'b':
            go_back()
            continue
        if choice == 'e':
            game_lasts = False
            continue
        prev_stats.append([Player.HP, Player.Mood, Player.Alive])
        current_point = DialogueTree[current_point].make_choice(int(choice), current_point, Player)
        Player.check_status()
        print("="*20)
        if current_point == "-1":
            game_lasts = False
    print("Ваше путешествие закончилось")


game()
