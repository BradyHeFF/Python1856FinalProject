import os

def read_money():
    try:
        with open("money.txt", "r") as file:
            money = float(file.readline().strip())
    except (FileNotFoundError, ValueError):
        print("Data file not found or corrupted. Starting with default balance of $1000.")
        money = 1000

    return money

def write_money(money):
    with open("money.txt", "w") as file:
        file.write(f"{money:.2f}")
