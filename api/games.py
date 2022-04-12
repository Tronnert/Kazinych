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


class Slots2(Game):
    def get_win(self, json):
        win = 0
        one = [[random.randint(0, 5) for e in range(3)] for j in range(3)]
        if (one[0][0] == one[1][1] == one[2][2]) \
                or (one[2][0] == one[1][1] == one[0][2]):
            win = 2 * int(json['bet'])
        if one[0][0] == one[0][1] == one[0][2]:
            win += int(2 * int(json['bet']))
        if one[1][0] == one[1][1] == one[1][2]:
            win = int(2 * int(json['bet']))
        if one[2][0] == one[2][1] == one[2][2]:
            win = int(2 * int(json['bet']))
        return win, one


class CoinToss(Game):
    def get_win(self, json):
        one = random.randint(0, 1)
        return one * 10, one


class Dice(Game):
    def get_win(self, json):
        one = [[], []]
        pl = True
        while sum(one[0]) < 100 and sum(one[1]) < 100:
            if pl:
                one[0].append(random.randint(1, 6))
                if one[0][-1] == 1:
                    pl = False
            else:
                one[1].append(random.randint(1, 6))
                if one[1][-1] == 1:
                    pl = True
        return 2 * int(json['bet']) * (sum(one[0]) >= 100), one


class ShellGame(Game):
    def get_win(self, json):
        one = random.randint(0, 2)
        if one == 2:
            return int(json['bet']) * 4, 1
        else:
            return 0, 0


games_dict = {'roulette': Roulette(), 'cyber_roulette': Cyber_Roulette(),
              'slots1': Slots1(), 'slots2': Slots2(), 'coin_toss': CoinToss(), 'dice': Dice(),
              'shell_game': ShellGame()}
# first_roulette = Game('first', 0.2, 0.5, 1, 1.2, 1.5)
# games_dict.update(first_roulette.get())
