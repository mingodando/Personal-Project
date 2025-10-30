import os
from tkinter import *
import customtkinter as ctk
import webbrowser
import json
from tkinter import messagebox
from datetime import datetime

frame1 = None
frame2 = None
frame3 = None
display = None


#----- Create Folder Path -----#
flashcard_folder = "Flashcards Files"
habit_folder = "Habit Trainer"
game_folder = "Game"


# File Paths
current_directory = os.getcwd()
print(current_directory)
#Go to file explorer and copy the path of the folder you want to use.
#CREATE, CHANGE, AND INSERT YOUR FOLDER PATH HERE
flashcard_folder_path = os.path.join(current_directory, flashcard_folder)
print(flashcard_folder_path)
#CREATE, CHANGE, AND INSERT YOUR FOLDER PATH HERE
habit_trainer_folder_path = os.path.join(current_directory, habit_folder)
print(habit_trainer_folder_path)
#GET RID OF THE BACKPART OF THE FILE PATH PATH
personal_project_file_path = current_directory
#CREATE, CHANGE, INSERT YOUR OWN GAME FOLDER PATH HERE
game_folder_path = os.path.join(current_directory, game_folder)


def check_path(flashcard_folder_path, habit_trainer_folder_path, game_folder_path):
    if not os.path.exists(flashcard_folder_path):
        os.makedirs(flashcard_folder_path, exist_ok=True)
    if not os.path.exists(habit_trainer_folder_path):
        os.makedirs(habit_trainer_folder_path, exist_ok=True)
    if not os.path.exists(game_folder_path):
        os.makedirs(game_folder_path, exist_ok=True)


#Check for folder path:
check_path(flashcard_folder_path, habit_trainer_folder_path, game_folder_path)


# Get file lists
flashcard_files = os.listdir(flashcard_folder_path)
habit_trainer_files = os.listdir(habit_trainer_folder_path)

# Timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%d"

# Theme preference file
THEME_PREFERENCE_FILE = os.path.join(os.path.dirname(__file__), "..", "theme_preference.json")


#----- Configurations -----#
# Theme configuration for tkinter widgets
THEMES = {
    "pink": {
        "frame_bg": "#FFD6E8",
        "ctrl_bg": "#FFE5F0",
        "fg": "#8B0045",
        "listbox_color": "#FFB8D9",
        "entry_color": "#FFFFFF",
        "button_bg": "#FF1493",
        "button_hover": "#C71585",
        "button_fg": "#FFFFFF"
    },
    "blue": {
        "frame_bg": "#B8E6FF",
        "ctrl_bg": "#D4F1FF",
        "fg": "#003D5C",
        "listbox_color": "#7DD3FC",
        "entry_color": "#FFFFFF",
        "button_bg": "#0EA5E9",
        "button_hover": "#0284C7",
        "button_fg": "#FFFFFF"
    },
    "white": {
        "frame_bg": "#F5F5F5",
        "ctrl_bg": "#FFFFFF",
        "fg": "#1F2937",
        "listbox_color": "#E5E7EB",
        "entry_color": "#FFFFFF",
        "button_bg": "#4B5563",
        "button_hover": "#374151",
        "button_fg": "#FFFFFF"
    }
}

# CustomTkinter appearance modes
CTK_APPEARANCE_MODES = {
    "pink": "light",
    "blue": "light",
    "white": "light"
}

# CustomTkinter color themes (if you want to define custom colors)
CTK_THEMES = {
    "pink": {
        "CTkFrame": {"fg_color": "#FFD6E8"},
        "CTkButton": {
            "fg_color": "#FF1493",
            "hover_color": "#C71585",
            "text_color": "#FFFFFF"
        },
        "CTkLabel": {"text_color": "#8B0045"},
        "CTkEntry": {
            "fg_color": "#FFFFFF",
            "text_color": "#8B0045",
            "border_color": "#FF1493"
        }
    },
    "blue": {
        "CTkFrame": {"fg_color": "#B8E6FF"},
        "CTkButton": {
            "fg_color": "#0EA5E9",
            "hover_color": "#0284C7",
            "text_color": "#FFFFFF"
        },
        "CTkLabel": {"text_color": "#003D5C"},
        "CTkEntry": {
            "fg_color": "#FFFFFF",
            "text_color": "#003D5C",
            "border_color": "#0EA5E9"
        }
    },
    "white": {
        "CTkFrame": {"fg_color": "#F5F5F5"},
        "CTkButton": {
            "fg_color": "#4B5563",
            "hover_color": "#374151",
            "text_color": "#FFFFFF"
        },
        "CTkLabel": {"text_color": "#1F2937"},
        "CTkEntry": {
            "fg_color": "#FFFFFF",
            "text_color": "#1F2937",
            "border_color": "#4B5563"
        }
    }
}


#----- Flashcard Functions -----#
def no_list_files(folder_name):
    """List files in a folder if it exists."""
    file_path = os.path.join(flashcard_folder_path, folder_name)
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")
        return

    list_file = os.listdir(file_path)
    if folder_name in flashcard_files:
        messagebox.showinfo("Info Dialog", f"Files in folder: {list_file}")
    else:
        messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")


def yes_list_files(folder_name):
    """Check if folder exists and list flashcard files."""
    if folder_name in flashcard_files:
        messagebox.showerror("Error", "Folder already exists. Please enter a different name.")
        return
    elif folder_name not in flashcard_files:
        messagebox.showinfo("Info Dialog", str(flashcard_files))
    # Update the display

