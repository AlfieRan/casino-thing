import os
import random
from time import sleep

# THIS CODE WAS NOT WRITTEN BY ME, IT IS BAD, THAT IS WHY I REFACTORED IT

tokens = 1000


def check_bet(bet):
    global tokens

    if bet > tokens:
        print("\n*Isufficient tokens*")
        menu()


def check_tokens():
    global tokens
    if tokens <= 0:
        print("\n\nYou have run out of tokens, your game is over. Thanks for playing!")
        sleep(3)
        quit()


####################################################################################################################################################################################################


deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4


def deal(deck):
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        if card == 11: card = "J"
        if card == 12: card = "Q"
        if card == 13: card = "K"
        if card == 14: card = "A"
        hand.append(card)
    return hand


def play_again(win, bet):
    global tokens

    if win:
        tokens = tokens + bet * 2
    again = input("Do you want to play again? (Y/N) : ").lower()
    if again == "y":
        dealer_hand = []
        player_hand = []
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
        BlackJack()
    else:
        print("Bye!")
        menu()


def total(hand):
    total = 0
    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total


def hit(hand):
    card = deck.pop()
    if card == 11: card = "J"
    if card == 12: card = "Q"
    if card == 13: card = "K"
    if card == 14: card = "A"
    hand.append(card)
    return hand


def clear():
    if os.name == 'nt':
        os.system('CLS')
    elif os.name == 'posix':
        os.system('clear')


def print_results(dealer_hand, player_hand):
    clear()
    print("The dealer has a " + str(dealer_hand) + " for a total of " + str(total(dealer_hand)))
    print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))


def bj(dealer_hand, player_hand):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Congratulations! You got a Blackjack!\n")
        play_again()
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Sorry, you lose. The dealer got a blackjack.\n")
        play_again()


