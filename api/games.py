class Game:
    def __init__(self, name, *args):
        self.name = name
        self.koeff = args

    def get(self):
        return {self.name: self.koeff}


games_dict = {}
first_roulette = Game('first', 0.2, 0.5, 1, 1.2, 1.5)
games_dict.update(first_roulette.get())

