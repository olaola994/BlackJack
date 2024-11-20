from Game_Participants.player import Player
from Game_Participants.dealer import Dealer
from game import Game

class Table():
    table_count = 0
    def __init__(self):
        Table.table_count += 1
        self.id = Table.table_count
        self.players = []
        self.dealer = Dealer()
        self.logs = {}
        self.games = []

    def openTable(self):
        print("Utworzenie stołu do gry BlackJack\n")
        print("\nCzy chcesz wyświetlić instrukcję gry BlackJack?\n-tak (1)\n-nie (0)")
        showInstruction = int(input())
        while(not (showInstruction == 1 or showInstruction == 0)):
            print("Prosze wybrac 1 lub 0")
            showInstruction = int(input())
        if(showInstruction == 1):
            with open('instrukcja_gry.txt', 'r') as file:
                content = file.read()
                print(content)

        print("\nIlu graczy będzie grać przy tym stole? (max 7)")
        n_players = int(input())
        while(n_players > 7):
            print("Max liczba graczy: 7. Prosze Poprawić")
            n_players = int(input())

        for i in range(n_players):
            print(f'Podaj imię dla gracza nr{i+1}: ')
            name = input()
            self.players.append(Player(name))
        isPlaying = 1
        while(isPlaying):
            print("Gra sie rozpoczyna")
            game = Game(self.players, self.dealer)
            game.start()
            self.logs[game.id] = game.logs
            print("Czy chcesz grac dalej?\n-tak (1)\n-nie (0)")
            playAgaian = int(input())
            isPlaying = playAgaian
        print(f"Koniec gry na stole nr {self.id}")
        print(f"Logi ze wszystkich gier: {self.logs}")