def score(dealer_hand, player_hand, win):
    if total(player_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Congratulations! You got a Blackjack!\n")
        win = True
    elif total(dealer_hand) == 21:
        print_results(dealer_hand, player_hand)
        print("Sorry, you lose. The dealer got a blackjack.\n")
        win = False
    elif total(player_hand) > 21:
        print_results(dealer_hand, player_hand)
        print("Sorry. You busted. You lose.\n")
        win = False
    elif total(dealer_hand) > 21:
        print_results(dealer_hand, player_hand)
        print("Dealer busts. You win!\n")
        win = True
    elif total(player_hand) < total(dealer_hand):
        print_results(dealer_hand, player_hand)
        # print ("Sorry. Your score isn't higher than the dealer. You lose.\n")
    elif total(player_hand) > total(dealer_hand):
        print_results(dealer_hand, player_hand)
        print("Congratulations. Your score is higher than the dealer. You win\n")
        win = True


def BlackJack():
    global tokens
    check_tokens()
    win = False

    choice = 0
    clear()
    print("WELCOME TO BLACKJACK!\n")
    bet = int(input("How much would you like to bet for this game the affect on your winnings is x2: "))
    check_bet(bet)
    tokens = tokens - bet
    dealer_hand = deal(deck)
    player_hand = deal(deck)
    print("The dealer is showing a " + str(dealer_hand[0]))
    print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    bj(dealer_hand, player_hand)
    quit = False
    while not quit:
        choice = input("Do you want to [H]it, [S]tand, or [Q]uit: ").lower()
        if choice == 'h':
            hit(player_hand)
            print("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
            if total(player_hand) > 21:
                print('You busted')
                win = False
                play_again(win, bet)
        elif choice == 's':
            while total(dealer_hand) < 17:
                hit(dealer_hand)
                print(dealer_hand, total(dealer_hand))
                if total(dealer_hand) > 21:
                    print('Dealer busts, you win!')
                    win = True
                    play_again(win, bet)
            score(dealer_hand, player_hand, win)
            play_again(win, bet)
        elif choice == "q":
            print("Bye!")
            quit = True
            menu()

def dice_playagain():
    again = input("Do you want to play again? (Y/N) : ").lower()
    if again == 'y':
        Dice()
    else:
        print("Bye")
        menu()


def dice_roll():
    roll = random.randint(1, 6)
    return roll


def Dice1P():
    global tokens
    bet = int(input("How many tokens would you like to bet?: "))
    check_bet(bet)

    tokens = tokens - bet

    input("Press Enter to continue...")
    player_roll_1 = dice_roll()
    print("You rolled a", player_roll_1)
    input("Press Enter to continue...")
    player_roll_2 = dice_roll()
    print("You rolled a", player_roll_2)

    computer_roll_1 = dice_roll()
    computer_roll_2 = dice_roll()
    print("\n\nComputer rolled a", computer_roll_1, "and a", computer_roll_2)

    player_score = player_roll_1 + player_roll_2
    computer_score = computer_roll_1 + computer_roll_2

    print("\nPlayer scored", player_score)
    print("\nComputer scored", computer_score)

    if player_score > computer_score:
        print("YOU WON", tokens, "tokens")

        win = True
    elif computer_score > player_score:
        print("You lose")

        win = False

    else:

        print("Scores drew , so close yet so far.")
        win = False

    if win == True:
        tokens = tokens + bet * 2


def Dice2P():
    global tokens
    bet = int(input("How many tokens would you like to bet?: "))

    tokens = tokens - bet

    input("Player 1, Press Enter to Roll...")
    player_roll_1 = dice_roll()
    print("\nYou rolled a", player_roll_1)
    input("Player 1, Press Enter to Roll...")
    player_roll_2 = dice_roll()
    print("\nYou rolled a", player_roll_2)

    input("Player 2, Press Enter to Roll...")

    player_roll_3 = dice_roll()
    print("\nYou rolled a", player_roll_3)

    input("Player 2, Press Enter to Roll...")
    player_roll_4 = dice_roll()
    print("\nYou rolled a", player_roll_4)

    player_score = player_roll_1 + player_roll_2
    player2_score = player_roll_3 + player_roll_4

    print("\nPlayer 1 scored", player_score)
    print("Player 2 scored", player2_score)

    if player_score > player2_score:
        print("\nPlayer 1 wins")
        print("YOU WON", tokens, "tokens")

        win = True
    elif player2_score > player_score:
        print("\nPlayer 2 wins")

        win = False

    else:

        print("Scores drew , so close yet so far.")
        win = False

    if win == True:
        tokens = tokens + bet * 2


def Dice():
    global tokens
    check_tokens()
    clear()

    print("WELCOME TO THE DICE GAME!\n")
    playercount = int(
        input("Would you like to play with 1 or 2 players?\n Please note that Player 2 does not bet any tokens.\n: "))

    if playercount == 1:
        Dice1P()
        dice_playagain()

    elif playercount == 2:
        Dice2P()
        dice_playagain()

    else:
        print("Please enter a valid number of players")
        Dice()


#######################################################################################################################################################


slot_results = ['CHERRY', 'LEMON', 'ORANGE', 'PLUM', 'BELL', 'BAR', 'SEVEN']


def slot_play():
    again = input("Do you want to play again? (Y/N) : ").lower()
    if again == 'y':
        slot_machine()
    else:
        print("Bye")
        menu()


def slot_machine():
    global tokens
    check_tokens()
    clear()

    print('''
------------------------------------------------------------------------------------------------------------------------------------------------------

Welcome to the Slot Machine
You have'''' \033', tokens, '\033 ' '''tokens. You'll be asked if you want to play.

To win you must get one of the following combinations:
BAR\tBAR\tBAR\t\tpays\tx250
BELL\tBELL\tBELL/BAR\tpays\tx20
PLUM\tPLUM\tPLUM/BAR\tpays\tx14
ORANGE\tORANGE\tORANGE/BAR\tpays\tx10
CHERRY\tCHERRY\tCHERRY\t\tpays\tx7
CHERRY\tCHERRY\t  -\t\tpays\tx5
CHERRY\t  -\t  -\t\tpays\tx2
7\t  7\t  7\t\tpays\tThe Jackpot! x1000
''')

    bet = int(input("How many tokens would you like to bet?: "))
    check_bet(bet)
    tokens = tokens - bet

    pick1 = random.randint(0, 6)
    slot_roll_1 = slot_results[pick1]

    pick2 = random.randint(0, 6)
    slot_roll_2 = slot_results[pick2]

    pick3 = random.randint(0, 6)
    slot_roll_3 = slot_results[pick3]

    print('''\n\nTHE ROLL IS ''', "|", slot_roll_1, '|\t|', slot_roll_2, '|\t|', slot_roll_3, '|')

    csv_roll = [pick1, pick2, pick3]
    a = 0

    if csv_roll[0] == 0 and csv_roll[1] == 0 and csv_roll[2] == 0:
        tokens = tokens + bet * 7
        print("You won", bet * 6, "tokens")
    elif csv_roll[0] == 0 and csv_roll[1] == 0:
        tokens = tokens + bet * 5
        print("You won", bet * 4, "tokens")

    elif csv_roll[0] == 0 and csv_roll[2] == 0:
        tokens = tokens + bet * 5
        print("You won", bet * 3, "tokens")

    elif csv_roll[1] == 0 and csv_roll[2] == 0:
        tokens = tokens + bet * 5
        print("You won", bet * 4, "tokens")

    elif csv_roll[0] == 0 or csv_roll[1] == 0 or csv_roll[2] == 0:
        tokens = tokens + bet * 2
        print("You won", bet * 1, "tokens")

    f = open("slots.txt", "r")

    while a < 8:
        if f.read(a) == csv_roll:
            if a == 0 or a == 1:
                tokens = tokens + bet * 10
                print("You won", bet * 9, "tokens")
            elif a == 2 or a == 3:
                tokens = tokens + bet * 14
                print("You won", bet * 13, "tokens")
            elif a == 4 or a == 5:
                tokens = tokens + bet * 20
                print("You won", bet * 19, "tokens")
            elif a == 6:
                tokens = tokens + bet * 250
                print("You won", bet * 249, "tokens")
            elif a == 7:
                tokens = tokens + bet * 1000
                print("You won", bet * 999, "tokens")
            a = 8
        else:
            a = a + 1

    slot_play()


###################################################################################################################################################################################################################


red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36}
black = {2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29, 31, 33, 35}
green = 0
even = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36}
odd = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35}