def add_card(edit_listbox, file_name, folder_name, frame):
    """Add a flashcard to a file."""
    add_card_file_path = os.path.join(flashcard_folder_path, folder_name, file_name)

    # Load existing data or start fresh
    data = {}
    if os.path.exists(add_card_file_path):
        with open(add_card_file_path, "r") as d:
            try:
                loaded = json.load(d)
                if isinstance(loaded, dict):
                    data = loaded
                else:
                    messagebox.showerror("Error", "Unsupported file format. Expected a JSON object.")
                    return
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Invalid JSON in file:\n{add_card_file_path}\n\n{e}")
                return

    # Create inputs
    question_heading = ctk.CTkLabel(frame,
                                    text="Enter the question:")
    question_heading.grid(row=20,
                          column=6,
                          sticky="n",
                          pady=5)
    question = ctk.CTkEntry(frame, width=200)
    question.grid(row=21,
                  column=6,
                  sticky="n",
                  pady=5)

    answer_heading = ctk.CTkLabel(frame,
                                  text="Enter the answer:")
    answer_heading.grid(row=22,
                        column=6,
                        sticky="n",
                        pady=5)
    answer = ctk.CTkEntry(frame, width=200)
    answer.grid(row=23,
                column=6,
                sticky="n",
                pady=5)

    def on_add():
        """Handle adding a card."""
        q = question.get().strip()
        a = answer.get().strip()
        if not q or not a:
            messagebox.showerror("Error", "Both question and answer are required.")
            return

        data[q] = a

        # Save to file
        try:
            with open(add_card_file_path, "w") as f:
                json.dump(data, f, indent=4)
        except OSError as t:
            messagebox.showerror("Error", f"Failed to save:\n{add_card_file_path}\n\n{t}")
            return

        # Update listbox
        edit_listbox.insert(END, f"{q}: {a}")

        # Clear inputs
        question.delete(0, END)
        answer.delete(0, END)
        question.focus_set()

    add_btn = ctk.CTkButton(frame,
                            text="Add Card",
                            command=on_add,
                            width=100)
    add_btn.grid(row=28,
                 column=6,
                 sticky="n",
                 pady=5)


def edit_card(edit_listbox, file_name, folder_name, item_selected, frame):
    """Edit an existing flashcard."""
    item_selection = edit_listbox.curselection()
    if not item_selection:
        return

    item_indices = item_selection[0]
    item_selected = edit_listbox.get(item_indices)
    print(f"Selected item: {item_selected}")

    selected_question = item_selected.split(":", 1)[0].strip()
    selected_answer = item_selected.split(":", 1)[1].strip() if ":" in item_selected else ""

    # Create edit inputs
    edit_question_heading = ctk.CTkLabel(frame,
                                         text="Enter the question:")
    edit_question_heading.grid(row=20,
                               column=7,
                               sticky="n",
                               pady=5)
    edit_question = ctk.CTkEntry(frame, width=200)
    edit_question.grid(row=21,
                       column=7,
                       sticky="n",
                       pady=5)
    edit_question.insert(0, selected_question)

    edit_answer_heading = ctk.CTkLabel(frame,
                                       text="Enter the answer:")
    edit_answer_heading.grid(row=22,
                             column=7,
                             sticky="n",
                             pady=5)
    edit_answer = ctk.CTkEntry(frame, width=200)
    edit_answer.grid(row=23,
                     column=7,
                     sticky="n",
                     pady=5)
    edit_answer.insert(0, selected_answer)

    edit_done_button = ctk.CTkButton(
        frame,
        text="Done",
        width=100,
        command=lambda: edit_done(file_name,
                                  folder_name,
                                  edit_question,
                                  edit_answer,
                                  item_selected)
    )
    edit_done_button.grid(row=28,
                          column=7,
                          sticky="n",
                          pady=5)


def edit_done(file_name, folder_name, edit_question, edit_answer, item_selected):
    """Save edited flashcard."""
    target_file = f"{file_name}.json" if not file_name.lower().endswith(".json") else file_name
    final_file_path = os.path.join(flashcard_folder_path, folder_name, target_file)

    # Load data
    with open(final_file_path, "r") as f:
        data = json.load(f)

    # Extract values
    new_question = edit_question.get().strip() if hasattr(edit_question, "get") else str(edit_question).strip()
    new_answer = edit_answer.get().strip() if hasattr(edit_answer, "get") else str(edit_answer).strip()

    if not new_question or not new_answer:
        messagebox.showerror("Error", "Both question and answer are required.")
        return

    original_question = item_selected.split(":", 1)[0].strip()

    if original_question not in data:
        messagebox.showerror("Error",
                             f"Original flashcard not found: '{original_question}'.")
        return

    # Update or replace
    if new_question == original_question:
        data[original_question] = new_answer
    else:
        del data[original_question]
        data[new_question] = new_answer

    # Save
    with open(final_file_path, "w") as f:
        json.dump(data, f, indent=4)
    messagebox.showinfo("Info Dialog", "Flashcard edited successfully.")


#----- Edit Flashcard Functions -----#
def edit_flashcards_frontend():
    """Create edit flashcards interface."""
    folder_name_heading = ctk.CTkLabel(frame1,
                                       text="Enter the name of the folder:")
    folder_name_heading.grid(row=1,
                             column=4,
                             sticky="n")

    folder_name = ctk.CTkEntry(frame1)
    folder_name.grid(row=2,
                     column=4,
                     sticky="n")

    folder_name_submit = ctk.CTkButton(
        frame1,
        text="Submit",
        command=lambda: no_list_files(folder_name.get())
    )
    folder_name_submit.grid(row=3,
                            column=4,
                            sticky="n")

    file_name_heading = ctk.CTkLabel(frame1,
                                     text="Enter the name for your flashcard file:")
    file_name_heading.grid(row=4,
                           column=4,
                           sticky="n")

    file_name = ctk.CTkEntry(frame1)
    file_name.grid(row=5,
                   column=4,
                   sticky="n")

    file_name_submit = ctk.CTkButton(
        frame1,
        text="Submit",
        command=lambda: edit_flashcard_cl(file_name.get(), folder_name.get())
    )
    file_name_submit.grid(row=6, column=4, sticky="n")


