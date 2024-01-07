import random

class BlackjackGame:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.player_value = 0
        self.dealer_hand = []
        self.dealer_value = 0

    def create_deck(self):
        suits = ['♥', '♦', '♣', '♠']
        ranks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 0}
        deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks.items()]
        random.shuffle(deck)
        return deck

    def deal_card(self):
        return self.deck.pop()

    def calculate_hand_value(self, hand):
        total_value = 0
        num_aces = 0

        for card in hand:
            (rank, value) = card['rank']
            if value == 0:
                num_aces += 1
                total_value += 11
            else:
                total_value += value

        while total_value > 21 and num_aces:
            total_value -= 10
            num_aces -= 1

        return total_value

    def display_card(self, hand, add_back_side = False):
        if len(hand) == 0:
            return ""

        card_top = "┌───────┐"
        card_strings = [
                f"│ {card['rank'][0]:<2}{card['suit']}   │" for card in hand
        ]
        last_card = [
                "│       │",
                "│       │",
                "│       │",
                "└───────┘"
        ]
        back_side = [
            "┌───────┐",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "│░░░░░░░│",
            "└───────┘"
        ]
        if add_back_side:
            card_strings.append(back_side[1])
            last_card = back_side[2:]

        result = []
        for i, card in enumerate(card_strings):
            margin1 = ''.join(['│' if i - j < 3 else ' ' for j in range(i)])
            margin2 = ''.join([('└' if i - j == 2 else '│') 
                               if i - j < 3 else ' ' for j in range(i)])
            result.append(margin1 + card_top)
            result.append(margin2 + card)

        i = len(card_strings) - 1
        margin1 = ''.join([
            '│' if i + 1 - j < 3 else ' ' for j in range(i)
        ])
        margin2 = ''.join([
            ('└' if i + 1 - j == 2 else '│') 
            if i + 1 - j < 3 else ' ' for j in range(i)
        ])
        margin3 = ''.join([
            '│' if i + 2 - j < 3 else ' ' for j in range(i)
        ])
        margin4 = ''.join([
            ('└' if i + 2 - j == 2 else '│') 
            if i + 2 - j < 3 else ' ' for j in range(i)
        ])

        result.append(margin1 + last_card[0])
        result.append(margin2 + last_card[1])
        result.append(margin3 + last_card[2])
        result.append(margin4 + last_card[3])
        return '\n'.join(result)

    def display_game_state(self, reveal_dealer_card=False):
        print(f"\nPlayer's Hand (Value: {self.player_value}):")
        print(self.display_card(self.player_hand))

        print(f"\nDealer's Hand (Value: {self.dealer_value}):")
        if reveal_dealer_card:
            print(self.display_card(self.dealer_hand))
        else:
            print(self.display_card([self.dealer_hand[0]], add_back_side=True))

    def play(self):
        # Initial deal
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

        self.player_value = self.calculate_hand_value(self.player_hand)
        self.dealer_value = self.calculate_hand_value([self.dealer_hand[0]])

        blackjack = self.player_value == 21

        # Player's turn
        while self.player_value < 21:
            self.display_game_state()
            player_choice = input("Do you want to hit(h) or stand(s)? ").lower()

            if player_choice == 'hit' or player_choice == 'h':
                self.player_hand.append(self.deal_card())
                self.player_value = self.calculate_hand_value(self.player_hand)

                if self.player_value > 21:
                    break
            elif player_choice == 'stand' or player_choice == 's':
                break
            else:
                print("Invalid choice. Please enter 'hit' or 'stand'.")

        # Dealer's turn
        self.dealer_value = self.calculate_hand_value(self.dealer_hand)
        if self.player_value <= 21:
            while self.dealer_value < 17:
                self.dealer_hand.append(self.deal_card())
                self.dealer_value = self.calculate_hand_value(self.dealer_hand)

        # Display final results
        self.display_game_state(reveal_dealer_card=True)

        if blackjack and self.dealer_value != 21:
            print("Blackjack! You win x3/2")
            return

        if self.dealer_value > 21 or \
            (self.player_value <= 21 and self.player_value > self.dealer_value):
            print("Congratulations! You win!")
        elif self.player_value == self.dealer_value:
            print("Nobody wins.")
        else:
            print("Dealer wins. Try again.")

if __name__ == "__main__":
    blackjack_game = BlackjackGame()
    blackjack_game.play()