def win_loss(spin, player, bet):
    global tokens
    if spin in red and player == 1:
        print("Spin landed on", spin, "which is red")
        print("\nYOU WON", bet, "tokens")
        tokens = tokens + bet * 2
    elif spin in black and player == 2:
        print("Spin landed on", spin, "which is black")
        print("\nYOU WON", bet, "tokens")
        tokens = tokens + bet * 2
    elif spin in odd and player == 4:
        print("Spin landed on", spin, "which is red")
        print("\nYOU WON", bet, "tokens")
        tokens = tokens + bet * 2
    elif spin in even and player == 5:
        print("Spin landed on", spin, "which is red")
        print("\nYOU WON", bet, "tokens")
        tokens = tokens + bet * 2
    elif spin == green and player == 3:
        print("Spin landed on", spin, "which is red")
        print("\nYOU WON", bet * 35, "tokens")
        tokens = tokens + bet * 36
    elif spin in red:
        print("Spin landed on", spin, "RED")
        print("You lost")
    elif spin in black:
        print("Spin landed on", spin, "BLACK")
        print("You lost")
    elif spin == green:
        print("Spin landed on", spin, "GREEN")
        print("You lost")


def roulette_play():
    again = input("Do you want to play again? (Y/N) : ").lower()
    if again == 'y':
        Roulette()
    else:
        print("Bye")
        menu()


def Roulette():
    global tokens
    check_tokens()
    clear()

    print("\n\n--------------------------------------------------------------")

    print("\n\n\nWELCOME TO ROULETTE!")
    print("You have", tokens, "tokens")

    print('Red = 1 | Bet x2')
    print('Black = 2 | Bet x2')
    print('Green = 3 | Bet x36')
    print('Odd = 4 | Bet x2')
    print('Even = 5 | Bet x2')
    print('-=-=-=-=-=-=-=-=-=-=-')
    player = int(input('Place your choice, 1-5: '))

    if player < 1 or player > 5:
        print("Please enter a valid value")
        Roulette()
    print('-=-=-=-=-=-=-=-=-=-=-')

    bet = int(input("How many tokens would you like to bet?: "))
    check_bet(bet)
    tokens = tokens - bet

    spin = random.randint(0, 36)
    win_loss(spin, player, bet)
    roulette_play()


def menu():
    print("-------------------------------------------------\n"
          "Welcome to the Casino\n"
          "You have", tokens, "tokens\n"
                              "----------------------------------------")
    option = int(input(
        "Please select which game you would like to play\n 1.BlackJack\n 2.Dice\n 3.Routlette\n 4.Slot Machine\n"))

    if option == 1:
        BlackJack()
    elif option == 2:
        Dice()
    elif option == 3:
        Roulette()
    elif option == 4:
        slot_machine()
    else:
        print("Please Enter a valid value")
        menu()


menu()