def edit_flashcard_cl(file_name, folder_name):
    """Load flashcards for editing."""
    import json
    from tkinter import messagebox

    file_name = f"{file_name.lower()}.json"
    folder_name = folder_name.lower()
    final_file_path = os.path.join(flashcard_folder_path, folder_name, file_name)

    # Create listbox frame
    edit_frame = ctk.CTkFrame(frame1)
    edit_frame.grid(row=4,
                    column=6,
                    rowspan=15,
                    columnspan=3,
                    sticky="nsew")
    edit_frame.grid_rowconfigure(0, weight=1)
    edit_frame.grid_columnconfigure(0, weight=1)

    edit_listbox = Listbox(edit_frame,
                           width=50,
                           height=10)
    edit_listbox.grid(row=0,
                      column=0,
                      sticky="n")

    edit_scrollbar = ctk.CTkScrollbar(edit_frame,
                                      orientation='vertical',
                                      command=edit_listbox.yview)
    edit_scrollbar.grid(row=0,
                        column=1,
                        sticky="ns")

    edit_listbox.config(yscrollcommand=edit_scrollbar.set)

    # Load data
    edit_listbox.delete(0, END)


    try:
        with open(final_file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found:\n{final_file_path}")
        return
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"Invalid JSON in file:\n{final_file_path}\n\n{e}")
        return
    except OSError as e:
        messagebox.showerror("Error", f"Could not open file:\n{final_file_path}\n\n{e}")
        return

    # Populate listbox
    if isinstance(data, dict):
        for key, value in data.items():
            edit_listbox.insert(END, f"{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            edit_listbox.insert(END, str(item))
    else:
        edit_listbox.insert(END, str(data))

    # Add section
    add_heading = ctk.CTkLabel(frame1,
                               text="Add",
                               font=("Arial", 15))
    add_heading.grid(row=19,
                     column=6,
                     sticky="s")
    add_card(edit_listbox,
             file_name,
             folder_name,
             frame1)

    # Edit section
    edit_heading = ctk.CTkLabel(frame1,
                                text="Edit",
                                font=("Arial", 15))
    edit_heading.grid(row=19,
                      column=7,
                      sticky="s")

    def on_select(event):
        item_selection = edit_listbox.curselection()
        if item_selection:
            item_indices = item_selection[0]
            item_selected = edit_listbox.get(item_indices)
            edit_card(edit_listbox, file_name, folder_name, item_selected, frame1)

    edit_listbox.bind("<<ListboxSelect>>", on_select)


#----- Inventory Functions -----#
# File Paths:
currency_file_name = "current_currency.txt"
combined_path = os.path.join(game_folder_path, currency_file_name)
inventory_path = os.path.join(game_folder_path, "inventory.json")

POWER_UPS = """
    1. Habit Revive: Revives a broken habit streak (50 Coins)
    2. Double Coins: Double reward for next review session (25 Coins)
    3. Combo Multiplier (review): Get 30 coins immediately when getting 10 correct answers in a row (15 Coins)    

"""

# Global variable to store the coin label
#coin_label = None
global coin_label


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
def initialize_currency():
    """Create currency file if it doesn't exist"""
    if not os.path.exists(combined_path):
        with open(combined_path, "w") as f:
            f.write("100\n")

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
        coin_label.configure(text=f"Current coins: {current_coins}")


# ===== INVENTORY UI FUNCTIONS =====
def habit_revive_function(file_path):
    inventory = get_inventory()
    if inventory.get("habit_revive", 0) >= 1:
        remove_from_inventory("habit_revive", 1)
        messagebox.showinfo("Success", "Habit Revive used! Your streak is safe.")
    else:
        response = messagebox.askyesno("Buy Powerup?", "Do you want to buy more powerups?")
        if response:
            open_inventory()
        elif not response:
            failed_streak(file_path)

def double_coins_function(file_path):
    inventory = get_inventory()
    if inventory.get("double_coins", 0) >= 1:
        remove_from_inventory("double_coins", 1)
        messagebox.showinfo("Success", "Double Coins powerup used! Double reward for next review session")
    else:
        response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
        if not response:
            failed_streak(file_path)

def combo_multiplier_function():
    inventory = get_inventory()
    if inventory.get("combo_multiplier", 0) >= 1:
        remove_from_inventory("combo_multiplier", 1)
        messagebox.showinfo("Success", "Combo Multiplier powerup used! Double reward for next review session")
    else:
        messagebox.showerror("Error", "You don't have any Combo Multipliers!")

def remove_habit_revive(habit_revive_function):
    """Use a Habit Revive from inventory"""
    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, your streak will stay alive.")
    if yes_no:
        print("User said yes")
        if callable(habit_revive_function):
            habit_revive_function()
        if remove_from_inventory("habit_revive", 1):
            messagebox.showinfo("Used!", "Habit Revive used successfully!")
        else:
            messagebox.showwarning("Not Available", "You don't have any Habit Revives!")
            messagebox.showinfo("Buy More", "Go to the shop to buy more and come back")

    else:
        print("User said no")

def remove_double_coin(double_coin_function):
    """Use a Double Coins potion from inventory"""

    yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, you will double the coins for next review session.")
    if yes_no:
        print("User said yes")
        if callable(double_coins_function):
            double_coins_function(file_path=None)
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
    inventory_window = ctk.CTkToplevel()
    inventory_window.title("Inventory")
    inventory_window.geometry("400x310")

    # Title
    title_label = ctk.CTkLabel(inventory_window,
                               text="Your Power-Ups",
                               font=("Arial", 14, "bold"))
    title_label.grid(pady=10)

    # Get current inventory
    inventory = get_inventory()

    # Create frame for inventory items
    items_frame = ctk.CTkFrame(inventory_window)
    items_frame.grid(pady=10,
                     padx=2)

    # Habit Revive
    habit_frame = ctk.CTkFrame(items_frame)
    habit_frame.grid(pady=5,
                     padx=10)
    (ctk.CTkLabel(habit_frame,
                 text=f"Habit Revive: {inventory['habit_revive']}",
                 width=200,
                  anchor="w")
     .grid(padx=5))
    (ctk.CTkButton(habit_frame,
                  text="Use",
                  width=80,
                  command=lambda: remove_habit_revive(None))
     .grid(padx=5))

    # Double Coins
    double_frame = ctk.CTkFrame(items_frame)
    double_frame.grid(pady=5, padx=10)
    (ctk.CTkLabel(double_frame,
                 text=f"Double Coins: {inventory['double_coins']}",
                 width=200, anchor="w")
     .grid(padx=5))
    (ctk.CTkButton(double_frame,
                  text="Use", width=80,
                  command=lambda: remove_combo_multiplier(None))
     .grid(padx=5))

    # Combo Multiplier
    combo_frame = ctk.CTkFrame(items_frame)
    combo_frame.grid(pady=5,
                     padx=10)
    (ctk.CTkLabel(combo_frame,
                 text=f"Combo Multiplier: {inventory['combo_multiplier']}",
                 width=200, anchor="w")
     .grid(padx=5))
    (ctk.CTkButton(combo_frame,
                  text="Use",
                  width=80,
                  command=lambda: remove_combo_multiplier(None))
     .grid(padx=5))

    # Close button
    ctk.CTkButton(inventory_window, text="Close", command=inventory_window.destroy).grid(pady=10)

def select_powerup(root):
    global coin_label

    # Display current coins at the top
    coin_label = ctk.CTkLabel(root,
                              text="",
                              font=("Arial", 12, "bold"))

    coin_label.grid(row=0,
                    column=0,
                    columnspan=2,
                    pady=10)
    update_coin_display()

    # Inventory button
    inventory_btn = ctk.CTkButton(frame3,
                                  text="Open Inventory",
                                  command=open_inventory)
    inventory_btn.grid(row=1,
                       column=0,
                       columnspan=2,
                       pady=5)

    #Power-ups:
    power_up = ctk.CTkLabel(frame3,
                            text=f"""Here are the available power-ups:
                            {POWER_UPS}
                            """,
                            font=("Arial", 12, "bold"))
    power_up.grid(row=2,
                  rowspan=3,
                  column=0,
                  columnspan=2,
                  pady=10)

    # Shop title
    shop_label = ctk.CTkLabel(frame3,
                              text="Shop",
                              font=("Arial", 11, "bold"))
    shop_label.grid(row=5,
                    column=0,
                    columnspan=2,
                    pady=(10, 5))

    # Power-up 1
    power_up1 = ctk.CTkLabel(frame3,
                             text="Habit Revive (50 coins)",
                             anchor="w")
    power_up1.grid(row=6,
                   column=0,
                   pady=5,
                   sticky="w",
                   padx=10)
    buy_power_up1 = ctk.CTkButton(frame3,
                                  command=buy_powerup1,
                                  text="Buy",
                                  width=80)
    buy_power_up1.grid(row=6,
                       column=1,
                       pady=5)


    # Power-up 2
    power_up2 = ctk.CTkLabel(frame3,
                             text="Double Coins (50 coins)",
                             anchor="w")
    power_up2.grid(row=7,
                   column=0,
                   pady=5,
                   sticky="w",
                   padx=10)
    buy_power_up2 = ctk.CTkButton(frame3,
                                  command=buy_powerup2,
                                  text="Buy",
                                  width=80)
    buy_power_up2.grid(row=7,
                       column=1,
                       pady=5)


    # Power-up 3
    power_up3 = ctk.CTkLabel(frame3,
                             text="Combo Multiplier (15 coins)",
                             anchor="w")
    power_up3.grid(row=8,
                   column=0,
                   pady=5,
                   sticky="w",
                   padx=10)
    buy_power_up3 = ctk.CTkButton(frame3,
                                  command=buy_powerup3,
                                  text="Buy",
                                  width=80)
    buy_power_up3.grid(row=8,
                       column=1,
                       pady=5
                       )


#----- Habit Functions -----#
def read_last_timestamp(file_path: str):
    """Read the last timestamp from a habit file."""
    with open(file_path, "r") as f:
        content = f.readlines()
        if content:
            content = content[-1].strip()
            return datetime.strptime(content, TIMESTAMP_FORMAT)
    return None


def write_timestamp(file_path: str, dt: datetime) -> None:
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
    with open(file_path, "w"):
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


def create_habit_backend(new_habit_input: ctk.CTkEntry, habit_listbox, new_habit_heading):
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

    with open(new_habit_file_path, "w"):
        pass

    messagebox.showinfo("Success", f"New habit added: {new_habit}.")
    habit_listbox.insert(END, habit)
    new_habit_input.delete(0, END)
    new_habit_input.destroy()
    new_habit_heading.destroy()
    print("Habit added successfully")

def create_habit_frontend(frame, habit_add_button: ctk.CTkButton, habit_listbox):
    """Frontend UI for creating a new habit."""
    new_habit_heading = ctk.CTkLabel(frame,
                                     text="Enter a new habit: ")
    new_habit_heading.grid(row=6, column=5)

    new_habit_input = ctk.CTkEntry(frame, width=200)
    new_habit_input.grid(row=7, column=5)

    habit_add_button.destroy()

    new_habit_submit_button = ctk.CTkButton(
        frame,
        text="Submit",
        command=lambda: create_habit_backend(new_habit_input, habit_listbox, new_habit_heading))

    new_habit_submit_button.grid(row=9, column=5)

def delete_habit(habit_listbox):
    # Corrected implementation: use curselection(), build correct file path, remove file and listbox entry.
    habit_selection = habit_listbox.curselection()
    if not habit_selection:
        messagebox.showinfo("Info Dialog", "No habit selected.")
        return

    habit_index = habit_selection[0]
    habit_entry = habit_listbox.get(habit_index)
    # If items include extra info like "name: ..." keep only the name; otherwise this is the filename already.
    selected_habit = habit_entry.split(":", 1)[0].strip()
    target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
    file_path = os.path.join(habit_trainer_folder_path, target_file)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"Habit file not found:\n{file_path}")
        return

    try:
        os.remove(file_path)
    except OSError as e:
        messagebox.showerror("Error", f"Could not delete habit file:\n{e}")
        return

    # Remove from listbox UI
    try:
        habit_listbox.delete(habit_index)
    except Exception:
        pass

    messagebox.showinfo("Success", "Habit deleted.")

