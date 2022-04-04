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
        ch = random.randint(0, 36)
        l = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
                    24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        print(json['number'])
        if json['number'] == 'odd':
            if ch % 2 == 1:
                win = 2 * int(json['bet'])
        elif json['number'] == 'even':
            if ch % 2 == 0:
                print(1)
                win = 2 * int(json['bet'])
        elif json['number'] == 'red':
            if l.index(ch) % 2 == 1:
                win = 2 * int(json['bet'])
        elif json['number'] == 'black':
            if l.index(ch) % 2 == 0 and ch != 0:
                win = 2 * int(json['bet'])
        else:
            if ch == int(json['number']):
                win = 2 * int(json['bet'])
        return win, ch


class Cyber_Roulette(Game):
    def __init__(self, *args, **kwargs):
        pass

    def get_win(self, json):
        win = 0
        ch = random.randint(1, 8)
        if ch == int(json['number']):
            win = 2 * int(json['bet'])
        return win, ch

games_dict = {'roulette': Roulette(), 'cyber_roulette': Cyber_Roulette()}
# first_roulette = Game('first', 0.2, 0.5, 1, 1.2, 1.5)
# games_dict.update(first_roulette.get())

