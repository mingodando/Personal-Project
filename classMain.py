import os
from tkinter import *
import customtkinter as ctk
import json
from tkinter import messagebox
from datetime import datetime

class Probo:
    def __init__(self):
        self.coin_label = None
        self.flashcard = None
        self.home = None
        self.shop = None
        self.timer = None
        self.display = None
        self.setting = None
        self.frame = None
        self.folder_name = None

        # ----- Create Folder Path -----#
        self.flashcard_folder = "Flashcards Files"
        self.habit_folder = "Habit Trainer"
        self.game_folder = "Game"

        #----- Inventory File Paths -----#
        currency_file_name = "current_currency.txt"
        self.combined_path = os.path.join(self.game_folder, currency_file_name)
        self.inventory_path = os.path.join(self.game_folder, "inventory.json")

        self.POWER_UPS = """
            1. Habit Revive: Revives a broken habit streak (50 Coins)
            2. Double Coins: Double reward for next review session (25 Coins)
            3. Combo Multiplier (review): Get 30 coins immediately when getting 10 correct answers in a row (15 Coins)    
        """

        # ----- Font Size ----- #
        self.TITLE_FONT = ("Arial", 20, "bold")
        self.SUBTITLE_FONT = ("Arial", 15, "bold")
        self.REGULAR_FONT = ("Arial", 13)

        #----- Folder Path -----#
        self.flashcard_folder = "Flashcards Files"
        self.habit_folder = "Habit Trainer"
        self.game_folder = "Game"

        self.current_directory = os.getcwd()
        self.flashcard_folder_path = os.path.join(self.current_directory, self.flashcard_folder)
        self.habit_trainer_folder_path = os.path.join(self.current_directory, self.habit_folder)
        self.game_folder_path = os.path.join(self.current_directory, self.game_folder)

        #----- Font -----#
        self.TITLE_FONT = ("Arial", 20, "bold")
        self.SUBTITLE_FONT = ("Arial", 15, "bold")
        self.REGULAR_FONT = ("Arial", 13)

        self.check_path(self.flashcard_folder_path, self.habit_trainer_folder_path, self.game_folder_path)

        self.flashcard_files = os.listdir(self.flashcard_folder_path)
        self.habit_trainer_files = os.listdir(self.habit_trainer_folder_path)

        self.TIMESTAMP_FORMAT = "%Y-%m-%d"

        self.THEME_PREFERENCE_FILE = os.path.join(os.path.dirname(__file__), "..", "theme_preference.json")

        #----- Theme Configurations -----#
        self.THEMES = {
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
            },
            "green": {
                "frame_bg": "#9AFF82",
                "ctrl_bg": "#B4FFA1",
                "fg": "94FFB2",
                "listbox_color": "#94FFB2",
                "entry_color": "#FFFFFF",
                "button_bg": "#00781C",
                "button_hover": "#06691F",
                "button_fg": "#FFFFFF"
            },
            "purple": {
                "frame_bg": "#D9B3FF",
                "ctrl_bg": "#ECB9FF",
                "fg": "#6B21A8",
                "listbox_color": "#C0B6FD",
                "entry_color": "#FFFFFF",
                "button_bg": "#8B5CF6",
                "button_hover": "#7C3AED",
                "button_fg": "#FFFFFF"
            },
            "yellow": {
                "frame_bg": "#FFFF99",
                "ctrl_bg": "#FFFFCC",
                "fg": "#996600",
                "listbox_color": "#FFE29D",
                "entry_color": "#FFE309",
                "button_bg": "#FFCC00",
                "button_hover": "#CC9900",
                "button_fg": "#000000"
            }
        }

        # CustomTkinter appearance modes
        self.CTK_APPEARANCE_MODES = {
            "pink": "light",
            "blue": "light",
            "white": "light",
            "green": "light",
            "purple": "light",
            "yellow": "light"
}

    @staticmethod
    def check_path(flashcard_folder_path, habit_trainer_folder_path, game_folder_path):
        if not os.path.exists(flashcard_folder_path):
            os.makedirs(flashcard_folder_path, exist_ok=True)
        if not os.path.exists(habit_trainer_folder_path):
            os.makedirs(habit_trainer_folder_path, exist_ok=True)
        if not os.path.exists(game_folder_path):
            os.makedirs(game_folder_path, exist_ok=True)

    @staticmethod
    def check_empty(file_path):
        #Check if file is empty
        with open(file_path, 'r') as f:
            content = f.read()
            if not content:
                return True
            else:
                return False

    @staticmethod
    def center_window(window, width, height):
        #Centers window based on screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        center_x = int(screen_width / 2) - (width / 2)
        center_y = int(screen_height / 2) - (height / 2)

        window.geometry(f'{width}x{height}+{int(center_x)}+{int(center_y)}')

    def tick(self, remaining, time_label, tick, min_entry, sec_entry, start_btn, stop_btn):
        if getattr(time_label, "_stopped", False):
            return

        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_label.configure(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

        if remaining > 0:
            time_label._after_id = time_label.after(1000, tick, remaining - 1)
        else:
            if not getattr(time_label, "_stopped", False):
                print("Time's up!")
                self.on_finish(min_entry, sec_entry, start_btn, stop_btn)

    def timer_function(self, total_seconds, time_label, min_entry, sec_entry, start_btn, stop_btn):
        time_label._stopped = False

        prev_after_id = getattr(time_label, "_after_id", None)
        if prev_after_id:
            try:
                time_label.after_cancel(prev_after_id)
            except KeyError:
                pass
            time_label._after_id = None

            self.tick(total_seconds, time_label, self.tick, min_entry, sec_entry, start_btn, stop_btn)

    @staticmethod
    def on_finish(min_entry, sec_entry, start_btn, stop_btn):
        min_entry.configure(state="normal")
        sec_entry.configure(state="normal")
        start_btn.configure(state="normal")
        stop_btn.configure(state="disabled")

    @staticmethod
    def calculate_seconds(min_entry, sec_entry):
        try:
            mins_text = (min_entry.get() or "0").strip()
            secs_text = (sec_entry.get() or "0").strip()
            mins = int(mins_text)
            secs = int(secs_text)

        except ValueError:
            print("Invalid input")
            return None
        if mins < 0 or secs < 0 or secs >= 60:
            print("Invalid input")
            return None
        return mins * 60 + secs

    def start_timer(self, min_entry, sec_entry, time_label, start_btn, stop_btn):
        total = self.calculate_seconds(min_entry, sec_entry)

        if total is None:
            return
        min_entry.configure(state="disabled")
        sec_entry.configure(state="disabled")
        start_btn.configure(state="disabled")
        stop_btn.configure(state="normal")

        self.timer_function(total, time_label, min_entry, sec_entry, start_btn, stop_btn)

    @staticmethod
    def stop_timer(min_entry, sec_entry, time_label, start_btn, stop_btn):
        time_label._stopped = True
        after_id = getattr(time_label, "_after_id", None)
        time_label.config(text="00:00:00")

        if after_id:
            try:
                time_label.after_cancel(after_id)
            except KeyError:
                pass
            time_label._after_id = None

        min_entry.configure(state="normal")
        sec_entry.configure(state="normal")
        start_btn.configure(state="normal")
        stop_btn.configure(state="disabled")
        return

    #===== Flashcard Functions =====#
    def no_list_files(self, folder_name):
        #List files in a folder if it exists.
        file_path = os.path.join(self.flashcard_folder_path, folder_name)
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")
            return

        list_file = os.listdir(file_path)
        if folder_name in self.flashcard_files:
            messagebox.showinfo("Info Dialog", f"Files in folder: {list_file}")
        else:
            messagebox.showerror("Error", "Please enter a valid folder name.")

    def yes_list_files(self, folder_name):
        #Check if the folder exists and list flashcard files.

        if folder_name in self.flashcard_files:
            messagebox.showerror("Error", "Folder already exists. Please enter a different name.")
            return
        elif folder_name not in self.flashcard_files:
            messagebox.showinfo("Info Dialog", str(self.flashcard_files))

    #----- Edit Flashcard Functions -----#
    def add_card(self, file_name, folder_name, frame):
        #Add a flashcard to a file
        add_card_file_path = os.path.join(self.flashcard_folder_path, folder_name, file_name)

        #Load existing data or start fresh
        self.data = {}
        if os.path.exists(add_card_file_path):
            with open(add_card_file_path, "r") as d:
                try:
                    loaded = json.load(d)
                    if isinstance(loaded, dict):
                        self.data = loaded
                    else:
                        messagebox.showerror("Error", "Unsupported file format. Expected a JSON object.")
                        return
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load data. Starting fresh.")

        #Create inputs (UI)
        question_heading = ctk.CTkLabel(frame,
                                        text="Enter the question:",
                                        font=self.SUBTITLE_FONT)
        question_heading.grid(row=20,
                              column=6,
                              sticky="n",
                              pady=5)
        question = ctk.CTkEntry(frame, width=200, font=self.REGULAR_FONT)
        question.grid(row=21,
                      column=6,
                      sticky="n",
                      pady=5)

        answer_heading = ctk.CTkLabel(frame,
                                      text="Enter the answer:",
                                      font=self.SUBTITLE_FONT)
        answer_heading.grid(row=22,
                            column=6,
                            sticky="n",
                            pady=5)
        self.answer = ctk.CTkEntry(frame, width=200, font=self.REGULAR_FONT)
        self.answer.grid(row=23,
                    column=6,
                    sticky="n",
                    pady=5)
    def on_add(self, question, answer, add_card_file_path, edit_listbox):
        #Handle adding a card
        q = question.get().strip()
        a = answer.get().strip()

        if not q or not a:
            messagebox.showerror("Error", "Both question and answer are required.")
            return

        self.data[q] = a

        try:
            with open(add_card_file_path, "w") as f:
                json.dump(self.data, f, indent=4)
        except OSError as t:
            messagebox.showerror("Error", f"Failed to save:\n{add_card_file_path}\n\n{t}")
            return

        #Update listbox
        edit_listbox.insert(END, f"{q}: {a}")

        #Clear inputs
        question.delete(0, END)
        answer.delete(0, END)
        question.focus_set()

        self.add_btn = ctk.CTkButton(self.frame,
                                     text="Add Card",
                                     command=self.on_add,
                                     width=100,
                                     hover=False,
                                     font=self.REGULAR_FONT)
        self.add_btn.grid(row=28,
                         column=6,
                         sticky="n",
                         pady=5)

        saved_theme = self.load_theme_preference()
        self.apply_theme(self.frame, saved_theme)

    def edit_card(self, file_name, folder_name, item_selected, frame, edit_listbox):
        #Save edited flashcard.
        self.item_selection = edit_listbox.curselection()
        if not self.item_selection:
            return

        item_indices = self.item_selection[0]
        item_selected = edit_listbox.get(item_indices)
        print(f"Selected item: {item_selected}")

        selected_question = item_selected.split(":")[0].strip()
        selected_answer = item_selected.split(":")[1].strip() if ":" in item_selected else ""

        #Create Edit Inputs
        edit_question_heading = ctk.CTkLabel(frame,
                                            text="Edit the question:",
                                            font=self.SUBTITLE_FONT)
        edit_question_heading.grid(row=20,
                                   column=7,
                                   sticky="n",
                                   pady=5)
        edit_question = ctk.CTkEntry(frame, width=200)
        edit_question.grid(row=21,
                           column=7,
                           sticky="n",
                           pady=5)
        edit_answer_heading = ctk.CTkLabel(frame,
                                           text="Edit the answer:",
                                           font=self.SUBTITLE_FONT)
        edit_answer_heading.grid(row=22,
                                 column=7,
                                 sticky="n",
                                 pady=5)
        edit_answer = ctk.CTkEntry(frame, width=200)
        edit_answer.grid(row=23,
                         column=7,
                         sticky="n",
                         pady=5)

        edit_done_button = ctk.CTkButton(
            frame,
            text="Done",
            width=100,
            font=self.REGULAR_FONT,
            command=lambda: self.edit_done(file_name,
                                           folder_name,
                                           edit_question,
                                           edit_answer,
                                           item_selected)
        )
        edit_done_button.grid(row=28,
                              column=7,
                              sticky="n",
                              pady=5)

        saved_theme = self.load_theme_preference()
        self.apply_theme(frame, saved_theme)

    def edit_done(self, file_name, folder_name, edit_question, edit_answer, item_selected):
        #Save edited flashcard.
        target_file = f"{file_name}.json" if not file_name.lower().endswith(".json") else file_name
        final_file_path = os.path.join(self.flashcard_folder_path, folder_name, target_file)

        #Load Data
        with open(final_file_path, "r") as f:
            data = json.load(f)

        #Extract values
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

    @staticmethod
    def on_select(_, edit_listbox, file_name, folder_name, flashcard, edit_card):
        item_selection = edit_listbox.curselection()
        if item_selection:
            item_indices = item_selection[0]
            item_selected = edit_listbox.get(item_indices)
            edit_card(edit_listbox, file_name, folder_name, item_selected, flashcard)

    def edit_flashcard_cl(self, file_name, folder_name):
        saved_theme = self.load_theme_preference()
        self.apply_theme(self.flashcard, saved_theme)

        #Load flashcards for editing
        json_file_name = f"{file_name.lower()}.json"
        folder_name = folder_name.lower()
        final_file_path = os.path.join(self.flashcard_folder_path, folder_name, json_file_name)

        #Create listbox frame
        edit_frame = ctk.CTkFrame(self.flashcard)
        edit_frame.grid(row=4,
                        column=6,
                        rowspan=15,
                        columnspan=3,
                        sticky="nsew")
        edit_frame.grid_rowconfigure(0, weight=1)
        edit_frame.grid_columnconfigure(0, weight=1)

        edit_listbox = Listbox(edit_frame,
                               width=80,
                               height=10)
        edit_listbox.grid(row=0,
                          column=0,
                          sticky="nsw")

        edit_scrollbar = ctk.CTkScrollbar(edit_frame,
                                          orientation='vertical',
                                          command=edit_listbox.yview)
        edit_scrollbar.grid(row=0,
                            column=1,
                            sticky="nsw")

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
        add_heading = ctk.CTkLabel(self.flashcard,
                                   text="Add",
                                   font=self.SUBTITLE_FONT)
        add_heading.grid(row=19,
                         column=6,
                         sticky="s")
        self.add_card(edit_listbox,
                 json_file_name,
                 folder_name)

        #Edit Section
        edit_heading = ctk.CTkLabel(self.flashcard,
                                   text="Edit",
                                   font=self.SUBTITLE_FONT)
        edit_heading.grid(row=19,
                         column=7,
                         sticky="s")

        edit_listbox.bind("<<ListboxSelect>>", lambda event: self.on_select(event, edit_listbox, json_file_name, folder_name, self.flashcard, self.edit_card))

    @staticmethod
    def _on_display_select(_, display, folder_name):
        sel = display.curselection()
        if not sel:
            return
        try:
            idx = int(sel[0])
        except (ValueError, TypeError):
            idx = sel[0]
        value = display.get(idx)
        #Put selected folder name into the entry
        folder_name.delete(0, END)
        folder_name.insert(0, value)

    def edit_flashcard_frontend(self, display):
        #Create eidt flashcards interface and autofill the folder name
        folder_name_heading = ctk.CTkLabel(self.flashcard, text="Enter Folder Name:", font=self.SUBTITLE_FONT)
        folder_name_heading.grid(row=1, column=4, sticky="n")

        folder_name = ctk.CTkEntry(self.flashcard)
        folder_name.grid(row=2, column=4, sticky="n")

        folder_name_submit = ctk.CTkButton(self.flashcard,
                                           text="Submit",
                                           command=lambda: self.no_list_files(self.folder_name.get()))
        folder_name_submit.grid(row=3, column=4, sticky="n")

        display.bind("<<ListboxSelect>>", lambda event: self._on_display_select(event, display, folder_name))

        #File Name widgets
        file_name_heading = ctk.CTkLabel(self.flashcard, text="Select File Name:", font=self.SUBTITLE_FONT)
        file_name_heading.grid(row=1, column=5, sticky="n")

        file_name_entry = ctk.CTkEntry(self.flashcard)
        file_name_entry.grid(row=2, column=5, sticky="n")

        file_name_submit = ctk.CTkButton(self.flashcard,
                                         text="Submit",
                                         command=lambda: self.no_list_files(self.folder_name.get()))
        file_name_submit.grid(row=6, column=4, sticky="n")

    def buy_powerup1(self):
        current_coin = self.get_current_coins()

        #Check if user have enough coins
        if current_coin < 50:
            messagebox.showerror("Insufficient Coins", "You don't have enough coins to buy this powerup.")
            return

        #Write new coin amount
        new_coin = current_coin - 50
        with open(self.combined_path, 'w') as d:
            d.write(str(new_coin) + "\n")

        self.add_to_inventory("Habit Revive", 1)

        messagebox.showinfo("Powerup Purchased", "You have successfully purchased Habit Revive!")

        self.update_coin_display()

    def buy_powerup2(self):
        current_coin = self.get_current_coins()

        # Check if user has enough coins
        if current_coin < 50:
            messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
            return

        # Write new coin amount
        new_coin = current_coin - 50
        with open(self.combined_path, "w") as d:
            d.write(str(new_coin) + "\n")

        # Add to inventory
        self.add_to_inventory("double_coins", 1)

        messagebox.showinfo("Success", "You bought 1 Double Coin Potion!\nCheck your inventory to use it.")

        # Update the display
        self.update_coin_display()

    def buy_powerup3(self):
        current_coin = self.get_current_coins()

        # Check if user has enough coins
        if current_coin < 15:
            messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 15.")
            return

        # Write new coin amount
        new_coin = current_coin - 15
        with open(self.combined_path, "w") as d:
            d.write(str(new_coin) + "\n")

        # Add to inventory
        self.add_to_inventory("combo_multiplier", 1)

        messagebox.showinfo("Success", "You bought 1 Combo Multiplier!\nCheck your inventory to use it.")

        # Update the display
        self.update_coin_display()

    # ===== INVENTORY MANAGEMENT FUNCTIONS =====
    def initialize_inventory(self,):
        """Create the inventory file if it doesn't exist"""
        if not os.path.exists(self.inventory_path):
            initial_inventory = {
                "habit_revive": 0,
                "double_coins": 0,
                "combo_multiplier": 0
            }
            with open(self.inventory_path, "w") as f:
                json.dump(initial_inventory, f, indent=4)

    def get_inventory(self):
        """Read and return the current inventory"""
        self.initialize_inventory()
        with open(self.inventory_path, "r") as f:
            return json.load(f)

    def add_to_inventory(self, item_key, quantity=1):
        """Add items to inventory"""
        inventory = self.get_inventory()
        inventory[item_key] = inventory.get(item_key, 0) + quantity
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)

    def remove_from_inventory(self, item_key, quantity=1):
        """Remove items from the inventory (returns True if successful)"""
        inventory = self.get_inventory()
        if inventory.get(item_key, 0) >= quantity:
            inventory[item_key] -= quantity
            with open(self.inventory_path, "w") as f:
                json.dump(inventory, f, indent=4)
            return True
        return False

    # ===== COIN MANAGEMENT FUNCTIONS =====
    def initialize_currency(self):
        """Create currency files if it doesn't exist"""
        if not os.path.exists(self.combined_path):
            with open(self.combined_path, "w") as f:
                f.write("100\n")

    def get_current_coins(self):
        """Helper function to read the current coin amount from the file"""
        try:
            with open(self.combined_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    return 0
                last_line = lines[-1].strip()
                return int(last_line)
        except (FileNotFoundError, ValueError):
            return 0

    def update_coin_display(self):
        """Update the coin display label"""
        if self.coin_label:
            current_coins = self.get_current_coins()
            self.coin_label.configure(text=f"Current coins: {current_coins}")

    # ===== INVENTORY UI FUNCTIONS =====
    def habit_revive_function(self, file_path):
        inventory = self.get_inventory()
        if inventory.get("habit_revive", 0) >= 1:
            self.remove_from_inventory("habit_revive", 1)
            messagebox.showinfo("Success", "Habit Revive used! Your streak is safe.")
        else:
            response = messagebox.askyesno("Buy Powerup?", "Do you want to buy more powerups?")
            if response:
                self.open_inventory()
            elif not response:
                self.failed_streak(file_path)

    def double_coins_function(self, file_path):
        inventory = self.get_inventory()
        if inventory.get("double_coins", 0) >= 1:
            self.remove_from_inventory("double_coins", 1)
            messagebox.showinfo("Success", "Double Coins powerup used! Double reward for next review session")
        else:
            response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
            if not response:
                self.failed_streak(file_path)

    def remove_habit_revive(self, habit_revive_function):
        """Use a Habit Revive from inventory"""
        yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, your streak will stay alive.")
        if yes_no:
            print("User said yes")
            if callable(habit_revive_function):
                habit_revive_function()
            if self.remove_from_inventory("habit_revive", 1):
                messagebox.showinfo("Used!", "Habit Revive used successfully!")
            else:
                messagebox.showwarning("Not Available", "You don't have any Habit Revives!")
                messagebox.showinfo("Buy More", "Go to the shop to buy more and come back")
        else:
            print("User said no")

    def remove_double_coin(self, double_coin_function):
        """Use a Double Coins potion from inventory"""

        yes_no = messagebox.askyesno("Use Powerup",
                                     "If you use this powerup, you will double the coins for next review session.")
        if yes_no:
            print("User said yes")
            if callable(double_coin_function):
                double_coin_function()
            if self.remove_from_inventory("double_coins", 1):
                messagebox.showinfo("Used!", "Double Coins Powerup used successfully!")
                self.open_inventory()
            else:
                messagebox.showwarning("Not Available", "You don't have any Double Coins!")
        else:
            print("User said no")

    def remove_combo_multiplier(self, combo_multiplier_function=None):
        """Use a Combo Multiplier from inventory"""
        yes_no = messagebox.askyesno("Use Powerup",
                                     "If you use this powerup, you will get 30 coins immediately when getting 10 correct answers in a row during review.")
        if yes_no:
            print("User said yes")
            if callable(combo_multiplier_function):
                combo_multiplier_function()
            if self.remove_from_inventory("combo_multiplier", 1):
                messagebox.showinfo("Used!", "Combo Multiplier used successfully!")
                self.open_inventory()
            else:
                messagebox.showwarning("Not Available", "You don't have any Combo Multipliers!")
        else:
            print("User said no")

    def open_inventory(self):
        """Open the inventory window"""
        inventory_window = ctk.CTkToplevel()
        inventory_window.title("Inventory")
        inventory_window.geometry("400x310")

        # Title
        title_label = ctk.CTkLabel(inventory_window,
                                   text="Your Power-Ups",
                                   font=self.SUBTITLE_FONT)
        title_label.grid(pady=10)

        # Get current inventory
        inventory = self.get_inventory()

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
                      anchor="w",
                      font=self.REGULAR_FONT)
         .grid(padx=5))
        (ctk.CTkButton(habit_frame,
                       text="Use",
                       width=80,

                       command=lambda: self.remove_habit_revive(None))
         .grid(padx=5))

        # Double Coins
        double_frame = ctk.CTkFrame(items_frame)
        double_frame.grid(pady=5, padx=10)
        (ctk.CTkLabel(double_frame,
                      text=f"Double Coins: {inventory['double_coins']}",
                      width=200, anchor="w", font=self.REGULAR_FONT)
         .grid(padx=5))
        (ctk.CTkButton(double_frame,
                       text="Use", width=80,
                       command=lambda: self.remove_double_coin(None))
         .grid(padx=5))

        # Combo Multiplier
        combo_frame = ctk.CTkFrame(items_frame)
        combo_frame.grid(pady=5,
                         padx=10)
        (ctk.CTkLabel(combo_frame,
                      text=f"Combo Multiplier: {inventory['combo_multiplier']}",
                      width=200, anchor="w", font=self.REGULAR_FONT)
         .grid(padx=5))
        (ctk.CTkButton(combo_frame,
                       text="Use",
                       width=80,

                       command=lambda: self.remove_combo_multiplier(None))
         .grid(padx=5))

        # Close button
        ctk.CTkButton(inventory_window, text="Close", command=inventory_window.destroy).grid(pady=10)

        saved_theme = self.load_theme_preference()
        self.apply_theme(inventory_window, saved_theme)
        self.apply_theme(habit_frame, saved_theme)
        self.apply_theme(double_frame, saved_theme)
        self.apply_theme(combo_frame, saved_theme)

    def select_powerup(self, root):
        global coin_label

        # Display current coins at the top
        coin_label = ctk.CTkLabel(root,
                                  text="",
                                  font=self.REGULAR_FONT)

        coin_label.grid(row=3,
                        column=0,
                        columnspan=2,
                        pady=10)
        self.update_coin_display()

        # Inventory button
        inventory_btn = ctk.CTkButton(self.shop,
                                      text="Open Inventory",
                                      command=lambda: self.open_inventory())
        inventory_btn.grid(row=5,
                           column=0,
                           columnspan=2,
                           pady=5)

        # Power-ups:
        power_up = ctk.CTkLabel(self.shop,
                                text=f"""Here are the available power-ups:
                                    {self.POWER_UPS}
                                    """,
                                font=self.REGULAR_FONT)
        power_up.grid(row=6,
                      rowspan=3,
                      column=0,
                      columnspan=2,
                      pady=10)

        # Power-up 1
        power_up1 = ctk.CTkLabel(self.shop,
                                 text="Habit Revive (50 coins)",
                                 anchor="w", font=self.SUBTITLE_FONT)
        power_up1.grid(row=9,
                       column=0,
                       pady=5,
                       sticky="w",
                       padx=10)

        buy_power_up1 = ctk.CTkButton(self.shop,
                                      command=self.buy_powerup1,
                                      text="Buy",
                                      width=80)

        buy_power_up1.grid(row=9,
                           column=1,
                           pady=5)

        # Power-up 2
        power_up2 = ctk.CTkLabel(self.shop,
                                 text="Double Coins (50 coins)",
                                 anchor="w", font=self.SUBTITLE_FONT)
        power_up2.grid(row=10,
                       column=0,
                       pady=5,
                       sticky="w",
                       padx=10)

        buy_power_up2 = ctk.CTkButton(self.shop,
                                      command=self.buy_powerup2,
                                      text="Buy",
                                      width=80)
        buy_power_up2.grid(row=10,
                           column=1,
                           pady=5)

        # Power-up 3
        power_up3 = ctk.CTkLabel(self.shop,
                                 text="Combo Multiplier (15 coins)",
                                 anchor="w", font=self.SUBTITLE_FONT)
        power_up3.grid(row=11,
                       column=0,
                       pady=5,
                       sticky="w",
                       padx=10)
        buy_power_up3 = ctk.CTkButton(self.shop,
                                      command=self.buy_powerup3,
                                      text="Buy",
                                      width=80)
        buy_power_up3.grid(row=11,
                           column=1,
                           pady=5)

    #===== Habit Functions =====#
    def read_last_timestamp(self, file_path: str):
        #Read the last timestamp from a habit file.
        with open(file_path, "r") as f:
            content = f.readlines()
            if content:
                content = content[-1].strip()
                return datetime.strptime(content, self.TIMESTAMP_FORMAT)
        return None

    def write_timestamp(self, file_path: str, timestamp: datetime):
        #Write a timestamp to a habit file.
        with open(file_path, "a") as f:
            f.write(timestamp.strftime(self.TIMESTAMP_FORMAT) + "\n")

    def read_streak(self, file_path: str):
        #Read current streak from a habit file.
        with open(file_path, "r") as f:
            content = f.readlines()
            return len(content)

    def failed_streak(self, file_path: str):
        #Reset the streak by clearing file
        with open(file_path, "w") as f:
            pass

    @staticmethod
    def new_streak(self, file_path: str):
        #Check if this is a new streak (empty file)
        with open(file_path, "r") as f:
            content = f.read()
        return not content

    def check_streak(self, _streak_path: str) -> int:
        #Get current streak count
        with open(_streak_path, "r") as f:
            lines = f.readlines()
            num_lines = len(lines)
            return int(num_lines)

    def create_habit_backend(self, new_habit_input: ctk.CTkEntry, habit_listbox):
        #Backend Logic for creating new habits
        new_habit = new_habit_input.get().strip()
        if not new_habit:
            messagebox.showerror("Error", "Habit name cannot be empty.")
            return

        habit = f"{new_habit}.txt"
        new_habit_file_path = os.path.join(self.habit_trainer_folder_path, habit)

        if os.path.exists(new_habit_file_path):
            messagebox.showinfo("Info", "Habit already exists.")
            return

        with open(new_habit_file_path, "w"):
            pass

        messagebox.showinfo("Success", f"New habit added: {new_habit}.")
        habit_listbox.insert(END, habit)
        new_habit_input.delete(0, END)
        print("Habit added successfully")

    def create_habit_frontend(self, frame, habit_add_button: ctk.CTkButton, habit_listbox):
        #Frontend UI for creating a new habit
        new_habit_heading = ctk.CTkLabel(frame,
                                         text="Enter a new habit: ", font=self.SUBTITLE_FONT)
        new_habit_heading.grid(row=5, column=0)

        new_habit_input = ctk.CTkEntry(frame, width=200)
        new_habit_input.grid(row=6, column=0)

        habit_add_button.destroy()

        new_habit_submit_button = ctk.CTkButton(
            frame,

            text="Submit",
            command=lambda: self.create_habit_backend(new_habit_input, habit_listbox))

        new_habit_submit_button.grid(row=7, column=0)
        saved_theme = self.load_theme_preference()
        self.apply_theme(frame, saved_theme)

    def delete_habit(self, habit_listbox):
        #Delete a habit by removing the file and updating the listbox
        habit_selection = habit_listbox.curselection()
        if not habit_selection:
            messagebox.showinfo("Info Dialog", "No habit selected.")
            return

        habit_index = habit_selection[0]
        habit_entry = habit_listbox.get(habit_index)
        # If items include extra info like "name: ..." keep only the name; otherwise this is the filename already.
        selected_habit = habit_entry.split(":", 1)[0].strip()
        target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
        file_path = os.path.join(self.habit_trainer_folder_path, target_file)

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
        except KeyError:
            pass

        messagebox.showinfo("Success", "Habit deleted.")

    def on_check(self, habit_listbox):
        #Check a habit to update the streak
        habit_selection = habit_listbox.curselection()
        if not habit_selection:
            messagebox.showinfo("Info Dialog", "No habit selected.")
            return

        habit_indices = habit_selection[0]
        habit_selected = habit_listbox.get(habit_indices)
        print(f"Selected habit: {habit_selected}")

        try:
            habit_listbox.itemconfig(habit_indices, bg="green")
        except KeyboardInterrupt:
            pass

        selected_habit = habit_selected.split(":", 1)[0]
        target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
        file_path = os.path.join(self.habit_trainer_folder_path, target_file)

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Habit not found.")
            return

        if self.new_streak(file_path, file_path):
            messagebox.showinfo("First Check", f"Congrats, this is your first check for {selected_habit}.")
            self.write_timestamp(file_path, datetime.now())
            return

        now = datetime.now()
        last = self.read_last_timestamp(file_path)

        if last is None:
            self.write_timestamp(file_path, now)
            return

        days_diff = (now.date() - last.date()).days

        if days_diff == 0:
            current_streak = self.read_streak(file_path)
            messagebox.showinfo("Info",
                                f"You've already completed this habit today. Current streak: {current_streak}")
            print(f"Already checked today. Streak = {current_streak}")

        elif days_diff == 1:
            streak = self.check_streak(file_path)
            streak += 1
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"Nice! Streak increased to {streak}.")
            print(f"Recorded today. Streak = {streak}")

        elif days_diff == 2:
            self.habit_revive_function(file_path)
            self.write_timestamp(file_path, now)

        elif days_diff > 2:
            streak = 1
            self.failed_streak(file_path)
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"You're late by {days_diff} day(s). Streak reset to {streak}")
            print(f"Streak reset = {streak}")

        else:
            streak = max(1, self.check_streak(file_path))
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"Time anomaly detected. Streak preserved at {streak}.")
            print(f"Anomaly detected. Streak = {streak}")

    # ----- Rename Functions -----#
    def rename_folder(self, input_old_folder, input_new_folder):
        """Rename a flashcard folder."""
        input_old_folder_name = input_old_folder.get()
        input_new_folder_name = input_new_folder.get()

        if input_old_folder_name in self.flashcard_files:
            # Start the renaming process
            os.rename(
                os.path.join(self.flashcard_folder_path, input_old_folder_name),
                os.path.join(self.flashcard_folder_path, input_new_folder_name)
            )
            messagebox.showinfo("Info Dialog",
                                f"Folder '{input_old_folder_name}' renamed to '{input_new_folder_name}'.")

        else:
            messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")

    def open_rename(self):
        """Create a rename folder interface."""
        heading_rename1 = ctk.CTkLabel(self.flashcard,
                                       text="Old Folder Name:",
                                       font=self.SUBTITLE_FONT)
        heading_rename1.grid(row=18,
                             column=0,
                             sticky="n")

        heading_rename2 = ctk.CTkLabel(self.flashcard,
                                       text="New Folder Name:",
                                       font=self.SUBTITLE_FONT)
        heading_rename2.grid(row=20,
                             column=0,
                             sticky="n")

        input_old_folder = ctk.CTkEntry(self.flashcard)
        input_new_folder = ctk.CTkEntry(self.flashcard)
        input_old_folder.grid(row=19,
                              column=0,
                              sticky="n")
        input_old_folder.focus_set()
        input_new_folder.grid(row=21,
                              column=0,
                              sticky="n")

        rename_submit = ctk.CTkButton(
            self.flashcard,
            text="Submit",

            command=lambda: [self.rename_folder(input_old_folder, input_new_folder), self.update_listbox(self.display)]
        )
        rename_submit.grid(row=22, column=0, sticky="n")

    # ----- Add Folder and File Feature -----#
    def create_file(self, folder_name, file_name):
        """Create a flashcard file in a folder."""
        file_path = os.path.join(self.flashcard_folder_path, folder_name, f"{file_name}.json")
        with open(file_path, "w") as f:
            json.dump({}, f)
        messagebox.showinfo("Info Dialog", f"File '{file_name}.json' created successfully.")

    def create_folder_and_file(self, folder_name, file_name):
        """Create both a folder and a flashcard file."""
        folder_path = os.path.join(self.flashcard_folder_path, folder_name)
        os.mkdir(folder_path)
        messagebox.showinfo("Info Dialog", f"Folder '{folder_name}' created successfully.")
        self.create_file(folder_name, file_name)

    def add_folder_and_file(self, command):
        """Handle folder and file creation."""
        command_request = command.get().lower()

        if command_request in ["y", "yes"]:
            folder_name_heading = ctk.CTkLabel(self.flashcard,
                                               text="Enter the name of the folder:", font=self.SUBTITLE_FONT)
            folder_name_heading.grid(row=21,
                                     column=1,
                                     sticky="n")

            folder_name = ctk.CTkEntry(self.flashcard)
            folder_name.grid(row=22,
                             column=1,
                             sticky="n")
            folder_name.focus_set()

            folder_name_submit = ctk.CTkButton(
                self.flashcard,
                text="Submit",
                command=lambda: self.yes_list_files(folder_name.get())
            )
            folder_name_submit.grid(row=23,
                                    column=1,
                                    sticky="n")

            file_name_heading = ctk.CTkLabel(self.flashcard,
                                             text="Enter the name for your flashcard file:", font=self.SUBTITLE_FONT)
            file_name_heading.grid(row=24,
                                   column=1,
                                   sticky="n",
                                   padx=10)

            file_name = ctk.CTkEntry(self.flashcard, width=200)
            file_name.grid(row=25,
                           column=1,
                           sticky="n")

            file_name_submit = ctk.CTkButton(
                self.flashcard,
                text="Submit",
                command=lambda: [self.create_folder_and_file(folder_name.get(),
                                                        file_name.get()),
                                 self.update_listbox(self.display)]
            )
            file_name_submit.grid(row=26,
                                  column=1,
                                  sticky="n")

        elif command_request in ["n", "no"]:
            folder_name_heading = ctk.CTkLabel(self.flashcard,
                                               text="Enter the name of the folder:", font=self.SUBTITLE_FONT)
            folder_name_heading.grid(row=21,
                                     column=1,
                                     sticky="n")

            folder_name = ctk.CTkEntry(self.flashcard)
            folder_name.grid(row=22,
                             column=1,
                             sticky="n")

            folder_name_submit = ctk.CTkButton(
                self.flashcard,
                text="Submit",

                command=lambda: self.no_list_files(folder_name.get())
            )
            folder_name_submit.grid(row=23,
                                    column=1,
                                    sticky="n")

            file_name_heading = ctk.CTkLabel(self.flashcard,
                                             text="Enter the name for your flashcard file:", font=self.SUBTITLE_FONT)
            file_name_heading.grid(row=24,
                                   column=1,
                                   sticky="n")

            file_name = ctk.CTkEntry(self.flashcard, width=200)
            file_name.grid(row=25,
                           column=1,
                           sticky="n")

            file_name_submit = ctk.CTkButton(
                self.flashcard,
                text="Submit",

                command=lambda: [self.create_folder_and_file(folder_name.get(),
                                                        file_name.get()),
                                 self.update_listbox(self.display)]
            )
            file_name_submit.grid(row=26,
                                  column=1,
                                  sticky="n")
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "Invalid input. Please enter 'y' or 'n'.")

        # Make sure that the theme is always loaded.
        saved_theme = self.load_theme_preference()
        self.apply_theme(self.flashcard, saved_theme)

    def open_add_folder_and_file(self, ):
        """Create a folder / file creation interface."""
        command_header = ctk.CTkLabel(self.flashcard,
                                      text="Do you want to create a new folder? (y/n):", font=self.SUBTITLE_FONT)
        command_header.grid(row=18,
                            column=1,
                            sticky="n")

        command = ctk.CTkEntry(self.flashcard)
        command.grid(row=19, column=1)

        command_submit = ctk.CTkButton(
            self.flashcard,
            text="Submit",

            command=lambda: self.add_folder_and_file(command)
        )
        command_submit.grid(row=20,
                            column=1,
                            sticky="n")

    # ----- Review Functions -----#
    def review_frontend(self, frame, display):
        """Create the review interface."""
        folder_name_heading = ctk.CTkLabel(frame,
                                           text="Enter the name of the folder:", font=self.SUBTITLE_FONT)
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

            command=lambda: self.list_folder_files(folder_name.get())
        )
        folder_name_submit.grid(row=3,
                                column=10,
                                sticky="n")

        file_name_heading = ctk.CTkLabel(frame,
                                         text="Enter the name for your flashcard file:", font=self.SUBTITLE_FONT)
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
            command=lambda: self.review_listbox_backend(folder_name, file_name, frame)
        )
        file_name_submit.grid(row=6,
                              column=10,
                              sticky="n")

    def list_folder_files(self, folder_name):
        """List files in the specified folder."""
        file_path = os.path.join(self.flashcard_folder_path, folder_name)
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Folder not found.")
            return

        files = os.listdir(file_path)
        messagebox.showinfo("Info", f"Files in folder: {files}")

    def review_listbox_backend(self, folder_name, file_name, frame):
        """Start the review quiz."""
        target_folder = folder_name.get()
        target_file = f"{file_name.get()}.json"
        final_file_path = os.path.join(self.flashcard_folder_path, target_folder, target_file)

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
                                        text=f"1. : {items[0][0]}", font=self.SUBTITLE_FONT)
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
            command=lambda: self.question_check(question_entry, question_heading)
        )
        question_submit.grid(row=10,
                             column=10,
                             sticky="n")

        saved_theme = self.load_theme_preference()
        self.apply_theme(self.flashcard, saved_theme)

        # Store state
        question_heading.items = items
        question_heading.idx = 0
        question_heading.correct = 0
        question_heading.wrong = 0
        question_heading.submit_btn = question_submit

    # ----- Check Functions -----#
    def question_check(self, question_entry, question_heading):
        """Check the answer and move to the next question."""
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
                self.use_powerup3(question_heading, correct)
                self.use_power_up2(question_heading, correct)
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
            if wrong > 5:
                messagebox.showinfo("Error", f"The right answer is {expected_answer}.")
            question_entry.delete(0, END)
            question_entry.focus_set()

    # ----- Power up Usage -----#
    def use_powerup3(self, question_heading, correct):
        items = getattr(question_heading, "items", [])
        if len(items) == 10:
            if correct == 10:
                self.use_combo_multiplier()
            else:
                pass
        elif len(items) < 10:
            if correct == len(items):
                self.use_combo_multiplier()
            else:
                pass
        elif len(items) > 10:
            if correct > 10:
                self.use_combo_multiplier()
            else:
                pass
        else:
            messagebox.showerror("Error", "No review state found.")

    def use_power_up2(self, question_heading, correct):
        items = getattr(question_heading, "items", [])
        if correct == len(items):
            self.use_double_coin_multiplier()

    # Use combo multiplier
    def use_combo_multiplier(self, ):
        current_coin = self.get_current_coins()

        new_coin = current_coin + 25
        with open(self.combined_path, "w") as q:
            q.write(str(new_coin) + "\n")
            self.update_listbox(self.display)
            messagebox.showinfo("Info Dialog", "You have used the combo multiplier! 25 Coins earned!")
            self.remove_combo_multiplier()

    # Use double coin multiplier
    def use_double_coin_multiplier(self, ):
        current_coin = self.get_current_coins()
        new_coin = current_coin + 50
        with open(self.combined_path, "w") as q:
            q.write(str(new_coin) + "\n")
            self.update_listbox(self.display)
            messagebox.showinfo("Info", "Double coin multiplier used! 50 Coins earned!")
            self.remove_double_coin(self.double_coins_function)

    # ----- Themes Functions -----#
    def save_theme_preference(self, theme_name):
        """Save the user's theme preference to a file."""
        with open(self.THEME_PREFERENCE_FILE, "w") as f:
            json.dump({"theme": theme_name}, f)

    def load_theme_preference(self, ):
        """Load the user's theme preference from the file."""
        if os.path.exists(self.THEME_PREFERENCE_FILE):
            with open(self.THEME_PREFERENCE_FILE, "r") as f:
                data = json.load(f)
                return data.get("theme", "blue")
        return "blue"

    def apply_theme(self, frame, theme_name):
        """Apply a theme to a frame by name."""
        if theme_name in self.THEMES:
            theme = self.THEMES[theme_name]
            self.apply_theme_to_widgets(
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

    def apply_theme_to_widgets(self, frame, frame_bg, ctrl_bg, fg=None, listbox_color=None,
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
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkButton):
                    try:
                        # If you want ZERO hover/press highlight:
                        w.configure(
                            fg_color=button_bg,
                            hover=False,  # <--- disable hover state
                            hover_color=button_bg,  # <--- same as normal bg (safety)
                            text_color=button_fg,
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkEntry):
                    try:
                        w.configure(
                            fg_color=entry_color,
                            text_color=fg,
                            border_color=button_bg
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkScrollbar):
                    try:
                        w.configure(
                            fg_color=ctrl_bg,
                            button_color=button_bg,
                            button_hover_color=button_hover
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                # Handle CTkOptionMenu explicitly
                elif isinstance(w, ctk.CTkOptionMenu):
                    try:
                        w.configure(
                            fg_color=ctrl_bg,
                            button_color=button_bg,
                            button_hover_color=button_hover,
                            text_color=fg,
                            font=self.SUBTITLE_FONT
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                # Handle regular tkinter widgets (like Listbox)
                elif widget_class in ('Label', 'Button', 'Entry', 'Listbox', 'Frame'):
                    if fg is not None:
                        try:
                            w.configure(fg=fg)
                        except (TclError, ValueError, AttributeError):
                            pass

                    if isinstance(w, Entry):
                        try:
                            w.configure(bg=entry_color)
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Listbox):
                        try:
                            w.configure(selectbackground=ctrl_bg)
                            w.configure(bg=listbox_color)
                            w.configure(selectforeground=fg or "black")
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Button):
                        try:
                            # Remove focus ring and active highlight on classic Tk buttons
                            w.configure(
                                bg=ctrl_bg,
                                activebackground=ctrl_bg,
                                activeforeground=fg if fg is not None else w.cget("fg"),
                                highlightthickness=0,
                                bd=0,
                                relief="flat",
                            )
                            # Avoid platform default "glow"/default-button styling and focus
                            try:
                                w.configure(default="normal", takefocus=0)
                            except (TclError, ValueError, AttributeError):
                                pass
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Label):
                        try:
                            w.configure(bg=ctrl_bg)
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Frame):
                        try:
                            w.configure(bg=frame_bg)
                        except (TclError, ValueError, AttributeError):
                            pass

                stack.append(w)

    @staticmethod
    def neutralize_button_highlight(root_widget):
        """
        Remove hover/active/focus highlights from CTkButton and tkinter.Button
        across the entire widget tree. Call after building the UI and theming.
        """
        # Global Tk defaults: remove focus ring and active highlight for classic Buttons
        try:
            root_widget.option_add("*Button.highlightThickness", 0)
            root_widget.option_add("*highlightThickness", 0)
            root_widget.option_add(
                "*Button.activeBackground",
                root_widget.cget("bg") if hasattr(root_widget, "cget") else "SystemButtonFace"
            )
            root_widget.option_add("*Button.activeForeground", "SystemButtonText")
        except KeyError:
            pass

        stack = [root_widget]
        while stack:
            parent = stack.pop()
            for w in parent.winfo_children():
                try:
                    # ----- CustomTkinter CTkButton -----
                    if isinstance(w, ctk.CTkButton):
                        try:
                            w.configure(
                                hover=False,
                                hover_color=w.cget("fg_color"),
                            )
                        except KeyError:
                            pass
                        try:
                            w.configure(border_width=w.cget("border_width"))
                        except KeyError:
                            pass

                    # ----- Classic tkinter Button -----
                    elif w.winfo_class() == "Button":
                        try:
                            normal_bg = w.cget("bg")
                            normal_fg = w.cget("fg")
                            w.configure(
                                activebackground=normal_bg,
                                activeforeground=normal_fg,
                                highlightthickness=0,
                                bd=0,
                                relief="flat",
                            )
                            try:
                                w.configure(default="normal", takefocus=0)
                            except KeyError:
                                pass
                        except KeyError:
                            pass
                except KeyError:
                    pass
                stack.append(w)

    def create_theme_buttons(self, parent, *targets):
        # Create theme buttons inside a frame.

        theme_frame = ctk.CTkFrame(parent)

        def change_theme(theme_name):
            self.save_theme_preference(theme_name)
            # Ensure the settings parent is included so the Settings tab updates immediately
            tgt_list = list(targets)
            if parent not in tgt_list:
                tgt_list.insert(0, parent)

            for t in tgt_list:
                if t is None:
                    continue
                try:
                    self.apply_theme(t, theme_name)
                except KeyError:
                    # ignore targets that can't be themed right now
                    pass

            # also set CustomTkinter appearance mode mapping (best-effort)
            try:
                mode = self.CTK_APPEARANCE_MODES.get(theme_name, "light")
                ctk.set_appearance_mode(mode)
            except KeyError:
                pass

            # Re-neutralize hover/active/focus highlights after theme change
            for t in tgt_list:
                try:
                    self.neutralize_button_highlight(t)
                except KeyError:
                    pass
            try:
                parent.update_idletasks()
            except KeyError:
                pass

        r = 0
        c = 0
        i = 0

        # Create theme buttons and position them using provided r/c params
        pink_btn = ctk.CTkButton(theme_frame,
                                 text="Pink Theme",

                                 command=lambda: change_theme("pink"),
                                 width=100)
        pink_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        blue_btn = ctk.CTkButton(theme_frame,
                                 text="Blue Theme",

                                 command=lambda: change_theme("blue"),
                                 width=100)
        blue_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        white_btn = ctk.CTkButton(theme_frame,
                                  text="White Theme",

                                  command=lambda: change_theme("white"),
                                  width=100)
        white_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        green_btn = ctk.CTkButton(theme_frame,
                                  text="Green Theme",

                                  command=lambda: change_theme("green"),
                                  width=100)
        green_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        purple_btn = ctk.CTkButton(theme_frame,
                                   text="Purple Theme",
                                   command=lambda: change_theme("purple"),
                                   width=100)
        purple_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        yellow_btn = ctk.CTkButton(theme_frame,
                                   text="Yellow Theme",

                                   command=lambda: change_theme("yellow"),
                                   width=100)
        yellow_btn.grid(row=r + i, column=c, padx=5, pady=5, sticky="sew")

        i += 1

        return theme_frame

    # ----- UI Functions -----#
    def update_listbox(self, display):
        """Refresh the listbox."""
        if display is None:
            return

        # Clear the whole listbox:
        display.delete(0, END)

        # Re-scan and input:
        if os.path.exists(self.flashcard_folder_path):
            folders = [f for f in os.listdir(self. flashcard_folder_path)
                       if os.path.isdir(os.path.join(self.flashcard_folder_path, f))]
            for folder in sorted(folders):
                display.insert(END, folder)

    # ----- Create Dropdown ----- #
    def file_dropdown(self, probo):
        def on_dropdown_change(choice):
            print(f"Selected action: {choice}")
            if choice == "Flashcard":
                probo.set("Flashcards")
            elif choice == "Shop":
                probo.set("Shop")
            elif choice == "Timer":
                probo.set("Timer")
            elif choice == "Home":
                probo.set("Home")
            elif choice == "Settings":
                probo.set("Settings")
            else:
                probo.set("Home")
            # Add more logic for other features here

        values = ["Home", "Flashcard", "Shop", "Timer", "Settings"]

        # Use CTkOptionMenu for a modern look that matches your theme
        home_dropdown = ctk.CTkOptionMenu(
            self.home,
            values=values,
            command=on_dropdown_change,
        )
        home_dropdown.grid(row=0, column=0, sticky="we")

        flashcard_dropdown = ctk.CTkOptionMenu(
            self.flashcard,
            values=values,
            command=on_dropdown_change,
        )
        flashcard_dropdown.grid(row=0, column=0, sticky="we")

        shop_dropdown = ctk.CTkOptionMenu(
            self.shop,
            values=values,
            command=on_dropdown_change,
        )
        shop_dropdown.grid(row=0, column=0, sticky="wn")

        timer_dropdown = ctk.CTkOptionMenu(
            self.timer,
            values=values,
            command=on_dropdown_change,
        )
        timer_dropdown.grid(row=0, column=0, sticky="wn")

        setting_dropdown = ctk.CTkOptionMenu(
            self.setting,
            values=values,
            command=on_dropdown_change,
        )
        setting_dropdown.grid(row=0, column=0, sticky="wn")

    # ----- Main UI -----#
    def main(self):
        """Main application entry point."""

        # Initialize the application
        self.initialize_currency()
        self.initialize_inventory()

        # Set CustomTkinter appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("Flashcard Feature")
        root.geometry("1800x1080")

        window_width = 1200
        window_height = 800
        self.center_window(root, window_width, window_height)

        # Create tabview instead of notebook
        probo = ctk.CTkTabview(root)
        # Add tabs first, then use a single geometry manager (pack) exactly once.
        probo.add("Home")
        probo.add("Flashcards")
        probo.add("Shop")
        probo.add("Timer")
        probo.add("Settings")
        probo.pack(fill="both", expand=1)

        # Frame 2 - Home (FIRST tab)
        self.home = probo.tab("Home")

        # Frame 1 - Flashcards (SECOND tab)
        self.flashcard = probo.tab("Flashcards")

        # Frame 3 - Shop (THIRD tab)
        self.shop = probo.tab("Shop")

        self.timer = probo.tab("Timer")
        # Settings tab (for centralized theme controls)
        self.setting = probo.tab("Settings")
        # select_powerup moved later so shop widgets and theme frames are created first

        # ===== FRAME 1 UI (FLASHCARDS PAGE) =====

        # Rename section
        rename_header = ctk.CTkLabel(self.flashcard,
                                     text="Rename",
                                     font=self.TITLE_FONT)
        rename_header.grid(row=17,
                           column=0,
                           sticky="nsew",
                           pady=5)
        self.open_rename()

        # Add folder section
        add_folder_header = ctk.CTkLabel(self.flashcard,
                                         text="     Add Folder     ",
                                         font=self.TITLE_FONT)
        add_folder_header.grid(row=17,
                               column=1,
                               sticky="n",
                               rowspan=2,
                               pady=5,
                               padx=5)
        self.open_add_folder_and_file()

        # Edit section
        edit_title = ctk.CTkLabel(self.flashcard,
                                  text="     Edit     ",
                                  font=self.TITLE_FONT)
        edit_title.grid(row=0,
                        column=3,
                        sticky="s",
                        columnspan=3)

        # ----- Home Page ----- #

        # Review section (same idea; call review_frontend later)
        review_heading = ctk.CTkLabel(self.flashcard,
                                      text="     Review     ",
                                      font=self.TITLE_FONT)
        review_heading.grid(row=0,
                            column=10,
                            sticky="n",
                            columnspan=3)

        list_frame = ctk.CTkFrame(self.home)
        list_frame.grid(row=1,
                        column=0,
                        columnspan=3,
                        rowspan=15,
                        sticky="nsew")

        welcome_frame = ctk.CTkFrame(self.home)
        welcome_frame.grid(row=1, column=3, rowspan=15, sticky="nsew")

        welcome_heading = ctk.CTkLabel(welcome_frame, text="Welcome to Pro Bo!", font=self.TITLE_FONT)
        welcome_heading.grid(row=0, column=1, sticky="nsew", padx=5, columnspan=2)

        # Short welcome text below the toolbar (same column)
        welcome_text = ctk.CTkLabel(welcome_frame,
                                    text="Productivity Booster or know as Pro bo is a study app that helps you study better.\n"
                                         "Pro Bo is aimed for students but it is useful to all people.\n\n"
                                         "Version 1 only contains Flashcard and Shop with boosters, but stay tuned for version 2 with more insane updates. \n"
                                         "If you have any questions or suggestions or maybe you find some problems while using the app, please contact me at. \n"
                                         "mingl_2028@concordian.org",
                                    font=self.REGULAR_FONT)
        welcome_text.grid(row=1, column=1, sticky="nesw", padx=5, columnspan=2)

        available_habit_label = ctk.CTkLabel(list_frame, text="Your daily habits", font=self.TITLE_FONT)
        available_habit_label.grid(row=0, column=0, sticky="nsew", columnspan=3)

        habit_listbox = Listbox(list_frame,
                                width=25,
                                height=15,
                                font=self.REGULAR_FONT)
        for i in self.habit_trainer_files:
            habit_listbox.insert(END, i)
        habit_listbox.grid(row=1,
                           column=0,
                           columnspan=2,
                           sticky="nsw",
                           padx=5)

        # scrollbar immediately to the right of the listbox and stretched vertically
        habit_scroll = ctk.CTkScrollbar(list_frame,
                                        orientation="vertical",
                                        command=habit_listbox.yview)
        habit_scroll.grid(row=1,
                          column=2,
                          sticky="ns")
        habit_listbox.config(yscrollcommand=habit_scroll.set)

        heading1 = ctk.CTkLabel(list_frame,
                                text="Available Flashcards",
                                font=self.TITLE_FONT)
        heading1.grid(row=2,
                      column=0,
                      columnspan=3)

        display = Listbox(list_frame,
                          width=25,
                          height=15,
                          font=self.REGULAR_FONT)
        if os.path.exists(self.flashcard_folder_path):
            if os.path.getsize(self.flashcard_folder_path) == 0:
                display.insert(END, "No flashcards yet!")
            else:
                for file in self.flashcard_files:
                    display.insert(END, file)

        display.grid(row=3,
                     column=0,
                     sticky="nsw",
                     padx=5,
                     columnspan=2)

        scrollbar = ctk.CTkScrollbar(list_frame,
                                     orientation="vertical",
                                     command=display.yview)
        scrollbar.grid(row=3,
                       column=2,
                       rowspan=10,
                       sticky="ns",
                       pady=5)

        display.config(yscrollcommand=scrollbar.set)

        # Now that `display` exists, initialize the Flashcards edit & review UIs
        self.edit_flashcard_frontend(display)
        self.review_frontend(self.flashcard, display)

        # Shop title
        shop_title = ctk.CTkLabel(self.shop,
                                  text="Welcome to the Shop",
                                  font=self.TITLE_FONT)
        shop_title.grid(row=2,
                        column=0,
                        columnspan=3,
                        pady=10)

        # Shop description
        shop_description = ctk.CTkLabel(self.shop,
                                        text="Use coins to buy power-ups that help you with your habits.",
                                        font=self.REGULAR_FONT)
        shop_description.grid(row=4,
                              column=0,
                              columnspan=3,
                              pady=10)

        # Theme buttons removed from Shop page — moved to Settings tab
        root.update_idletasks()

        # Now initialize shop widgets that rely on the frames existing
        self.select_powerup(self.shop)

        # ----- Timer Tab -----#
        time_panel = ctk.CTkFrame(self.timer, width=300, height=400)
        time_panel.grid(row=2, column=0, sticky="nsew")
        time_panel.grid_propagate(False)

        time_panel.grid_columnconfigure(0, weight=1)
        time_panel.grid_columnconfigure(1, weight=1)

        input_label = ctk.CTkLabel(time_panel, text="Input minutes and seconds", font=self.SUBTITLE_FONT, width=300)
        input_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        min_label = ctk.CTkLabel(time_panel, text="Minutes:", font=self.SUBTITLE_FONT, width=300)
        min_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        min_entry = ctk.CTkEntry(time_panel, font=self.SUBTITLE_FONT, width=300)
        min_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        sec_label = ctk.CTkLabel(time_panel, text="Seconds:", font=self.SUBTITLE_FONT, width=300)
        sec_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        sec_entry = ctk.CTkEntry(time_panel, font=self.SUBTITLE_FONT, width=300)
        sec_entry.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        time_label = ctk.CTkLabel(time_panel, text="00:00:00", font=self.SUBTITLE_FONT, width=300)
        time_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="we")

        start_btn = ctk.CTkButton(
            time_panel,
            text="Start",
            command=lambda: self.start_timer(min_entry, sec_entry, time_label, start_btn, stop_btn),
            width=150
        )
        start_btn.grid(row=8, column=0, padx=(10, 5), pady=(5, 10), sticky="we")

        stop_btn = ctk.CTkButton(
            time_panel,
            text="Stop",
            command=lambda: self.stop_timer(min_entry, sec_entry, time_label, start_btn, stop_btn),
            width=150
        )
        stop_btn.grid(row=8, column=1, padx=(5, 10), pady=(5, 10), sticky="we")

        # allow entries/labels to stretch horizontally within the Timer tab
        self.timer.grid_columnconfigure(0, weight=1)
        self.timer.grid_columnconfigure(1, weight=1)
        theme_frame_settings = self.create_theme_buttons(self.setting, self.flashcard, self.home, self.shop, self.timer)
        theme_frame_settings.grid(row=2, column=0, padx=20, pady=20,
                                  sticky="nwes")

        theme_label = ctk.CTkLabel(self.setting, text="Theme", font=self.REGULAR_FONT)
        theme_label.grid(row=1, column=0, sticky="nwe", padx=20, pady=20)

        # ensure Settings tab rows/columns behave
        self.setting.grid_columnconfigure(1, weight=1)
        self.setting.grid_rowconfigure(0, weight=0)

        self.file_dropdown(self)

        # Load and apply saved theme
        saved_theme = self.load_theme_preference()
        self.apply_theme(self.flashcard, saved_theme)
        self.apply_theme(self.home, saved_theme)
        self.apply_theme(self.shop, saved_theme)
        self.apply_theme(self.setting, saved_theme)
        self.apply_theme(self.timer, saved_theme)
        # ensure layout is up-to-date so theme buttons render immediately
        root.update_idletasks()
        # Apply final pass to kill any button highlight/hover/focus effects
        self.neutralize_button_highlight(root)
        root.mainloop()

if __name__ == "__main__":
    app = Probo()
    app.main()