def on_check(habit_listbox):

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
    except KeyboardInterrupt:
        pass

    selected_habit = habit_selected.split(":", 1)[0]
    target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
    file_path = os.path.join(habit_trainer_folder_path, target_file)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Habit not found.")
        return

    if new_streak(file_path):
        messagebox.showinfo("First Check", f"Congrats, this is your first check for {selected_habit}.")
        write_timestamp(file_path, datetime.now())
        return

    now = datetime.now()
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
        habit_revive_function(file_path)
        write_timestamp(file_path, now)

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


#----- Rename Functions -----#
def rename_folder(input_old_folder, input_new_folder):
    """Rename a flashcard folder."""
    input_old_folder_name = input_old_folder.get()
    input_new_folder_name = input_new_folder.get()

    if input_old_folder_name in flashcard_files:
        # Start the renaming process
        os.rename(
            os.path.join(flashcard_folder_path, input_old_folder_name),
            os.path.join(flashcard_folder_path, input_new_folder_name)
        )
        messagebox.showinfo("Info Dialog",
                            f"Folder '{input_old_folder_name}' renamed to '{input_new_folder_name}'.")

    else:
        messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")


def open_rename():
    """Create rename folder interface."""
    heading_rename1 = ctk.CTkLabel(frame1,
                                   text="Old Folder Name:",
                                   font=("Arial", 15))
    heading_rename1.grid(row=18,
                         column=0,
                         sticky="n")

    heading_rename2 = ctk.CTkLabel(frame1,
                                   text="New Folder Name:",
                                   font=("Arial", 15))
    heading_rename2.grid(row=20,
                         column=0,
                         sticky="n")

    input_old_folder = ctk.CTkEntry(frame1)
    input_new_folder = ctk.CTkEntry(frame1)
    input_old_folder.grid(row=19,
                          column=0,
                          sticky="n")
    input_old_folder.focus_set()
    input_new_folder.grid(row=21,
                          column=0,
                          sticky="n")

    rename_submit = ctk.CTkButton(
        frame1,
        text="Submit",
        command=lambda: [rename_folder(input_old_folder, input_new_folder), update_listbox(display)]
    )
    rename_submit.grid(row=22, column=0, sticky="n")


