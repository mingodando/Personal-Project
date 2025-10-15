import os
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# File Paths:
game_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Game Like Functions"
file_name = "current_currency.txt"
combined_path = os.path.join(game_folder_path, file_name)
inventory_path = os.path.join(game_folder_path, "inventory.json")

POWER_UPS = """
    1. Habit Revive: Revives a broken habit streak (50 Coins)
    2. Double Coins: Double reward for next review session (50 Coins)
    3. Combo Multiplier (review): Get 30 coins immediately when getting 10 correct answers in a row (15 Coins)    

"""

# Global variable to store the coin label
coin_label = None


# ===== SHOP FUNCTIONS =====

def buy_powerup1():
    current_coin = get_current_coins()

    # Check if user has enough coins
    if current_coin < 50:
        messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
        return

    # Write new coin amount
    new_coin = current_coin - 50
    with open(combined_path, "w") as d:
        d.write(str(new_coin) + "\n")

    # Add to inventory
    add_to_inventory("habit_revive", 1)

    messagebox.showinfo("Success", "You bought 1 Habit Revive Pass!\nCheck your inventory to use it.")

    # Update the display
    update_coin_display()


def buy_powerup2():
    current_coin = get_current_coins()

    # Check if user has enough coins
    if current_coin < 50:
        messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
        return

    # Write new coin amount
    new_coin = current_coin - 50
    with open(combined_path, "w") as d:
        d.write(str(new_coin) + "\n")

    # Add to inventory
    add_to_inventory("double_coins", 1)

    messagebox.showinfo("Success", "You bought 1 Double Coin Potion!\nCheck your inventory to use it.")

    # Update the display
    update_coin_display()


def buy_powerup3():
    current_coin = get_current_coins()

    # Check if user has enough coins
    if current_coin < 15:
        messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 15.")
        return

    # Write new coin amount
    new_coin = current_coin - 15
    with open(combined_path, "w") as d:
        d.write(str(new_coin) + "\n")

    # Add to inventory
    add_to_inventory("combo_multiplier", 1)

    messagebox.showinfo("Success", "You bought 1 Combo Multiplier!\nCheck your inventory to use it.")

    # Update the display
    update_coin_display()




# ===== INVENTORY MANAGEMENT FUNCTIONS =====

def initialize_inventory():
    #Create inventory file if it doesn't exist
    if not os.path.exists(inventory_path):
        initial_inventory = {
            "habit_revive": 0,
            "double_coins": 0,
            "combo_multiplier": 0
        }
        with open(inventory_path, "w") as f:
            json.dump(initial_inventory, f, indent=4)


def get_inventory():
    #Read and return current inventory
    initialize_inventory()
    #Read and return the current inventory
    with open(inventory_path, "r") as f:
        return json.load(f)


def add_to_inventory(item_key, quantity=1):
    #Add items to inventory
    inventory = get_inventory()
    inventory[item_key] = inventory.get(item_key, 0) + quantity
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=4)


def remove_from_inventory(item_key, quantity=1):
    #Remove items from inventory (returns True if successful)
    inventory = get_inventory()
    if inventory.get(item_key, 0) >= quantity:
        inventory[item_key] -= quantity
        with open(inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)
        return True
    return False


def get_item_count(item_key):
    """Get count of specific item in inventory"""
    inventory = get_inventory()
    return inventory.get(item_key, 0)


# ===== COIN MANAGEMENT FUNCTIONS =====

def get_current_coins():
    """Helper function to read current coin amount from file"""
    with open(combined_path, "r") as f:
        lines = f.readlines()
        if not lines:
            return 0
        last_line = lines[-1].strip()
        return int(last_line)


def update_coin_display():
    """Update the coin display label"""
    current_coins = get_current_coins()
    coin_label.config(text=f"Current coins: {current_coins}")


# ===== INVENTORY UI FUNCTIONS =====
def habit_revive_function():
    with open(file_name, "r") as f:
        data = json.load(f)
        try:
            specs = data["habit_revive"]
            if specs >= 1:
                remove_habit_revive()
            else:
                response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
                if response:
                    pass
                else:
                    print("Don't buy")
        except EXCEPTION:
            pass

def remove_habit_revive():
    """Use a Habit Revive from inventory"""
    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, your streak will stay alive.")
    if yes_no:
        print("User said yes")

    else:
        print("User said no")
        if remove_from_inventory("Habit_revive", 1):
            messagebox.showinfo("Used!", "Habit Revive used successfully!\n(Implement your habit revival logic here)")
            open_inventory()  # Refresh inventory window
        else:
            messagebox.showwarning("Not Available", "You don't have any Habit Revives!")


