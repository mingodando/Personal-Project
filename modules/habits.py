import os
import json
import datetime
from tkinter import messagebox
from tkinter import *
from tkinter import ttk

# Change relative import to absolute import
try:
    from modules.config import habit_trainer_folder_path, TIMESTAMP_FORMAT
except ImportError:
    # Fallback for direct execution - adjust path as needed
    from config import habit_trainer_folder_path, TIMESTAMP_FORMAT

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
    """Create inventory file if it doesn't exist"""
    if not os.path.exists(inventory_path):
        initial_inventory = {
            "habit_revive": 0,
            "double_coins": 0,
            "combo_multiplier": 0
        }
        with open(inventory_path, "w") as f:
            json.dump(initial_inventory, f, indent=4)


def get_inventory():
    """Read and return current inventory"""
    initialize_inventory()
    with open(inventory_path, "r") as f:
        return json.load(f)


def add_to_inventory(item_key, quantity=1):
    """Add items to inventory"""
    inventory = get_inventory()
    inventory[item_key] = inventory.get(item_key, 0) + quantity
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=4)


def remove_from_inventory(item_key, quantity=1):
    """Remove items from inventory (returns True if successful)"""
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
    try:
        with open(combined_path, "r") as f:
            lines = f.readlines()
            if not lines:
                return 0
            last_line = lines[-1].strip()
            return int(last_line)
    except (FileNotFoundError, ValueError):
        return 0


def update_coin_display():
    """Update the coin display label"""
    if coin_label:
        current_coins = get_current_coins()
        coin_label.config(text=f"Current coins: {current_coins}")


# ===== INVENTORY UI FUNCTIONS =====

def remove_habit_revive(habit_revive_function):
    """Use a Habit Revive from inventory"""
    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, your streak will stay alive.")
    if yes_no:
        print("User said yes")
        if callable(habit_revive_function):
            habit_revive_function()
        if remove_from_inventory("habit_revive", 1):
            messagebox.showinfo("Used!", "Habit Revive used successfully!")
            open_inventory()
        else:
            messagebox.showwarning("Not Available", "You don't have any Habit Revives!")
    else:
        print("User said no")


def remove_double_coins(double_coins_function):
    """Use a Double Coins potion from inventory"""

    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, you will double the coins for next review session.")
    if yes_no:
        print("User said yes")
        if callable(double_coins_function):
            double_coins_function()
        if remove_from_inventory("double_coins", 1):
            messagebox.showinfo("Used!", "Double Coins Powerup used successfully!")
            open_inventory()
        else:
            messagebox.showwarning("Not Available", "You don't have any Double Coins!")
    else:
        print("User said no")


def remove_combo_multiplier(combo_multiplier_function=None):
    """Use a Combo Multiplier from inventory"""
    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, you will get 30 coins immediately when getting 10 correct answers in a row during review.")
    if yes_no:
        print("User said yes")
        if callable(combo_multiplier_function):
            combo_multiplier_function()
        if remove_from_inventory("combo_multiplier", 1):
            messagebox.showinfo("Used!", "Combo Multiplier used successfully!")
            open_inventory()
        else:
            messagebox.showwarning("Not Available", "You don't have any Combo Multipliers!")
    else:
        print("User said no")


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
    ttk.Button(habit_frame, text="Use", command=lambda: remove_habit_revive(None)).pack(side=LEFT, padx=5)

    # Double Coins
    double_frame = ttk.Frame(items_frame)
    double_frame.pack(fill=X, pady=5)
    ttk.Label(double_frame, text=f"Double Coins: {inventory['double_coins']}", width=25).pack(side=LEFT)
    ttk.Button(double_frame, text="Use", command=lambda: remove_double_coins(None)).pack(side=LEFT, padx=5)

    # Combo Multiplier
    combo_frame = ttk.Frame(items_frame)
    combo_frame.pack(fill=X, pady=5)
    ttk.Label(combo_frame, text=f"Combo Multiplier: {inventory['combo_multiplier']}", width=25).pack(side=LEFT)
    ttk.Button(combo_frame, text="Use", command=lambda: remove_combo_multiplier(None)).pack(side=LEFT, padx=5)

    # Close button
    ttk.Button(inventory_window, text="Close", command=inventory_window.destroy).pack(pady=10)


# ===== MAIN UI =====

def select_powerup(root):
    global coin_label

    # Display current coins at the top
    coin_label = ttk.Label(root, text="", font=("Arial", 12, "bold"))
    coin_label.grid(row=0, column=0, columnspan=2, pady=10)
    update_coin_display()

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
    use_power_up1 = ttk.Button(root,text="Use Powerup", command=lambda:remove_habit_revive(habit_revive_function=None))
    use_power_up1.grid(row=3, column=2,pady=5)

    # Power-up 2
    power_up2 = ttk.Label(root, text="Double Coins (50 coins)")
    power_up2.grid(row=4, column=0, pady=5, sticky=W, padx=10)
    buy_power_up2 = ttk.Button(root, command=buy_powerup2, text="Buy")
    buy_power_up2.grid(row=4, column=1, pady=5)
    use_power_up2 =ttk.Button(root, text="Use Powerup", command=lambda:remove_double_coins(double_coins_function=None))
    use_power_up2.grid(row=4, column=2, pady=5)

    # Power-up 3
    power_up3 = ttk.Label(root, text="Combo Multiplier (15 coins)")
    power_up3.grid(row=5, column=0, pady=5, sticky=W, padx=10)
    buy_power_up3 = ttk.Button(root, command=buy_powerup3, text="Buy")
    buy_power_up3.grid(row=5, column=1, pady=5)
    use_power_up3 = ttk.Button(root, text="Use Powerup", command=lambda:remove_combo_multiplier(combo_multiplier_function=None))
    use_power_up3.grid(row=5, column=2, pady=5)


