import random
import db


def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10,
              'King': 10, 'Ace': 11}

    deck = [[suit, rank, values[rank]] for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


def deal_card(hand, deck):
    hand.append(deck.pop())


def hand_value(hand):
    value = sum(card[2] for card in hand)
    aces = sum(1 for card in hand if card[1] == 'Ace')

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value


def display_hand(hand, hide_first_card=False):
    if hide_first_card:
        print("DEALER'S SHOW CARD:", end=" ")
        cards = hand[1:]
    else:
        cards = hand

    for card in cards:
        print(f"{card[1]} of {card[0]}", end=" ")
    print()


def main():
    player_money = db.read_money()
    print("\nBLACKJACK!")
    print("Blackjack payout is 3:2\n")
    while player_money >= 5:
        print(f"Money: ${player_money:.2f}")

        try:
            bet = float(input("Bet amount: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if bet < 5 or bet > 1000:
            print("Invalid bet amount. Minimum bet is 5 and maximum is 1000.")
            continue
        elif bet > player_money:
            print("Insufficient funds.")
            continue

        deck = create_deck()
        player_hand = []
        dealer_hand = []

        deal_card(player_hand, deck)
        deal_card(player_hand, deck)
        deal_card(dealer_hand, deck)
        deal_card(dealer_hand, deck)

        print("\nPlayer's hand:")
        display_hand(player_hand)
        print("\nDealer's hand:")
        display_hand(dealer_hand, hide_first_card=True)

        player_value = hand_value(player_hand)
        dealer_value = hand_value(dealer_hand)
        player_blackjack = player_value == 21
        dealer_blackjack = dealer_value == 21

        if player_blackjack and dealer_blackjack:
            print("Both you and the dealer have Blackjack! It's a push.")
        elif player_blackjack:
            print("Blackjack! You win!")
            payout = 1.5 * bet
            player_money += round(payout, 2)
        elif dealer_blackjack:
            print("Dealer has Blackjack. You lose.")
            player_money -= bet
        else:
            while True:
                move = input("\nHit or Stand? (hit/stand): ").lower()
                if move == 'hit':
                    deal_card(player_hand, deck)
                    player_value = hand_value(player_hand)
                    print("\nPlayer's hand:")
                    display_hand(player_hand)

                    if player_value > 21:
                        print("Busted! You lose.")
                        player_money -= bet
                        break
                    elif player_value == 21:
                        print("You have 21!")
                        break
                elif move == 'stand':
                    break
                else:
                    print("Invalid input. Please enter 'hit' or 'stand'.")

            if player_value <= 21:
                while dealer_value < 17:
                    deal_card(dealer_hand, deck)
                    dealer_value = hand_value(dealer_hand)

                display_hand(dealer_hand)

                if dealer_value > 21:
                    print("Dealer busts! You win!")
                    player_money += bet
                elif dealer_value == player_value:
                    print("It's a push.")
                elif dealer_value < player_value:
                    print("You win!")
                    player_money += bet
                else:
                    print("You lose.")
                    player_money -= bet

        db.write_money(player_money)

    print("You don't have enough money to continue playing.")
    while True:
        choice = input("Do you want to buy more chips? (y/n): ").lower()
        if choice == 'y':
            try:
                amount = float(input("Enter the amount of money you want to buy: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            if amount > 0:
                player_money += amount
                db.write_money(player_money)
                print(f"Your new balance is ${player_money:.2f}")
                main()
                break
            else:
                print("Invalid amount. Please enter a positive number.")
        elif choice == 'n':
            print("Thank you for playing!")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
