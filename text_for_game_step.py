from termcolor import cprint
from datetime import timedelta


def print_info(game):
    curr_pos = game.current_status
    curr_info = game.step_info

    cprint(
        f'{"_" * 50}\n'
        f'Вы находитесь в {curr_pos["curr_loc"]}\n'
        f'У вас {curr_pos["exp"]} опыта и осталось {curr_pos["remaining_time"]} секунд до наводнения\n'
        f'Прошло времени: {timedelta(seconds=int(curr_pos["time"]))}\n'
        f'{"_" * 50}\n'
        f'Внутри вы видите:', color='blue', attrs=['bold'])

    for monster in curr_info["monsters"]:
        print(f'— Монстра: {monster}')

    for location in curr_info["locations"]:
        print(f'— Вход в локацию: {location}')


def print_attack_text(monster):
    cprint(f'Вы сражаетесь с монстром {monster}', color='red', attrs=['bold'])


def print_move_text(location):
    cprint(f'Вы поднимаетесь еще выше и попадаете в {location}', color='red')


def print_game_over_text():
    cprint('У вас темнеет в глазах... прощай, принцесса...\n'
           'Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)\n'
           'Ну, на этот-то раз у вас все получится! Трепещите, монстры!\n'
           'Вы осторожно входите в пещеру...', color='cyan', attrs=['bold'])


def print_game_end_text():
    cprint(f'Ура, вы успешно выбрались из подземелья..', color='red')


def print_value_error():
    cprint('Введено неверное значение, попробуйте еще раз', color='red', attrs=['bold'])