def read_last_timestamp(file_path: str):
    """Read the last timestamp from a habit file."""
    with open(file_path, "r") as f:
        content = f.readlines()
        if content:
            content = content[-1].strip()
            return datetime.datetime.strptime(content, TIMESTAMP_FORMAT)
    return None


def write_timestamp(file_path: str, dt: datetime.datetime) -> None:
    """Write a timestamp to a habit file."""
    with open(file_path, "a") as f:
        f.write(dt.strftime(TIMESTAMP_FORMAT) + "\n")


def read_streak(file_path: str):
    """Read the current streak from a habit file."""
    with open(file_path, "r") as f:
        lines = f.readlines()
        num_lines = len(lines)
        return int(num_lines)


def failed_streak(file_path: str):
    """Reset the streak by clearing the file."""
    with open(file_path, "w") as f:
        pass


def new_streak(file_path: str):
    """Check if this is a new streak (empty file)."""
    with open(file_path, "r") as f:
        content = f.read()
    return not content


def check_streak(_streak_path: str) -> int:
    """Get the current streak count."""
    with open(_streak_path, "r") as f:
        lines = f.readlines()
        num_lines = len(lines)
        return int(num_lines)


def create_habit_backend(new_habit_input: Entry):
    """Backend logic for creating a new habit."""
    new_habit = new_habit_input.get().strip()
    if not new_habit:
        messagebox.showerror("Error", "Habit name cannot be empty.")
        return

    habit = f"{new_habit}.txt"
    new_habit_file_path = os.path.join(habit_trainer_folder_path, habit)

    if os.path.exists(new_habit_file_path):
        messagebox.showinfo("Info", "Habit already exists.")
        return

    with open(new_habit_file_path, "w") as f:
        pass

    messagebox.showinfo("Success", f"New habit added: {new_habit}.")
    print("Habit added successfully")


def create_habit_frontend(frame, habit_add_button: Button):
    """Frontend UI for creating a new habit."""
    new_habit_heading = ttk.Label(frame, text="Enter a new habit: ")
    new_habit_heading.grid(row=7, column=2)

    new_habit_input = ttk.Entry(frame, width=30)
    new_habit_input.grid(row=8, column=2)

    habit_add_button.destroy()

    new_habit_submit_button = ttk.Button(
        frame,
        text="Submit",
        command=lambda: create_habit_backend(new_habit_input)
    )
    new_habit_submit_button.grid(row=9, column=2)


def on_check(habit_listbox):
    def habit_revive_function():
        inventory = get_inventory()
        if inventory.get("habit_revive", 0) >= 1:
            remove_from_inventory("habit_revive", 1)
            messagebox.showinfo("Success", "Habit Revive used! Your streak is safe.")
        else:
            response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
            if not response:
                failed_streak(file_path)

    def double_coins_function():
        inventory = get_inventory()
        if inventory.get("double_coins", 0) >= 1:
            remove_from_inventory("double_coins", 1)
            messagebox.showinfo("Success", "Double Coins powerup used! Double reward for next review session")
        else:
            response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
            if not response:
                failed_streak(file_path)

    """Check a habit and update streak."""
    habit_selection = habit_listbox.curselection()
    if not habit_selection:
        messagebox.showinfo("Info Dialog", "No habit selected.")
        return

    habit_indices = habit_selection[0]
    habit_selected = habit_listbox.get(habit_indices)
    print(f"Selected Habit: {habit_selected}")

    try:
        habit_listbox.itemconfig(habit_indices, bg="green")
    except:
        pass

    selected_habit = habit_selected.split(":", 1)[0]
    target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
    file_path = os.path.join(habit_trainer_folder_path, target_file)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Habit not found.")
        return

    if new_streak(file_path):
        messagebox.showinfo("First Check", f"Congrats, this is your first check for {selected_habit}.")
        write_timestamp(file_path, datetime.datetime.now())
        return

    now = datetime.datetime.now()
    last = read_last_timestamp(file_path)

    if last is None:
        write_timestamp(file_path, now)
        return

    days_diff = (now.date() - last.date()).days

    if days_diff == 0:
        current_streak = read_streak(file_path)
        messagebox.showinfo("Info",
                            f"You've already completed this habit today. Current streak: {current_streak}")
        print(f"Already checked today. Streak = {current_streak}")

    elif days_diff == 1:
        streak = check_streak(file_path)
        streak += 1
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"Nice! Streak increased to {streak}.")
        print(f"Recorded today. Streak = {streak}")

    elif days_diff == 2:
        streak = 1
        habit_revive_function()
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"You're late by {days_diff} day(s). Streak reset to {streak}.")
        print(f"Streak reset = {streak}")

    elif days_diff > 2:
        streak = 1
        failed_streak(file_path)
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"You're late by {days_diff} day(s). Streak reset to {streak}")
        print(f"Streak reset = {streak}")

    else:
        streak = max(1, check_streak(file_path))
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"Time anomaly detected. Streak preserved at {streak}.")
        print(f"Anomaly detected. Streak = {streak}")


# Only run main() if this file is executed directly (for testing purposes)
if __name__ == "__main__":
    initialize_inventory()

    root = Tk()
    root.title("Power-Up Shop")

    select_powerup(root)

    root.geometry("350x300")
    root.mainloop()