def use_double_coins():
    """Use a Double Coins potion from inventory"""
    if remove_from_inventory("Double_coins", 1):
        messagebox.showinfo("Used!", "Double Coins activated!\n(Implement your double coins logic here)")
        open_inventory()  # Refresh inventory window
    else:
        messagebox.showwarning("Not Available", "You don't have any Double Coin Potions!")


def use_combo_multiplier():
    """Use a Combo Multiplier from inventory"""
    if remove_from_inventory("Combo_multiplier", 1):
        messagebox.showinfo("Used!", "Combo Multiplier activated!\n(Implement your combo multiplier logic here)")
        open_inventory()  # Refresh inventory window
    else:
        messagebox.showwarning("Not Available", "You don't have any Combo Multipliers!")


def open_inventory():
    """Open inventory window"""
    inventory_window = Toplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("400x300")

    # Title
    title_label = ttk.Label(inventory_window, text="Your Power-Ups", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)

    # Get current inventory
    inventory = get_inventory()

    # Create frame for inventory items
    items_frame = ttk.Frame(inventory_window)
    items_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

    # Habit Revive
    habit_frame = ttk.Frame(items_frame)
    habit_frame.pack(fill=X, pady=5)
    ttk.Label(habit_frame, text=f"Habit Revive: {inventory['habit_revive']}", width=25).pack(side=LEFT)
    ttk.Button(habit_frame, text="Use", command=remove_habit_revive).pack(side=LEFT, padx=5)

    # Double Coins
    double_frame = ttk.Frame(items_frame)
    double_frame.pack(fill=X, pady=5)
    ttk.Label(double_frame, text=f"Double Coins: {inventory['double_coins']}", width=25).pack(side=LEFT)
    ttk.Button(double_frame, text="Use", command=use_double_coins).pack(side=LEFT, padx=5)

    # Combo Multiplier
    combo_frame = ttk.Frame(items_frame)
    combo_frame.pack(fill=X, pady=5)
    ttk.Label(combo_frame, text=f"Combo Multiplier: {inventory['combo_multiplier']}", width=25).pack(side=LEFT)
    ttk.Button(combo_frame, text="Use", command=use_combo_multiplier).pack(side=LEFT, padx=5)

    # Close button
    ttk.Button(inventory_window, text="Close", command=inventory_window.destroy).pack(pady=10)


# ===== MAIN UI =====

def select_powerup(root):
    global coin_label

    # Display current coins at the top
    coin_label = ttk.Label(root, text="", font=("Arial", 12, "bold"))
    coin_label.grid(row=0, column=0, columnspan=2, pady=10)
    update_coin_display()  # Initialize with current value

    # Inventory button
    inventory_btn = ttk.Button(root, text="Open Inventory", command=open_inventory)
    inventory_btn.grid(row=1, column=0, columnspan=2, pady=5)

    # Shop title
    shop_label = ttk.Label(root, text="Shop", font=("Arial", 11, "bold"))
    shop_label.grid(row=2, column=0, columnspan=2, pady=(10, 5))

    # Power-up 1
    power_up1 = ttk.Label(root, text="Habit Revive (50 coins)")
    power_up1.grid(row=3, column=0, pady=5, sticky=W, padx=10)
    buy_power_up1 = ttk.Button(root, command=buy_powerup1, text="Buy")
    buy_power_up1.grid(row=3, column=1, pady=5)

    # Power-up 2
    power_up2 = ttk.Label(root, text="Double Coins (50 coins)")
    power_up2.grid(row=4, column=0, pady=5, sticky=W, padx=10)
    buy_power_up2 = ttk.Button(root, command=buy_powerup2, text="Buy")
    buy_power_up2.grid(row=4, column=1, pady=5)

    # Power-up 3
    power_up3 = ttk.Label(root, text="Combo Multiplier (15 coins)")
    power_up3.grid(row=5, column=0, pady=5, sticky=W, padx=10)
    buy_power_up3 = ttk.Button(root, command=buy_powerup3, text="Buy")
    buy_power_up3.grid(row=5, column=1, pady=5)


def main():
    initialize_inventory()  # Make sure inventory file exists

    root = Tk()
    root.title("Power-Up Shop")

    select_powerup(root)

    root.geometry("350x300")
    root.mainloop()


main()