#----- Add Folder and File Feature -----#
def create_file(folder_name, file_name):
    """Create a flashcard file in a folder."""
    file_path = os.path.join(flashcard_folder_path, folder_name, f"{file_name}.json")
    with open(file_path, "w") as f:
        json.dump({}, f)
    messagebox.showinfo("Info Dialog", f"File '{file_name}.json' created successfully.")


def create_folder_and_file(folder_name, file_name):
    """Create both a folder and a flashcard file."""
    folder_path = os.path.join(flashcard_folder_path, folder_name)
    os.mkdir(folder_path)
    messagebox.showinfo("Info Dialog", f"Folder '{folder_name}' created successfully.")
    create_file(folder_name, file_name)

def add_folder_and_file(command):
    """Handle folder and file creation."""
    command_request = command.get().lower()

    if command_request in ["y", "yes"]:
        folder_name_heading = ctk.CTkLabel(frame1,
                                           text="Enter the name of the folder:")
        folder_name_heading.grid(row=21,
                                 column=1,
                                 sticky="n")

        folder_name = ctk.CTkEntry(frame1)
        folder_name.grid(row=22,
                         column=1,
                         sticky="n")
        folder_name.focus_set()

        folder_name_submit = ctk.CTkButton(
            frame1,
            text="Submit",
            command=lambda: yes_list_files(folder_name.get())
        )
        folder_name_submit.grid(row=23,
                                column=1,
                                sticky="n")

        file_name_heading = ctk.CTkLabel(frame1,
                                         text="Enter the name for your flashcard file:")
        file_name_heading.grid(row=24,
                               column=1,
                               sticky="n",
                               padx=10)

        file_name = ctk.CTkEntry(frame1, width=200)
        file_name.grid(row=25,
                       column=1,
                       sticky="n")

        file_name_submit = ctk.CTkButton(
            frame1,
            text="Submit",
            command=lambda: [create_folder_and_file(folder_name.get(),
                                                    file_name.get()),
                             update_listbox(display)]
        )
        file_name_submit.grid(row=26,
                              column=1,
                              sticky="n")

    elif command_request in ["n", "no"]:
        folder_name_heading = ctk.CTkLabel(frame1,
                                           text="Enter the name of the folder:")
        folder_name_heading.grid(row=21,
                                 column=1,
                                 sticky="n")

        folder_name = ctk.CTkEntry(frame1)
        folder_name.grid(row=22,
                         column=1,
                         sticky="n")

        folder_name_submit = ctk.CTkButton(
            frame1,
            text="Submit",
            command=lambda: no_list_files(folder_name.get())
        )
        folder_name_submit.grid(row=23,
                                column=1,
                                sticky="n")

        file_name_heading = ctk.CTkLabel(frame1,
                                         text="Enter the name for your flashcard file:")
        file_name_heading.grid(row=24,
                               column=1,
                               sticky="n")

        file_name = ctk.CTkEntry(frame1, width=200)
        file_name.grid(row=25,
                       column=1,
                       sticky="n")

        file_name_submit = ctk.CTkButton(
            frame1,
            text="Submit",
            command=lambda: [create_folder_and_file(folder_name.get(),
                                                    file_name.get()),
                             update_listbox(display)]
        )
        file_name_submit.grid(row=26,
                              column=1,
                              sticky="n")
    else:
        from tkinter import messagebox
        messagebox.showerror("Error", "Invalid input. Please enter 'y' or 'n'.")


def open_add_folder_and_file():
    """Create folder/file creation interface."""
    command_header = ctk.CTkLabel(frame1,
                                  text="Do you want to create a new folder? (y/n):")
    command_header.grid(row=18,
                        column=1,
                        sticky="n")

    command = ctk.CTkEntry(frame1)
    command.grid(row=19, column=1)

    command_submit = ctk.CTkButton(
        frame1,
        text="Submit",
        command=lambda: add_folder_and_file(command)
    )
    command_submit.grid(row=20,
                        column=1,
                        sticky="n")


#----- Review Functions -----#
def review_frontend(frame):
    """Create the review interface."""
    folder_name_heading = ctk.CTkLabel(frame,
                                       text="Enter the name of the folder:")
    folder_name_heading.grid(row=1,
                             column=10,
                             sticky="n")

    folder_name = ctk.CTkEntry(frame)
    folder_name.grid(row=2,
                     column=10,
                     sticky="n")
    folder_name.focus_set()

    folder_name_submit = ctk.CTkButton(
        frame,
        text="Submit",
        command=lambda: list_folder_files(folder_name.get())
    )
    folder_name_submit.grid(row=3,
                            column=10,
                            sticky="n")

    file_name_heading = ctk.CTkLabel(frame,
                                     text="Enter the name for your flashcard file:")
    file_name_heading.grid(row=4,
                           column=10,
                           sticky="n")

    file_name = ctk.CTkEntry(frame)
    file_name.grid(row=5,
                   column=10,
                   sticky="n")

    file_name_submit = ctk.CTkButton(
        frame,
        text="Submit",
        command=lambda: review_listbox_backend(folder_name, file_name, frame)
    )
    file_name_submit.grid(row=6,
                          column=10,
                          sticky="n")


