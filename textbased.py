import os

game_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Game Like Functions"

file_name = "current_currency.txt"

def start():
    currency_file_path = os.path.join(game_folder_path, file_name)

    # Only initialize if file doesn't exist
    if not os.path.exists(currency_file_path):
        initial_currency = "50"
        with open(currency_file_path, "w") as f:
            f.write(initial_currency)
        print("New game started with 50 coins!")
    else:
        print("Continuing existing game...")


def shop():
    shop_info = """
    PLEASE PICK 1: 
    1. Habit Revive: Revives a broken habit streak (50 Coins)
    2. Double Coins: Double reward for next review session (50 Coins)
    3. Combo Multiplier (review): Get 30 coins immediately when getting 10 correct answers in a row (15 Coins)    
    """
    print(shop_info)
    shop_select = input("Choose one of them (type in the number): ")
    return shop_select

def earn_currency():
    earn_info = """
    HERE'S HOW YOU CAN EARN COINS
    1. Daily Habit Check-in (15 Coins per habit)
    2. Answering all cards in the flashcard correctly (20 Coins)
    3. Get 20 coins for having a 5 day streak (20 Coins)
    """
    print(earn_info)

def command_input_func():
    command_input = input("Input a prompt: ")

    if command_input.lower() == "shop":
        print(command_input)
        shop_selection = shop()
        if shop_selection == "1":
            currency_file_path = os.path.join(game_folder_path, file_name)
            
            # Read current coins
            with open(currency_file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    print("Error: Currency file is empty!")
                    return
                last_line = lines[-1].strip()
                print(f"Current coins: {last_line}")
                current_coin = int(last_line) - 50
            
            # Check if user has enough coins
            if current_coin < 0:
                print("Not enough coins!")
                return
            
            print("You got yourself a Habit Review Pass!")
            
            # Write new coin amount
            with open(currency_file_path, "a") as d:
                d.write("\n" + str(current_coin))
            
            print(f"New balance: {current_coin}")

        elif shop_selection == "2":
            currency_file_path = os.path.join(game_folder_path, file_name)

            print("You got yourself a Double Coins Buff!")

            # Read current coins
            with open(currency_file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    print("Error: Currency file is empty!")
                    return
                last_line = lines[-1].strip()
                print(f"Current coins: {last_line}")
                current_coin = int(last_line) - 50

            # Check if user has enough coins
            if current_coin < 0:
                print("Not enough coins!")
                return

            print("You got yourself a Double Coins Buff!")

            # Write new coin amount
            with open(currency_file_path, "a") as d:
                d.write("\n" + str(current_coin))

            print(f"New balance: {current_coin}")
        elif shop_selection == "3":
            currency_file_path = os.path.join(game_folder_path, file_name)


            # Read current coins
            with open(currency_file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    print("Error: Currency file is empty!")
                    return
                last_line = lines[-1].strip()
                print(f"Current coins: {last_line}")
                current_coin = int(last_line) - 15

            # Check if user has enough coins
            if current_coin < 0:
                print("Not enough coins!")
                return

            print("You got yourself a Combo Multiplier Buff!")

            # Write new coin amount
            with open(currency_file_path, "a") as d:
                d.write("\n" + str(current_coin))

            print(f"New balance: {current_coin}")
            
    elif command_input.lower() == "earn":
        print(command_input)
        earn_currency()
    else:
        pass

command_input_func()