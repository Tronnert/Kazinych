import random


class Game:
    def __init__(self, *args, **kwargs):
        ...

    def get_win(self, json):
        win = None
        ch = None
        return win, ch


class Roulette(Game):
    def get_win(self, json):
        win = 0
        ch = random.randint(0, 36)
        if ch == int(json['number']):
            win = 2 * int(json['bet'])
        return win, ch


class Cyber_Roulette(Game):
    def get_win(self, json):
        win = 0
        ch = random.randint(1, 8)
        if ch == int(json['number']):
            win = 2 * int(json['bet'])
        return win, ch


class Slots1(Game):
    def get_win(self, json):
        win = 0
        one = [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)]
        if one[0] == one[1] == one[2]:
            win = 36 * int(json['bet'])
        if one[0] == one[1] or one[0] == one[2] or one[1] == one[2]:
            win = int(9 / 4 * int(json['bet']))
        return win, one


games_dict = {'roulette': Roulette(), 'cyber_roulette': Cyber_Roulette(), 'slots1': Slots1()}
# first_roulette = Game('first', 0.2, 0.5, 1, 1.2, 1.5)
# games_dict.update(first_roulette.get())