def list_folder_files(folder_name):
    """List files in the specified folder."""
    file_path = os.path.join(flashcard_folder_path, folder_name)
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Folder not found.")
        return

    files = os.listdir(file_path)
    messagebox.showinfo("Info", f"Files in folder: {files}")


def review_listbox_backend(folder_name, file_name, frame):
    """Start the review quiz."""
    target_folder = folder_name.get()
    target_file = f"{file_name.get()}.json"
    final_file_path = os.path.join(flashcard_folder_path, target_folder, target_file)

    if not os.path.exists(final_file_path):
        messagebox.showerror("Error", f"File not found:\n{final_file_path}")
        return

    try:
        with open(final_file_path, "r") as f:
            loaded_data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Could not read file:\n{final_file_path}\n\n{e}")
        return

    items = list(loaded_data.items()) if isinstance(loaded_data, dict) else []
    if not items:
        messagebox.showinfo("Info Dialog", "No flashcards found in this file.")
        return

    # Show first question
    question_heading = ctk.CTkLabel(frame,
                                    text=f"1. : {items[0][0]}")
    question_heading.grid(row=8,
                          column=10,
                          sticky="n")

    question_entry = ctk.CTkEntry(frame)
    question_entry.grid(row=9,
                        column=10,
                        sticky="n")
    question_entry.focus_set()

    question_submit = ctk.CTkButton(
        frame,
        text="Submit",
        command=lambda: question_check(question_entry, question_heading)
    )
    question_submit.grid(row=10,
                         column=10,
                         sticky="n")

    # Store state
    question_heading.items = items
    question_heading.idx = 0
    question_heading.correct = 0
    question_heading.wrong = 0
    question_heading.submit_btn = question_submit


#----- Check Functions -----#
def question_check(question_entry, question_heading):
    """Check the answer and move to next question."""
    items = getattr(question_heading, "items", [])
    idx = getattr(question_heading, "idx", 0)
    correct = getattr(question_heading, "correct", 0)
    wrong = getattr(question_heading, "wrong", 0)

    if not items:
        messagebox.showerror("Error", "No review state found.")
        return

    _, expected_answer = items[idx]
    user_answer = question_entry.get().strip()

    if user_answer == expected_answer:
        messagebox.showinfo("Info Dialog", "Correct!")
        question_entry.delete(0, END)
        idx += 1
        correct += 1
        question_heading.idx = idx
        question_heading.correct = correct

        if idx < len(items):
            next_question = items[idx][0]
            question_heading.configure(text=f"{idx + 1}. : {next_question}")
            question_entry.focus_set()
        else:
            total = len(items)
            correct = total - wrong
            messagebox.showinfo("Info Dialog", "All questions completed!")
            messagebox.showinfo("Info Dialog",
                                f"Correct: {correct}, Wrong: {wrong}, Total: {correct}/{total}")
            use_powerup3(question_heading, correct)
            use_power_up2(question_heading, correct)
            try:
                question_heading.destroy()
                question_entry.destroy()
                submit_btn = getattr(question_heading, "submit_btn", None)
                if submit_btn:
                    submit_btn.destroy()
            except TclError:
                pass
    else:
        messagebox.showerror("Info Dialog", "Incorrect!")
        wrong += 1
        question_heading.wrong = wrong
        question_entry.delete(0, END)
        question_entry.focus_set()


#----- Power up Usage -----#
def use_powerup3(question_heading, correct):
    items = getattr(question_heading, "items", [])
    if len(items) == 10:
        if correct == 10:
            use_combo_multiplier()
        else:
            pass
    elif len(items) < 10:
        if correct == len(items):
            use_combo_multiplier()
        else:
            pass
    elif len(items) > 10:
        if correct > 10:
            use_combo_multiplier()
        else:
            pass
    else:
        messagebox.showerror("Error", "No review state found.")

def use_power_up2(question_heading, correct):
    items = getattr(question_heading, "items", [])
    if correct == len(items):
        use_double_coin_multiplier()

#Use combo multiplier
def use_combo_multiplier():
    current_coin = get_current_coins()

    new_coin = current_coin + 25
    with open(combined_path, "w") as q:
        q.write(str(new_coin) + "\n")
        update_listbox(display)
        messagebox.showinfo("Info Dialog", "You have used the combo multiplier! 25 Coins earned!")
        remove_combo_multiplier()
#Use double coin multiplier
def use_double_coin_multiplier():
    current_coin = get_current_coins()
    new_coin = current_coin + 50
    with open(combined_path, "w") as q:
        q.write(str(new_coin) + "\n")
        update_listbox(display)
        messagebox.showinfo("Info", "Double coin multiplier used! 50 Coins earned!")
        remove_double_coin(double_coins_function)


#----- Themes Functions -----#
def save_theme_preference(theme_name):
    """Save the user's theme preference to a file."""
    with open(THEME_PREFERENCE_FILE, "w") as f:
        json.dump({"theme": theme_name}, f)


def load_theme_preference():
    """Load the user's theme preference from file."""
    if os.path.exists(THEME_PREFERENCE_FILE):
        with open(THEME_PREFERENCE_FILE, "r") as f:
            data = json.load(f)
            return data.get("theme", "blue")
    return "blue"


def apply_theme(frame, theme_name):
    """Apply a theme to a frame by name."""
    if theme_name in THEMES:
        theme = THEMES[theme_name]
        apply_theme_to_widgets(
            frame,
            theme["frame_bg"],
            theme["ctrl_bg"],
            fg=theme["fg"],
            listbox_color=theme["listbox_color"],
            entry_color=theme["entry_color"],
            button_bg=theme["button_bg"],
            button_hover=theme["button_hover"],
            button_fg=theme["button_fg"]
        )


