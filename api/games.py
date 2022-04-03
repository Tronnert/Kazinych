import random


class Game:
    def __init__(self, *args, **kwargs):
        ...

    def get_win(self, json):
        win = None
        ch = None
        return win, ch

class Roulette(Game):
    def __init__(self, *args, **kwargs):
        pass

    def get_win(self, json):
        win = 0
        ch = random.randint(1, 37)
        if ch == int(json['number']):
            win = int(json['bet'])
        return win, ch

class Cyber_Roulette:
    def __init__(self):
        pass

    def get_win(self, json):
        win = 0
        ch = random.randint(1, 8)
        if ch == int(json['number']):
            win = int(json['bet'])
        return win, ch

games_dict = {'roulette': Roulette(), 'cyber_roulette': Cyber_Roulette()}
# first_roulette = Game('first', 0.2, 0.5, 1, 1.2, 1.5)
# games_dict.update(first_roulette.get())

