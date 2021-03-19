import json
import re
import csv
from decimal import Decimal

from text_for_game_step import *

EXP_FOR_EXIT = 280
field_names = ['current_location', 'current_experience', 'current_date']


class RPG:

    def __init__(self, game_data, game_log):
        self.game_data = game_data
        self.game_log = game_log

        self.game_map = None
        self.current_status = {
            'curr_loc': str,  # текущее местоположение
            'exp': 0,  # текущий опыт
            'time': 0,  # прошло времени
            'remaining_time': Decimal('123456.0987654321')  # оставшееся время
        }
        self.step_info = {}

    def get_game_map(self):
        with open(self.game_data, 'r', encoding='utf-8') as file:
            loaded_file = json.load(file)

        self.current_status['curr_loc'] = 'Location_0_tm0'
        self.game_map = loaded_file['Location_0_tm0']

    def get_next_step(self):

        print_info(self)

        monstr, loc = self.step_info['monsters'], self.step_info['locations']

        if monstr and loc:
            step = (
                f'\nВыберите действие:\n'
                f'1.Атаковать монстра \n'
                f'2.Перейти в другую локацию \n'
                f'3.Сдаться и выйти из игры\n'
            )
            act = ['attack', 'move', 'game_over']
            x = 3
        elif monstr and not loc:
            step = (
                f''
                f'Вы зашли в тупик, игра окончена\n'
                f'1.Сдаться и выйти из игры\n'
            )
            act = ['game_over']
            x = 1
        else:
            step = (
                f'\nВыберите действие:\n'
                f'1.Перейти в другую локацию\n'
                f'2.Сдаться и выйти из игры\n'
            )
            act = ['move', 'game_over']
            x = 2

        while True:
            choice_pattern = f'[1-{x}]'
            next_step = input(step)
            match = re.match(choice_pattern, next_step)
            if match:
                return act[int(next_step) - 1]
            else:
                print_value_error()

    def get_position(self):
        self.step_info = {
            'monsters': [],  # монстры в текущей локации
            'locations': [],  # возможные пути дальше
        }

        for item in self.game_map:
            if isinstance(item, str):
                self.step_info['monsters'].append(item)
            else:
                for location in item.keys():
                    self.step_info['locations'].append(location)

    def make_log(self):
        curr_loc = str(self.current_status['curr_loc'])
        curr_exp = str(self.current_status['exp'])
        curr_time = str(self.current_status['time'])
        new_record = {'current_location': curr_loc, 'current_experience': curr_exp, 'current_date': curr_time}

        with open(self.game_log, 'a', newline='') as out_csv:
            writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=field_names)
            writer.writerow(new_record)


class GameActions:

    def __init__(self, game, action):
        self.action = action
        self.game = game

    def attack(self):
        monsters = self.game.step_info['monsters']
        n = 1
        x = len(monsters)

        choice_pattern = f'[1-{x}]'

        print(f'Доступны следующие действия:')
        while True:
            for monster in monsters:
                print(f'{n}. Атаковать {monster}')
                n += 1

            number = input(
                f'\nВыберите действие:\n')

            match = re.match(choice_pattern, number)
            if match:
                monster = monsters[int(number) - 1]
                print_attack_text(monster)
                break
            else:
                print_value_error()
                n = 1

        self.game.game_map.remove(monster)
        name, exp, tm = monster.split('_')
        self.game.current_status['exp'] += int(exp[3:])
        self.game.current_status['time'] += Decimal(float(tm[2:]))
        self.game.current_status['remaining_time'] -= Decimal(float(tm[2:]))

    def go(self):
        locations = self.game.step_info['locations']
        n = 1
        x = len(locations)

        choice_pattern = f'[1-{x}]'

        print(f'Доступны следующие действия:')
        while True:
            for location in locations:
                print(f'{n}. Перейти в {location}')
                n += 1

            number = input(f'\nВыберите действие:\n')

            match = re.match(choice_pattern, number)
            if match:
                location = locations[int(number) - 1]
                print_move_text(location)
                break
            else:
                print_value_error()
                n = 1

        if 'Hatch' in location.split('_'):
            if int(self.game.current_status['exp']) >= EXP_FOR_EXIT:
                print_game_end_text()
                return 'Hatch'
            else:
                print('Вам недостает опыта чтобы открыть люк. Игра окончена')
                self.game_over()
                print_game_over_text()
        else:
            print(location, type(location))
            name, loc_number, tm = location.split('_')
            self.game.current_status['time'] += Decimal(float(tm[2:]))
            self.game.current_status['remaining_time'] -= Decimal(float(tm[2:]))
            self.game.current_status['curr_loc'] = location

        for item in self.game.game_map:
            try:
                new_map = item[location]
                self.game.game_map = new_map
            except Exception as exc:
                print(exc)

    def game_over(self):
        self.game.current_status = {
            'curr_loc': str,
            'exp': 0,
            'time': 0,
            'remaining_time': Decimal('123456.0987654321')
        }
        self.game.get_game_map()

    def check(self):
        if float(self.game.current_status['remaining_time']) <= 0:
            self.game_over()
            print_game_over_text()

    def act(self):
        self.check()
        if self.action == 'attack':
            self.attack()
        elif self.action == 'move':
            if self.go() == 'Hatch':
                return 'Hatch'
        elif self.action == 'game_over':
            self.game_over()
            print_game_over_text()
        else:
            print('Что-то пошло не так')


def play():
    game = RPG(game_data='rpg.json', game_log='rpg_game_log.csv')
    game.get_game_map()

    with open(game.game_log, 'w', newline='') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerow(field_names)

    while True:
        game.get_position()
        act = game.get_next_step()
        action = GameActions(game, act)
        if action.act() == 'Hatch':
            again = int(input('Еще раз - нажмите "1"\nВыход - "0"'))
            if again == 1:
                print('Вы осторожно входите в пещеру...')
                action.game_over()
            else:
                break
        else:
            game.make_log()


if __name__ == '__main__':
    play()