def apply_theme_to_widgets(frame, frame_bg, ctrl_bg, fg=None, listbox_color=None,
                           entry_color=None, button_bg=None, button_hover=None, button_fg=None):
    """Apply theme colors to all widgets in a frame."""
    try:
        frame.configure(fg_color=frame_bg)
    except TclError:
        pass

    # Set CustomTkinter appearance mode and color theme
    ctk.set_appearance_mode("light")

    stack = [frame]

    while stack:
        parent = stack.pop()

        for w in parent.winfo_children():
            widget_class = w.winfo_class()

            # Handle CustomTkinter widgets
            if isinstance(w, ctk.CTkFrame):
                try:
                    w.configure(fg_color=frame_bg)
                except (TclError, AttributeError):
                    pass

            elif isinstance(w, ctk.CTkLabel):
                try:
                    w.configure(text_color=fg, fg_color=ctrl_bg)
                except (TclError, AttributeError):
                    pass

            elif isinstance(w, ctk.CTkButton):
                try:
                    w.configure(
                        fg_color=button_bg,
                        hover_color=button_hover,
                        text_color=button_fg
                    )
                except (TclError, AttributeError):
                    pass

            elif isinstance(w, ctk.CTkEntry):
                try:
                    w.configure(
                        fg_color=entry_color,
                        text_color=fg,
                        border_color=button_bg
                    )
                except (TclError, AttributeError):
                    pass

            elif isinstance(w, ctk.CTkScrollbar):
                try:
                    w.configure(
                        fg_color=ctrl_bg,
                        button_color=button_bg,
                        button_hover_color=button_hover
                    )
                except (TclError, AttributeError):
                    pass

            # Handle regular tkinter widgets (like Listbox)
            elif widget_class in ('Label', 'Button', 'Entry', 'Listbox', 'Frame'):
                if fg is not None:
                    try:
                        w.configure(fg=fg)
                    except TclError:
                        pass

                if isinstance(w, Entry):
                    try:
                        w.configure(bg=entry_color)
                    except TclError:
                        pass

                elif isinstance(w, Listbox):
                    try:
                        w.configure(selectbackground=ctrl_bg)
                        w.configure(bg=listbox_color)
                        w.configure(selectforeground=fg or "black")
                    except TclError:
                        pass

                elif isinstance(w, Button):
                    try:
                        w.configure(bg=ctrl_bg)
                        if fg is not None:
                            w.configure(activeforeground=fg)
                            w.configure(activebackground=ctrl_bg)
                    except TclError:
                        pass

                elif isinstance(w, Label):
                    try:
                        w.configure(bg=ctrl_bg)
                    except TclError:
                        pass

                elif isinstance(w, Frame):
                    try:
                        w.configure(bg=frame_bg)
                    except TclError:
                        pass

            stack.append(w)


def create_theme_buttons(parent, frame1, frame2, frame3):
    """Create theme selection buttons."""
    theme_frame = ctk.CTkFrame(parent)

    def change_theme(theme_name):
        """Change theme and save preference."""
        save_theme_preference(theme_name)
        apply_theme(frame1, theme_name)
        apply_theme(frame2, theme_name)
        apply_theme(frame3, theme_name)

    # Create theme buttons with CustomTkinter
    pink_btn = ctk.CTkButton(theme_frame,
                             text="Pink Theme",
                             command=lambda: change_theme("pink"),
                             width=100)
    pink_btn.grid(row=0, column=0, padx=5, pady=5)

    blue_btn = ctk.CTkButton(theme_frame,
                             text="Blue Theme",
                             command=lambda: change_theme("blue"),
                             width=100)
    blue_btn.grid(row=0, column=1, padx=5, pady=5)

    white_btn = ctk.CTkButton(theme_frame,
                              text="White Theme",
                              command=lambda: change_theme("white"),
                              width=100)
    white_btn.grid(row=0,
                   column=2,
                   padx=5,
                   pady=5)

    return theme_frame

#----- UI Functions -----#
def update_listbox(display):
    """Refresh the listbox."""
    if display is None:
        return

    # Clear the whole listbox:
    display.delete(0, END)

    # Re-scan and input:
    if os.path.exists(flashcard_folder_path):
        folders = [f for f in os.listdir(flashcard_folder_path)
                   if os.path.isdir(os.path.join(flashcard_folder_path, f))]
        for folder in sorted(folders):
            display.insert(END, folder)


