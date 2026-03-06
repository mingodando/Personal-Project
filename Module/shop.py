import os
import json
from tkinter import StringVar
from tkinter import messagebox
import customtkinter as ctk

from theme import Theme


class Shop(Theme):
    def __init__(self):
        super().__init__()
        # FIX: only declare UI state variables here, NEVER method names
        self.root = None
        self.shop_window = None
        self.coin_label = None
        self.display = None

    # ===== COIN MANAGEMENT FUNCTIONS ===== #
    def initialize_currency(self):
        """Create currency file if it doesn't exist."""
        if not os.path.exists(self.combined_path):
            with open(self.combined_path, "w") as f:
                f.write("100\n")

    def get_current_coins(self):
        """Read the current coin amount from the file."""
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
        """Update the coin display label."""
        if self.coin_label:
            current_coins = self.get_current_coins()
            self.coin_label.configure(text=f"Current coins: {current_coins}")

    # ===== INVENTORY MANAGEMENT FUNCTIONS ===== #
    def initialize_inventory(self):
        """Create the inventory file if it doesn't exist."""
        if not os.path.exists(self.inventory_path):
            initial_inventory = {
                "Habit Revive": 0,
                "Double Coins": 0,
                "Combo Multiplier": 0
            }
            with open(self.inventory_path, "w") as f:
                json.dump(initial_inventory, f, indent=4)

    def get_inventory(self):
        """Read and return the current inventory."""
        self.initialize_inventory()
        with open(self.inventory_path, "r") as f:
            return json.load(f)

    def add_to_inventory(self, item_key, quantity=1):
        """Add items to inventory."""
        inventory = self.get_inventory()
        inventory[item_key] = inventory.get(item_key, 0) + quantity
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)

    def remove_from_inventory(self, item_key, quantity=1):
        """Remove items from the inventory (returns True if successful)."""
        inventory = self.get_inventory()
        if inventory.get(item_key, 0) >= quantity:
            inventory[item_key] -= quantity
            with open(self.inventory_path, "w") as f:
                json.dump(inventory, f, indent=4)
            return True
        return False

    # ===== BUY POWERUP FUNCTIONS ===== #
    def buy_powerup1(self):
        """Buy Habit Revive powerup (50 coins)."""
        current_coin = self.get_current_coins()
        if current_coin < 50:
            messagebox.showerror("Insufficient Coins", "You don't have enough coins to buy this powerup.")
            return
        new_coin = current_coin - 50
        with open(self.combined_path, 'w') as d:
            d.write(str(new_coin) + "\n")
        self.add_to_inventory("Habit Revive", 1)
        messagebox.showinfo("Powerup Purchased", "You have successfully purchased Habit Revive!")
        self.update_coin_display()

    def buy_powerup2(self):
        """Buy Double Coins powerup (50 coins)."""
        current_coin = self.get_current_coins()
        if current_coin < 50:
            messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
            return
        new_coin = current_coin - 50
        with open(self.combined_path, "w") as d:
            d.write(str(new_coin) + "\n")
        self.add_to_inventory("Double Coins", 1)
        messagebox.showinfo("Success", "You bought 1 Double Coin Potion!\nCheck your inventory to use it.")
        self.update_coin_display()

    def buy_powerup3(self):
        """Buy Combo Multiplier powerup (15 coins)."""
        current_coin = self.get_current_coins()
        if current_coin < 15:
            messagebox.showwarning("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 15.")
            return
        new_coin = current_coin - 15
        with open(self.combined_path, "w") as d:
            d.write(str(new_coin) + "\n")
        self.add_to_inventory("Combo Multiplier", 1)
        messagebox.showinfo("Success", "You bought 1 Combo Multiplier!\nCheck your inventory to use it.")
        self.update_coin_display()

    # ===== INVENTORY UI FUNCTIONS ===== #
    def habit_revive_function(self, file_path):
        """Use or prompt to buy Habit Revive."""
        inventory = self.get_inventory()
        if inventory.get("Habit Revive", 0) >= 1:
            self.remove_from_inventory("Habit Revive", 1)
            messagebox.showinfo("Success", "Habit Revive used! Your streak is safe.")
        else:
            response = messagebox.askyesno("Buy Powerup?", "Do you want to buy more powerups?")
            if response:
                self.open_inventory()
            else:
                self.failed_streak(file_path)

    def double_coins_function(self, file_path):
        """Use or prompt to buy Double Coins."""
        inventory = self.get_inventory()
        if inventory.get("Double Coins", 0) >= 1:
            self.remove_from_inventory("Double Coins", 1)
            messagebox.showinfo("Success", "Double Coins powerup used! Double reward for next review session")
        else:
            response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
            if not response:
                self.failed_streak(file_path)

    def remove_habit_revive(self, habit_revive_function):
        """Use a Habit Revive from inventory."""
        yes_no = messagebox.askyesno("Use Powerup", "If you use this powerup, your streak will stay alive.")
        if yes_no:
            if callable(habit_revive_function):
                habit_revive_function()
            if self.remove_from_inventory("Habit Revive", 1):
                messagebox.showinfo("Used!", "Habit Revive used successfully!")
            else:
                messagebox.showwarning("Not Available", "You don't have any Habit Revives!")
                messagebox.showinfo("Buy More", "Go to the shop to buy more and come back")

    def remove_double_coin(self, double_coin_function):
        """Use a Double Coins potion from inventory."""
        yes_no = messagebox.askyesno(
            "Use Powerup",
            "If you use this powerup, you will double the coins for next review session."
        )
        if yes_no:
            if callable(double_coin_function):
                double_coin_function()
            if self.remove_from_inventory("Double Coins", 1):
                messagebox.showinfo("Used!", "Double Coins Powerup used successfully!")
                self.open_inventory()
            else:
                messagebox.showwarning("Not Available", "You don't have any Double Coins!")

    def remove_combo_multiplier(self, combo_multiplier_function=None):
        """Use a Combo Multiplier from inventory."""
        yes_no = messagebox.askyesno(
            "Use Powerup",
            "If you use this powerup, you will get 30 coins immediately when getting 10 correct answers in a row during review."
        )
        if yes_no:
            if callable(combo_multiplier_function):
                combo_multiplier_function()
            if self.remove_from_inventory("Combo Multiplier", 1):
                messagebox.showinfo("Used!", "Combo Multiplier used successfully!")
                self.open_inventory()
            else:
                messagebox.showwarning("Not Available", "You don't have any Combo Multipliers!")

    def open_inventory(self):
        """Open the inventory window."""
        inventory_window = ctk.CTkToplevel(self.root)
        inventory_window.title("Inventory")
        inventory_window.geometry("400x330")

        inventory = self.get_inventory()

        habit_var  = StringVar(value=f"Habit Revive: {inventory['Habit Revive']}")
        double_var = StringVar(value=f"Double Coins: {inventory['Double Coins']}")
        combo_var  = StringVar(value=f"Combo Multiplier: {inventory['Combo Multiplier']}")

        def refresh_labels():
            inv = self.get_inventory()
            habit_var.set(f"Habit Revive: {inv['Habit Revive']}")
            double_var.set(f"Double Coins: {inv['Double Coins']}")
            combo_var.set(f"Combo Multiplier: {inv['Combo Multiplier']}")

        def poll():
            if inventory_window.winfo_exists():
                refresh_labels()
                inventory_window.after(1000, poll)

        ctk.CTkLabel(inventory_window, text="Your Power-Ups", font=self.SUBTITLE_FONT).grid(
            row=0, column=0, columnspan=2, pady=10, padx=10
        )
        ctk.CTkLabel(inventory_window, textvariable=habit_var, width=200, anchor="w", font=self.REGULAR_FONT).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(inventory_window, text="Use", width=80,
                      command=lambda: [self.remove_habit_revive(None), refresh_labels()]).grid(
            row=1, column=1, padx=10, pady=5
        )
        ctk.CTkLabel(inventory_window, textvariable=double_var, width=200, anchor="w", font=self.REGULAR_FONT).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(inventory_window, text="Use", width=80,
                      command=lambda: [self.remove_double_coin(None), refresh_labels()]).grid(
            row=2, column=1, padx=10, pady=5
        )
        ctk.CTkLabel(inventory_window, textvariable=combo_var, width=200, anchor="w", font=self.REGULAR_FONT).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(inventory_window, text="Use", width=80,
                      command=lambda: [self.remove_combo_multiplier(None), refresh_labels()]).grid(
            row=3, column=1, padx=10, pady=5
        )
        ctk.CTkButton(inventory_window, text="Close", command=inventory_window.destroy).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        poll()
        saved_theme = self.load_theme_preference()
        self.apply_theme(inventory_window, saved_theme)
        self.neutralize_button_highlight(inventory_window)
        inventory_window.tkraise()
        inventory_window.attributes("-topmost", True)
        inventory_window.focus_force()

    def select_powerup(self):
        """Open the shop window."""
        self.shop_window = ctk.CTkToplevel(self.root)
        self.shop_window.title("Shop")
        self.shop_window.geometry("800x310")
        self.shop_window.attributes("-topmost", True)
        self.shop_window.focus_force()

        coin_label = ctk.CTkLabel(
            self.shop_window,
            text=f"Current Coins: {self.get_current_coins()}",
            font=self.REGULAR_FONT
        )
        coin_label.grid(row=3, column=0, columnspan=2, pady=10)

        inventory_btn = ctk.CTkButton(
            self.shop_window, text="Open Inventory", command=lambda: self.open_inventory()
        )
        inventory_btn.grid(row=5, column=0, columnspan=2, pady=5)

        power_up = ctk.CTkLabel(
            self.shop_window,
            text=f"Here are the available power-ups:\n{self.POWER_UPS}",
            font=self.REGULAR_FONT
        )
        power_up.grid(row=6, rowspan=3, column=0, columnspan=2, pady=10)

        power_up1 = ctk.CTkLabel(self.shop_window, text="Habit Revive (50 coins)", anchor="w", font=self.SUBTITLE_FONT)
        power_up1.grid(row=9, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup1, text="Buy", width=80).grid(row=9, column=1, pady=5)

        power_up2 = ctk.CTkLabel(self.shop_window, text="Double Coins (50 coins)", anchor="w", font=self.SUBTITLE_FONT)
        power_up2.grid(row=10, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup2, text="Buy", width=80).grid(row=10, column=1, pady=5)

        power_up3 = ctk.CTkLabel(self.shop_window, text="Combo Multiplier (15 coins)", anchor="w", font=self.SUBTITLE_FONT)
        power_up3.grid(row=11, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup3, text="Buy", width=80).grid(row=11, column=1, pady=5)

    # ----- Power-up Usage ----- #
    def use_powerup3(self, question_heading, correct):
        """Trigger Combo Multiplier reward at end of review."""
        items = getattr(question_heading, "items", [])
        if len(items) <= 10:
            if correct == len(items):
                self.use_combo_multiplier()
        elif len(items) > 10:
            if correct > 10:
                self.use_combo_multiplier()

    def use_power_up2(self, question_heading, correct):
        """Trigger Double Coin reward at end of review."""
        items = getattr(question_heading, "items", [])
        if correct == len(items):
            self.use_double_coin_multiplier()

    def use_combo_multiplier(self):
        """Award 25 coins when Combo Multiplier activates."""
        current_coin = self.get_current_coins()
        new_coin = current_coin + 25
        with open(self.combined_path, "w") as q:
            q.write(str(new_coin) + "\n")
        messagebox.showinfo("Info Dialog", "You have used the combo multiplier! 25 Coins earned!")
        self.remove_combo_multiplier()

    def use_double_coin_multiplier(self):
        """Award 50 coins when Double Coin Multiplier activates."""
        current_coin = self.get_current_coins()
        new_coin = current_coin + 50
        with open(self.combined_path, "w") as q:
            q.write(str(new_coin) + "\n")
        messagebox.showinfo("Info", "Double coin multiplier used! 50 Coins earned!")
        self.remove_double_coin(self.double_coins_function)

    # ----- Stub overridden by Flashcard ----- #
    def update_listbox(self, display):
        pass

    # ----- Stub overridden by Habit ----- #
    def failed_streak(self, file_path):
        pass
