# (c) 2018 Tingda Wang
# terminal blackjack game with betting

import random

SUITS = ('♠', '♥', '♦', '♣')

RANK = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

# risk-taking ability of dealer, increases with higher value
RISK_FACTOR = 500

# starting number of chips to bet on
STARTING_CHIPS = 500

class Card():
    ''' card class denoting the suit and rank '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def __str__(self):
        ''' pretty prints the card in terminal '''
        return '%s %s ' %(self.suit, self.rank)

class Hand():
    ''' hand class storing cards in class and their value '''
    def __init__(self):
        self.hand = []
        self.ace = 0 # used to adjust ace value, stores number of aces at 11
        self.value = 0
        self.twentyone = False
        
    def deal(self, cards):
        ''' deals cards to hand '''
        for card in cards:
            self.receive(card)
            
    def receive(self, card):
        ''' receives card and updates total card value and twentyone status '''
        self.hand.append(card)
        
        if card.rank == 'A':

            if self.value < 11:
                self.ace += 1
                self.value += 11
            else:
                self.value += 1
        else:
            self.value += RANK[card.rank]

            # see we have to lower ace value
            while self.value > 21 and self.ace > 0:
                self.value -= 10
                self.ace -= 1 # ace no longer at 11

        if self.value == 21:
            self.twentyone = True
            
    def get_value(self):
        return self.value

    def __str__(self):
        ''' returns string of cards '''
        ls = [str(card) for card in self.hand]
        return "\n".join(ls)
    
class Deck():
    ''' stores all cards in deck shuffled '''
    
    def __init__(self):
        self.deck = [Card(suit, r) for suit in SUITS for r in RANK.keys()]

        # shuffle deck
        random.shuffle(self.deck)

    def draw(self):
        ''' draws card '''
        return self.deck.pop()

    def draw_cards(self, n):
        ''' draws multiple cards '''
        return [self.deck.pop() for _ in range(n)]

    def __repr__(self):
        ''' For debugging, returns string of entire deck '''
        ls = []
        for i, card in enumerate(self.deck):
            ls.append("%d: %s" %(i,card))

        return "\n".join(ls)
            
class Dealer():
    ''' 
    Dealer class to facilitate card dealing
    Dealer AI also intelligently decides whether to deal to self
    based on risk averseness and hands
    '''
    
    def __init__(self, dealer_risk = RISK_FACTOR):
        self.deck = Deck()
        self.dealer_hand = Hand()
        self.player_hand = Hand()
        self.risk = dealer_risk
        
    def start(self):
        ''' deals starting hands '''
        # deal 2 cards to player
        for card in self.deck.draw_cards(2):
            self.player_hand.receive(card)

        # deal 2 cards to dealer
        for card in self.deck.draw_cards(2):
            self.dealer_hand.receive(card)

    def blackjack(self):
        ''' determines whether either player has gotten a blackjack (21)'''
        if self.dealer_hand.twentyone and self.player_hand.twentyone:
            return 2
        elif self.dealer_hand.twentyone:
            return -1
        elif self.player_hand.twentyone:
            return 1
        else:
            return 0
        
    def print_hand(self, dealer = True, player = True):
        """ pretty prints the hands of either or both player """
        if dealer:
            print("---Dealer hand---")
            print(self.dealer_hand)
        if player:
            print("---Player Hand---")
            print(self.player_hand)
            
    def deal_player(self):
        ''' deals to the player '''
        self.player_hand.receive(self.deck.draw())
        self.print_hand(dealer = False)
        if self.player_hand.twentyone:
            return 1
        elif self.player_hand.get_value() > 21:
            return -1
        else:
            return 0

    def compare_hands(self):
        ''' compares hands of dealer and player '''
        res = self.blackjack()

        if res == 1:
            print("Player has Blackjack, player wins!")
            return 1
        elif res == -1:
            print("Dealer has Blackjack, player loses...")
            return -1
        elif res == 2:
            print("Two Blackjacks! A draw! Bet returned to player")
            return 0
        else: # no blackjacks, compare who is closer
            if self.player_hand.get_value() > self.dealer_hand.get_value():
                print("Player has bigger hand. Player wins!")
                return 1
            elif self.player_hand.get_value() < self.dealer_hand.get_value():
                print("Dealer has bigger hand. Player loses...")
                return -1
            elif self.player_hand.get_value() == self.dealer_hand.get_value():
                print("Same value for both hands! A draw. Bet returned to player")
                return 0
            
        
    def deal_self(self):
        ''' dealer deals to itself '''

        print("Dealer's turn to play...")

        while True:
            if self.dealer_hand.get_value() < 10: # hits regardless
                self.dealer_hand.receive(self.deck.draw())
                self.print_hand(player = False)
            else: # desides based on riskiness and risk taking tendency of dealer
                # get risk factor based on hand
                n = 2 if self.dealer_hand.get_value() < 15 else 4 if self.dealer_hand.get_value() < 20 else 8
                num = random.randint(1, 1000)
                if num < self.risk // n:
                    print("Dealer hits!")
                    self.dealer_hand.receive(self.deck.draw())
                    self.print_hand(player = False)

                    if self.dealer_hand.get_value() > 21: # bust
                        print("Dealer busts! Player wins the round!")
                        return 1
                    elif self.dealer_hand.get_value() == 21:
                        print("Dealer BlackJack!")
                        return self.compare_hands()
                else:
                    print("Dealer stands!\nComparing hands...")
                    return self.compare_hands()

        
        
class Game():
    ''' main game class that runs each round of the game '''

    def __init__(self):
        ''' initiates game and starting menu '''
        
        print("===== Welcome to ♠ BlackJack =====")

        # starting number of chips to bet on
        self.chips = STARTING_CHIPS

        # determines player response
        q = False
        while (not q):

            if self.chips == 0:
                print("No more chips, ending game...")
                exit()
            else:
                print("You have %d chips.\n" %self.chips)
                
            start = input("Press s to start or q to quit\n")

            if start == 's':
                self.dealer = Dealer()
                self.main()
            elif start == 'q':
                print("Quitting game...")
                q = True

        exit()
    
    def main(self):
        ''' Main game loop '''
        
        print("Starting game...\n")

        bet = 0

        # getting the bet
        while bet == 0:
            try:
                bet = int(input("You have %d chips. Place your bet: " %self.chips))

                if bet > self.chips:
                    print("Insufficient chips, try again")
                    bet = 0
                elif bet < 1:
                    print("Must least 1 chip, try again")
                    
            except ValueError:
                print("Invalid input, a real number please")

        
        # deal starting hand
        self.dealer.start()

        # print starting hands
        self.dealer.print_hand()

    
        # check for blackjack
        winner = self.dealer.blackjack()

        # determine if blackjack
        if winner == 0: # no winners yet

            bust = False
            
            # player decides to hit or stand
            while True:
                hit = input("Hit or Stand?\n(Press enter to hit, other key to stand)\n")

                if hit == '':
                    # deal card
                    result = self.dealer.deal_player()
                    
                    if result == 1: # win
                        print("BlackJack! Dealer moves...")
                        break
                    elif result == -1: # bust
                        print("Bust! Dealer wins...")
                        self.chips -= bet
                        bust = True
                        break
                else:
                    break

            if not bust:
                # dealer moves
                result = self.dealer.deal_self()
                # update bet
                self.chips += result * bet
                
        elif winner == 1: # player won
            print("BlackJack! Player Wins!")
            self.chips += bet
            
        elif winner == -1: # player lost
            print("BlackJack! Dealer wins...")
            self.chips -= bet
            
        else: # draw
            print("WOW! Two BlackJacks! A draw, bet returned to player")

                
if __name__ == "__main__":

    game = Game()