#----- Main UI -----#
def main():
    """Main application entry point."""
    global frame1, frame2, display, frame3

    #Initialize the application
    initialize_currency()
    initialize_inventory()

    # Set CustomTkinter appearance
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Flashcard Feature")
    root.geometry("1400x600")

    # Create tabview instead of notebook
    flashcard = ctk.CTkTabview(root)
    # Add tabs first, then use a single geometry manager (pack) exactly once.
    flashcard.add("Home")
    flashcard.add("Flashcards")
    flashcard.add("Shop")
    flashcard.pack(fill="both", expand=1)

    # Frame 2 - Home (FIRST tab)
    frame2 = flashcard.tab("Home")

    # Frame 1 - Flashcards (SECOND tab)
    frame1 = flashcard.tab("Flashcards")

    # Frame 3 - Shop (THIRD tab)
    frame3 = flashcard.tab("Shop")
    # select_powerup moved later so shop widgets and theme frames are created first

    # ===== FRAME 1 UI (FLASHCARDS PAGE) =====

    # Flashcard list
    heading1 = ctk.CTkLabel(frame1,
                            text="Available Flashcard",
                            font=("Arial", 20))
    heading1.grid(row=0,
                  column=0,
                  rowspan=2,
                  columnspan=3,
                  pady=10)

    list_frame = ctk.CTkFrame(frame1)
    list_frame.grid(row=2,
                    column=0,
                    columnspan=3,
                    rowspan=15,
                    sticky="nsew",
                    padx=10,
                    pady=10)

    display = Listbox(list_frame,
                      width=50,
                      height=10,
                      font=("Arial", 12))
    for file in flashcard_files:
        display.insert(END, file)
    display.grid(row=0,
                 column=0,
                 sticky="nsew",
                 padx=5,
                 pady=5)

    scrollbar = ctk.CTkScrollbar(list_frame,
                                 orientation="vertical",
                                 command=display.yview)
    scrollbar.grid(row=0,
                   column=1,
                   rowspan=10,
                   sticky="ns",
                   pady=5)

    display.config(yscrollcommand=scrollbar.set)

    list_frame.grid_rowconfigure(0, weight=2)
    list_frame.grid_columnconfigure(0, weight=2)

    # Rename section
    rename_header = ctk.CTkLabel(frame1,
                                 text="Rename",
                                 font=("Arial", 20))
    rename_header.grid(row=17,
                       column=0,
                       sticky="nsew",
                       pady=5)
    open_rename()

    # Add folder section
    add_folder_header = ctk.CTkLabel(frame1,
                                     text="Add Folder",
                                     font=("Arial", 15))
    add_folder_header.grid(row=17,
                           column=1,
                           sticky="n",
                           rowspan=2,
                           pady=5)
    open_add_folder_and_file()

    # Edit section
    edit_title = ctk.CTkLabel(frame1,
                              text="     Edit     ",
                              font=("Arial", 15))
    edit_title.grid(row=0,
                    column=3,
                    sticky="s",
                    columnspan=3)
    edit_flashcards_frontend()

    # Review section
    review_heading = ctk.CTkLabel(frame1,
                                  text="     Review     ",
                                  font=("Arial", 15))
    review_heading.grid(row=0,
                        column=10,
                        sticky="n",
                        columnspan=3)
    review_frontend(frame1)

    # Theme buttons for frame1
    theme_frame1 = create_theme_buttons(frame1,
                                        frame1,
                                        frame2,
                                        frame3)
    theme_frame1.grid(row=30,
                      column=29,
                      columnspan=3,
                      padx=15,
                      pady=15,
                      sticky="se")

    # ===== FRAME 2 UI (HOME PAGE) =====

    # Welcome heading
    welcome_heading = ctk.CTkLabel(
        frame2,
        text="Welcome to Pro Bo!",
        font=("Arial", 20, "bold")
    )
    welcome_heading.grid(row=0,
                         column=6,
                         columnspan=3,
                         pady=20)

    # Welcome text
    welcome_text = ctk.CTkLabel(
        frame2,
        text="""Pro Bo is a study app that helps you study better.
    I hope you find this app useful! It is free to use.

    If you have any questions or suggestions,
    please feel free to contact me:""",
        font=("Arial", 12),
        justify="center"
    )
    welcome_text.grid(row=1,
                      column=6,
                      columnspan=3,
                      pady=10)

    # Function to open email
    def open_email():
        email = "mingl_2028@concordian.org"
        subject = "Feedback about Pro Bo App"
        body = "Hello,\n\nI have a question/suggestion about Pro Bo:\n\n"

        # Create mailto link with pre-filled subject and body
        mailto_link = f"mailto:{email}?subject={subject}&body={body}"
        webbrowser.open(mailto_link)

    # Clickable email label (looks like a link)
    email_label = ctk.CTkLabel(
        frame2,
        text="✉ mingl_2028@concordian.org",
        font=("Arial", 12, "underline"),
        text_color="blue",
        cursor="hand2"
    )
    email_label.grid(row=2,
                     column=6,
                     columnspan=3,
                     pady=10)
    email_label.bind("<Button-1>", lambda e: open_email())

    # Email button
    email_button = ctk.CTkButton(
        frame2,
        text="📧 Contact Me",
        command=open_email,
        width=150
    )
    email_button.grid(row=3,
                      column=6,
                      columnspan=3)

    # Habit listbox
    habit_listbox = Listbox(frame2,
                            width=35,  # increase this number to show longer items
                            height=15,
                            font=("Arial", 14))
    for i in habit_trainer_files:
        habit_listbox.insert(END, i)
    habit_listbox.grid(row=2,
                       column=0,
                       rowspan=9,
                       columnspan=5,
                       sticky="nsew",
                       padx=5,
                       pady=5)

    # Make sure frame2 gives the listbox space if needed
    frame2.grid_rowconfigure(2, weight=1)

    # Habit buttons
    habit_check_button = ctk.CTkButton(frame2, text="Check Habit",
                                       command=lambda: on_check(habit_listbox),
                                       width=150)
    habit_check_button.grid(row=2, column=5)

    habit_delete_button = ctk.CTkButton(frame2, text="Delete Habit",
                                    command=lambda: delete_habit(habit_listbox),
                                    width=150)
    habit_delete_button.grid(row=3, column=5)

    habit_create_button = ctk.CTkButton(frame2, text="Create Habit",
                                        command=lambda: create_habit_frontend(frame2, habit_create_button, habit_listbox),
                                        width=150)
    habit_create_button.grid(row=4,
                             column=5)

    # Theme buttons for frame2
    theme_frame2 = create_theme_buttons(frame2,
                                        frame1,
                                        frame2,
                                        frame3)
    # place theme buttons to the right of the Contact Me button on the same row
    theme_frame2.grid(row=3,
                      column=8,
                      padx=(10, 20),
                      pady=5,
                      sticky="w")
    # refresh layout so buttons are realized immediately
    root.update_idletasks()

    # ===== FRAME 3 UI (SHOP PAGE) =====

    # Shop title
    shop_title = ctk.CTkLabel(frame3,
                              text="Welcome to the Shop",
                              font=("Arial", 20, "bold"))
    shop_title.grid(row=0,
                   column=0,
                   columnspan=3,
                   pady=10)

    # Shop description
    shop_description = ctk.CTkLabel(frame3,
                                    text="Use coins to buy power-ups that help you with your habits.",
                                    font=("Arial", 12),
                                    justify="center")
    shop_description.grid(row=1,
                         column=0,
                         columnspan=3,
                         pady=10)

    # Theme buttons for frame3
    theme_frame3 = create_theme_buttons(frame3,
                                        frame1,
                                        frame2,
                                        frame3)
    theme_frame3.grid(row=5,
                      column=3,
                      rowspan=3,
                      padx=15,
                      pady=15,
                      sticky="e")
    root.update_idletasks()

    # Now initialize shop widgets that rely on the frames existing
    select_powerup(frame3)

    # Load and apply saved theme
    saved_theme = load_theme_preference()
    apply_theme(frame1, saved_theme)
    apply_theme(frame2, saved_theme)
    apply_theme(frame3, saved_theme)
    # ensure layout is up-to-date so theme buttons render immediately
    root.update_idletasks()
    root.mainloop()

main()