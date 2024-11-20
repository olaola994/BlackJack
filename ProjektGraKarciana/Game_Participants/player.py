class Player():
    player_count = 0

    def __init__(self, name):
        Player.player_count += 1
        self.id = Player.player_count
        self.name = name
        self.reward = 0
        self.money = 20000
        self.even_money = False
        self.insurance_taken = False
        self.initial_bet = 0
        self.hand = []
        self.points = 0
        self.twoHandGame = False
        self.isBlackJack = False

