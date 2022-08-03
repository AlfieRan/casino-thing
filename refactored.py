import time
import os
import random

# THIS FILE IS WRITTEN BY ME - NOT MY BEST WORK BUT NOT BAD FOR 2 HOURS


def clear():
    if os.name == 'nt':  # windows
        os.system('CLS')
    elif os.name == 'posix':  # macos & linux
        os.system('clear')
    else:
        print("\n" * 50)
        # this is incase the programming is running on a different OS or a different shell - like pycharm


def total(hand):
    count = 0
    aces = 0
    for card in hand:
        if card == "A":
            aces += 1
        elif card in ["J", "Q", "K"]:
            count += 10
        else:
            count += card

    if aces == 2:
        return 12
    elif aces == 1:
        if count < 11:
            return count + 11
        else:
            return count + 1
    else:
        return count


def print_bj_hands(dealer_hand, player_hand):
    clear()
    print(f"The dealer has {dealer_hand} for a total {total(dealer_hand)}"
          f"\n You have {player_hand} for a total of {total(player_hand)}")


def check_for_bj(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_bj_hands(dealer_hand, player_hand)
        print("You got a BlackJack! Congratulations you Win!")
        return [True, True]  # Player won, return [game ended, player won]

    elif total(dealer_hand) == 21:
        print_bj_hands(dealer_hand, player_hand)
        print("The dealer got a BlackJack, that means you lose :(")
        return [True, False]  # Dealer won, return [game ended, dealer won]

    else:
        return [False, False]  # no-one won, return [game not ended, no-one won]


def score_bj(dealer_hand, player_hand, win):
    print_bj_hands(dealer_hand, player_hand)
    if total(player_hand) <= total(dealer_hand):
        print("\nThis means you lost :( \n")
        return False
    else:
        print("\nThis means you won!\n")
        return True


def dice_roll():
    roll = random.randint(1, 6)
    return roll


def get_rolls(roll_count, person=None):
    rolls = []

    if person is None:
        prefix = ""
    else:
        prefix = f"{person}, "

    for i in range(roll_count):
        input(f"{prefix}Press Enter to roll the dice...")
        rolls.append(dice_roll())
        print(f"{prefix}You rolled a {rolls[i]}")

    return rolls


def parse_combo_item(item: [str]):
    if len(item) == 1:
        return item[0]
    elif len(item) == 2:
        return f"{item[0]}/{item[1]}"
    else:
        raise f"Unknown data: {item} fed into item parser for slot machine"


def wrap_combos(item, combinations):
    if item == ["ANY"]:
        return combinations
    else:
        return item


def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False


class Casino:
    full_deck = [x for x in range(2, 15)] * 4

    # INITIALISATION AND MAIN STUFF

    def __init__(self, start_tokens=1000):
        self.tokens = start_tokens
        self.modes = [
            {"name": "1. Blackjack", "function": self.black_jack},
            {"name": "2. Dice", "function": self.dice},
            {"name": "3. Roulette", "function": self.roulette},
            {"name": "4. Slot Machine", "function": self.slot_machine},
            {"name": "5. Quit", "function": quit}
        ]
        self.deck = self.full_deck

        self.menu()

    def menu(self):
        print(f"{'-' * 10}\nWelcome to the Casino\n You have {self.tokens} tokens\n{'-' * 10}"
              f"\n\nPlease selectwhat you would like to do:")

        for mode in self.modes:
            print(f"{mode['name']}")

        option = int(input())

        if len(self.modes) + 1 >= option > 0:  # add one to deal with 0 indexing
            self.modes[option - 1]['function']()
        else:
            print("Please Enter a valid value")
            self.menu()

    def menu_check(self, depth=0):
        return_to_menu = str(input("Would you like to return to the Menu? (yes/no)")).lower()
        if return_to_menu == "yes" or return_to_menu == "y" or depth > 5:
            # depth is used here to prevent recursion if the user just doesn't understand how to write yes or no
            self.menu()
        elif return_to_menu == "no" or return_to_menu == "n":
            return False
        else:
            print("That was not an option, please answer yes or no.")
            return self.menu_check(depth=depth + 1)

    # GAMES START HERE

    def black_jack(self):
        self.check_tokens()

        clear()
        print("WELCOME TO BLACKJACK!\n")
        bet = self.get_bet()

        if not self.check_bet(bet):
            # if the user does not have enough tokens to make this bet then check if they want to go to the menu
            if not self.menu_check():
                # if they don't, then recall this function to let them make a new bet
                self.black_jack()

        self.tokens -= bet
        dealer_hand = self.deal()
        player_hand = self.deal()
        print(f"The dealer is showing a {dealer_hand[0]}, "
              f"You have {player_hand} for a total of {total(player_hand)}")

        [game_ended, win] = check_for_bj(dealer_hand, player_hand)
        while not game_ended:
            choice = input("Do you want to [H]it, [S]tand, or [Q]uit to menu (you will lose your bet): ").lower()

            if choice == 'h':
                player_hand = self.deal(1, player_hand)
                print(f"You have {player_hand} for a total of {total(player_hand)}")

                if total(player_hand) > 21:
                    print_bj_hands(dealer_hand, player_hand)
                    print('\nYou went bust, meaning you lost :(\n')
                    win = False
                    game_ended = True

            elif choice == 's':
                while total(dealer_hand) < 17 and not game_ended:
                    dealer_hand = self.deal(1, dealer_hand)
                    print(f"The dealer has {dealer_hand} for a total of {total(dealer_hand)}")

                    if total(dealer_hand) > 21:
                        print_bj_hands(dealer_hand, player_hand)
                        print('\nDealer busts, you win!\n')
                        win = True
                        game_ended = True

                win = score_bj(dealer_hand, player_hand, win)
                game_ended = True

            elif choice == "q":
                print("Bye!")
                self.menu()

        if win:
            self.tokens += bet * 2
        self.play_again(self.black_jack)

    def dice(self, recursion=0):
        self.check_tokens()
        clear()

        player_count = int(input(
            "WELCOME TO THE DICE GAME!\n"
            "Would you like to play with 1 or 2 players?\n Please note that Player 2 does not bet any tokens.\n "))

        bet = self.get_bet()

        if player_count == 1:
            self.dice_1_player(bet)
            self.play_again(self.dice)

        elif player_count == 2:
            self.dice_2_player(bet)
            self.play_again(self.dice)

        else:
            if recursion > 5:
                self.menu()
            print("Please enter a valid number of players")
            self.dice(recursion=recursion + 1)

    def roulette(self):
        self.check_tokens()
        clear()

        print(f'{"-=" * 10}-')

        print("\n\n\nWELCOME TO ROULETTE!"
              f"You have {self.tokens} tokens"
              "In roulette you can win either 2 times your bet or 36 times!")

        bet = self.get_bet()

        print('You can make place your bet on the following:'
              '\n1. Red   | Bet x2'
              '\n2. Black | Bet x2'
              '\n3. Green | Bet x36'
              '\n4. Odd   | Bet x2'
              '\n5. Even  | Bet x2'
              f'{"-=" * 10}-')

        player = int(input("Which would you like to bet on, 1-5? "))

        if player < 1 or player > 5:
            print("Please enter a valid value")
            self.roulette()

        print(f'{"-=" * 10}-')

        spin = random.randint(0, 36)
        self.check_if_won(player, spin, bet)
        self.play_again(self.roulette)

    def slot_machine(self):
        self.check_tokens()
        slot_results = ['CHERRY', 'LEMON', 'ORANGE', 'PLUM', 'BELL', 'BAR', 'SEVEN']

        possible_combos = [
            {"combo": [["SEVEN"], ["SEVEN"], ["SEVEN"]], "payout": "1000"},
            {"combo": [["BAR"], ["BAR"], ["BAR"]], "payout": "250"},
            {"combo": [["BELL"], ["BELL"], ["BELL", "BAR"]], "payout": "20"},
            {"combo": [["PLUM"], ["PLUM"], ["PLUM", "BAR"]], "payout": "14"},
            {"combo": [["ORANGE"], ["ORANGE"], ["ORANGE", "BAR"]], "payout": "10"},
            {"combo": [["CHERRY"], ["CHERRY"], ["CHERRY"]], "payout": "7"},
            {"combo": [["CHERRY"], ["CHERRY"], ["ANY"]], "payout": "5"},
            {"combo": [["CHERRY"], ["ANY"], ["ANY"]], "payout": "2"},
        ]

        clear()

        print(f"{'-' * 10}"
              f"\nWelcome to the Slot Machine "
              f"\nYou have \033 {self.tokens} \033 tokens. "
              f"\nTo win you must get one of the following combinations:")

        for combo in possible_combos:
            table = ""
            for item in combo["combo"]:
                item_str = parse_combo_item(item)
                if len(item_str) >= 7:
                    table += item_str
                else:
                    table += f"{item_str} \t"

            if combo["payout"] == "1000":
                extra = "The Jackpot! "
            else:
                extra = ""

            print(f"{table} \t pays \t x{combo['payout']} {extra}")

        bet = self.get_bet()

        slot_rolls = [slot_results[random.randint(0, 6)] for i in range(3)]

        print('''\n\nTHE ROLL IS ''', "|", slot_rolls[0], '|\t|', slot_rolls[1], '|\t|', slot_rolls[2], '|')

        found_combo = False
        for combo in possible_combos:
            if found_combo:
                break

            for i in range(3):
                if (slot_rolls[0] in wrap_combos(combo["combo"][i % 3], slot_results)
                        and slot_rolls[1] in wrap_combos(combo["combo"][(i + 1) % 3], slot_results)
                        and slot_rolls[2] in wrap_combos(combo["combo"][(i + 2) % 3], slot_results)):
                    print(f"Congratulations you just won {bet * int(combo['payout'])} tokens!")
                    self.tokens += bet * int(combo['payout'])
                    found_combo = True
                    break

        if not found_combo:
            print(f"Sorry you didn't win this time, you lost {bet} tokens.")

        self.play_again(self.slot_machine)

    # GENERAL FUNCTIONS

    def get_bet(self, recursion=0):
        try:
            bet = int(input("How many tokens would you like to bet?: "))
            self.check_bet(bet)
            self.tokens -= bet
            return bet

        except ValueError:
            print("That is not a valid number, please try again.")
            return self.get_bet(recursion=recursion + 1)

    def check_tokens(self):
        if self.tokens <= 0:
            print("\n\nYou have run out of tokens, your game is over. Thanks for playing!")
            time.sleep(3)
            quit()

    def check_bet(self, bet):
        if bet > self.tokens:
            print("\n*Insufficient tokens*")
            return False
        else:
            return True

    def play_again(self, function_to_run, recursion=0):
        again = input(f"You now have {self.tokens} tokens.\nDo you want to play again? (Y/N) : ").lower()

        if again in ["y", "yes"]:
            function_to_run()

        elif again in ["n", "no"]:
            print("Bye!")
            self.menu()

        else:
            if recursion > 5:
                self.menu()
            else:
                print("That was not an option, please try again.")
                self.play_again(function_to_run, recursion=recursion + 1)

    # BLACKJACK SUB-FUNCTIONS

    def deal(self, amount=2, hand=None):
        if hand is None:
            hand = []

        for i in range(amount):
            random.shuffle(self.deck)
            card = self.deck.pop()
            if 10 < card < 15:
                card = str(card).replace("11", "J").replace("12", "Q").replace("13", "K").replace("14", "A")
            elif card > 14:
                raise "card generated was above 14, which shouldn't happen, deck is probably be generating wrong"
            hand.append(card)
        return hand

    # DICE SUB FUNCTIONS

    def dice_1_player(self, bet):
        rolls = 2
        player_score = sum(get_rolls(2))
        computer_rolls = [dice_roll() for i in range(rolls)]
        computer_score = sum(computer_rolls)

        print(f"\n\nComputer rolled a {computer_rolls[0]} and a {computer_rolls[1]}")

        print(f"\nPlayer scored: {player_score}"
              f"\nComputer scored: {computer_score}")

        self.score_dice(player_score, computer_score, bet)

    def dice_2_player(self, bet):
        rolls = 2
        player_1_score = sum(get_rolls(rolls, "Player 1"))
        player_2_score = sum(get_rolls(rolls, "Player 2"))

        print(f"\nPlayer 1 scored: {player_1_score}"
              f"\nPlayer 2 scored: {player_2_score}")

        self.score_dice(player_1_score, player_2_score, bet)

    def score_dice(self, player_score: int, other_score: int, bet: int):
        if player_score > other_score:
            print("\nPlayer 1 wins"
                  f"\nPlayer 1 WON {bet * 2} tokens")
            self.tokens += bet * 2

        elif player_score > other_score:
            print(f"\nPlayer 2 wins, Player 1 lost {bet} tokens")

        else:
            print("Scores drew , so close yet so far. Player 1's bet was refunded")
            self.tokens += bet

    # ROULETTE SUB FUNCTIONS
    def check_if_won(self, player, spin, bet):
        red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36}
        black = {2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35}
        green = 0

        if spin in red:
            colour = "red"
        elif spin in black:
            colour = "black"
        else:
            colour = "green"

        print(f"The spin was {spin} which is {colour}.")
        won = True

        if player == 1 and spin in red:
            reason = "red"
        elif player == 2 and spin in black:
            reason = "black"
        elif player == 4 and is_even(spin):
            reason = "even"
        elif player == 5 and not is_even(spin):
            reason = "odd"
        else:
            won = False

        if won:
            self.tokens += bet * 2
            print(f"Congratulations, because you bet {reason} that means you won {bet}!")

        elif player == 3 and spin == green:
            print(f"Congratulations, you bet green and it was green!!!\nYou just won {bet*35}")
            self.tokens += bet * 36
            won = True

        if not won:
            print("Sorry you did not win anything this time")
            return False

        return True


Casino()
