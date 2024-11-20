from deck import Deck
from move import Move
from datetime import datetime
from Game_Participants.player import Player

class Game():
    game_count = 0

    def __init__(self, players, dealer):
        Game.game_count += 1
        self.id = Game.game_count
        self.deck = Deck()
        self.players = players
        self.dealer = dealer
        self.dealer.hand = []
        self.logs = []
        for player in players:
            player.hand = []
            player.reward = 0


    def start(self):
        # postawienie zakładów
        self.setBets(self.players)

        # rozdanie kart krupiera
        self.dealerDeal(self.dealer)

        # rozdanie kart graczy
        self.playersDeal(self.players)

        # decyzje każdego gracza
        self.playerGame(self.players, self.dealer)

    def setBets(self, players):
        for player in players:
            print(f"Zakład gracza {player.name}: ")
            player.initial_bet = int(input())
            player.money -= player.initial_bet

    def playersDeal(self, players):
        for player in players:
            player.hand.extend(self.deck.deal_cards(2))

    def dealerDeal(self, dealer):
        dealer.hand.extend(self.deck.deal_cards(2))
        print(f"Karta krupiera: {self.dealer.hand[0]} [X]")

    def playerGame(self, players, dealer):
        for player in players:
            player.points = 0

            doesPlayerHasBlackJack = self.isBlackJack(player.hand)
            player.isBlackJack = doesPlayerHasBlackJack
            if(doesPlayerHasBlackJack):
                player.points = 21

            doesDealerHasBlackJack = self.isBlackJack(dealer.hand)
            dealer.isBlackJack = doesDealerHasBlackJack
            if(doesDealerHasBlackJack):
                dealer.points = 21

            player.points = self.countPoints(player.hand)
            dealer.points = self.countPoints(dealer.hand)


            if(player.points == 21):
                self.logs.append(f"{self.getCurrentTime()} - {player.name} BlackJack")

            while (player.points == 21 and self.dealer.hand[0][0] == 'A'):
                selectedOption = self.getDecision(player)
                self.logs.append(f"{self.getCurrentTime()} - {player.name} wybrał ruch: {selectedOption.name}")
                if selectedOption == Move.STAND:
                    break
                elif selectedOption == Move.EVEN_MONEY:
                    player.even_money = True
                    break
                else:
                    print("\nTa opcja jest niedostepna. Prosze wybrac dostępną opcję\n")

            while (player.points < 21):
                insuranceTaken = False
                selectedOption = self.getDecision(player)
                self.logs.append(f"{self.getCurrentTime()} - {player.name} wybrał ruch: {selectedOption.name}")

                if selectedOption == Move.HIT:
                    player.hand.extend(self.deck.deal_cards(1))
                    player.points = self.countPoints(player.hand)

                elif selectedOption == Move.STAND:
                    player.points = self.countPoints(player.hand)
                    break

                elif selectedOption == Move.DOUBLE:
                    if (self.isDoubleAvailable(player.hand)):
                        player.initial_bet *= 2
                        player.hand.extend(self.deck.deal_cards(1))
                        player.points = self.countPoints(player.hand)
                        break
                    else:
                        print('\nDouble jest niedostępny, prosze wybrać inną opcję\n')
                        continue

                elif selectedOption == Move.SPLIT:
                    if(self.isSplitAvailable(player.hand) and not player.twoHandGame):
                        player.hand.pop()
                        player.hand.extend(self.deck.deal_cards(1))
                        player.points = self.countPoints(player.hand)
                        current_player_index = players.index(player)
                        second_hand_player = self.splitCards(player.hand, player)
                        players.insert(current_player_index + 1, second_hand_player)
                    else:
                        print('\nSplit jest niedostępny, prosze wybrać inną opcję\n')
                        continue

                elif selectedOption == Move.INSURANCE:
                    if (self.isInsuranceAvailable(player.hand) and not insuranceTaken):
                        player.insurance_taken = True
                        half_wager = player.initial_bet / 2
                        player.money -= half_wager
                        print('\nWybrano Insurance na wypadek BlackJacka u krupiera\n')
                        print(f'\nStawka Insurance: {half_wager}\n')
                        continue
                    else:
                        print('\nInsurance jest niedostępny, prosze wybrać inną opcję\n')
                        continue

                elif selectedOption == Move.EVEN_MONEY:
                    print('\nEven Money jest niedostępny, prosze wybrać inną opcję\n')
                    continue

                elif selectedOption == Move.SURRENDER:
                    player.points = 0
                    break

            print(f"Karty gracza {player.name}: {player.hand}")
            print(f"Punkty: {player.points}")
            print("\n-----------------------------\n")

        self.checkDealer(dealer)
        for i, player in enumerate(players):
            self.checkResult(player, dealer)
            if player.twoHandGame:
                players[i-1].reward += player.reward
                players.pop(i)
        for player in players:
            print(f"Wygrana gracza {player.name}: {player.reward}")


    def checkResult(self, player, dealer):
        if (player.points > 21):
            self.dealerWin(player, dealer)
        elif (player.even_money == True):
            self.evenMoney(player)
        else:
            if (dealer.isBlackJack):
                if (player.insurance_taken):
                    self.insurance_win(player, dealer)
                elif (player.isBlackJack):
                    self.push(player)
                else:
                    self.dealerWin(player, dealer)
            elif (player.isBlackJack):
                if (dealer.isBlackJack):
                    self.push(player)
                else:
                    self.playerWin(player, dealer)
            elif (player.insurance_taken):
                self.insurance_lose(player)
            elif (dealer.points > 21):
                self.playerWin(player, dealer)
            elif (player.points < dealer.points):
                self.dealerWin(player, dealer)
            elif (player.points > dealer.points):
                self.playerWin(player, dealer)
            elif (player.points == dealer.points):
                self.push(player)

    def checkDealer(self, dealer):
        while (dealer.points < 17):
            dealer.hand.extend(self.deck.deal_cards(1))
            dealer.points = self.countPoints(dealer.hand)
        print(f"Punkty krupiera: {dealer.points}")
        print(f"Karty krupiera: {dealer.hand}")

    def push(self, player):
        self.logs.append(f"{self.getCurrentTime()} - push {player.name}")
        player.reward += player.initial_bet
        player.money += player.reward

    def insurance_win(self, player, dealer):
        player.reward += player.initial_bet * 2
        player.money += player.reward
        dealer.money -= player.initial_bet / 2
        self.logs.append(f"{self.getCurrentTime()} - insurance won {player.name}")

    def insurance_lose(self, player):
        self.logs.append(f"{self.getCurrentTime()} - insurance lost {player.name}")

    def evenMoney(self, player):
        print(f"Even money: {player.name}")
        self.logs.append(f"{self.getCurrentTime()} - even money {player.name}")
        player.reward += player.initial_bet
        player.money += player.reward

    def playerWin(self, player, dealer):
        player.reward += player.initial_bet * 2
        player.money += player.reward
        dealer.money -= player.initial_bet
        self.logs.append(f"{self.getCurrentTime()} - wygrana gracza {player.name}")

    def dealerWin(self, player, dealer):
        player.money -= player.initial_bet
        dealer.reward += player.initial_bet
        dealer.money += dealer.reward
        self.logs.append(f"{self.getCurrentTime()} - przegrana gracza {player.name}")

    def countPoints(self, cards):
        points = 0
        aces = 0

        for card in cards:
            if card[0] == 'A':
                aces += 1
            else:
                points += self.deck.points[card[0]]

        for _ in range(aces):
            if points + self.deck.points['A'][1] <= 21:
                points += self.deck.points['A'][1]
            else:
                points += self.deck.points['A'][0]

        return points


    def getDecision(self, player):
        print(f"Karty gracza {player.name}: {player.hand}")
        print(f"Punkty: {player.points}")
        print(f"Decyzja gracza: {player.name}")
        options = Move.getAllOptions()
        selectedOption = self.promptUser(options, player.hand)
        decision = Move(selectedOption)
        print(f"{player.name} wybrał ruch: {decision.name}")
        return decision


    def promptUser(self, options, cards):
        print("Dostępne opcje:")
        if(self.isBlackJack(cards)):
            print("Do you want Even Money?")
            print(f"2: STAND")
            print(f"6: EVEN_MONEY")
        else:
            for index, option in options:
                if option == 'DOUBLE':
                    if(self.isDoubleAvailable(cards)):
                        print(f"{index}: {option}")
                elif option == 'INSURANCE':
                    if(self.isInsuranceAvailable(cards)):
                        print(f"{index}: {option}")
                elif option == 'SPLIT':
                    if(self.isSplitAvailable(cards)):
                        print(f"{index}: {option}")
                elif option == 'EVEN_MONEY':
                    continue
                else:
                    print(f"{index}: {option}")

        while True:
            try:
                selectedIndex = int(input("Wybierz numer opcji: "))
                if selectedIndex < 1 or selectedIndex > len(options):
                    print("Nieprawidłowy numer opcji. Wybierz ponownie.")
                else:
                    return options[selectedIndex - 1][0]
            except ValueError:
                print("Wprowadzona wartość nie jest liczbą. Wybierz ponownie.")

    def splitCards(self, cards, player):
        player2 = Player(f"{player.name}2")
        player2.hand.append(cards[1])
        player2.hand.extend(self.deck.deal_cards(1))
        player2.points = self.countPoints(player.hand)
        player2.twoHandGame = True
        player2.initial_bet = player.initial_bet
        player.money -= player.initial_bet
        return player2

    def isBlackJack(self, cards):
        if len(cards) != 2:
            return False
        if cards[0][0] == 'A':
            if cards[1][0] in ['10', 'J', 'Q', 'K']:
                return True
        if cards[0][0] in ['10', 'J', 'Q', 'K']:
            if cards[1][0] == 'A':
                return True
        return False
    def isSplitAvailable(self, cards):
        if(len(cards) == 2):
            if(cards[0][0] == cards[1][0]):
                return True
        else:
            return False
    def isDoubleAvailable(self, cards):
        if(len(cards) == 2):
            return True
        else:
            return False
    def isInsuranceAvailable(self, cards):
        if(len(cards) == 2):
            if(self.dealer.hand[0][0] == 'A'):
                return True
        else:
            return False
    def isEvenMoneyAvailable(self, cards):
        if(len(cards) == 2):
            if(self.isBlackJack(cards) and self.dealer.hand[0][0] == 'A'):
                return True
        else:
            return False
    def getCurrentTime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")