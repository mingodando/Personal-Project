import os
import json
from tkinter import StringVar
from tkinter import messagebox
import customtkinter as ctk

from theme import Theme

class Shop(Theme):
    def __init__(self):
        super().__init__()
        self.root = None
        self.shop_window = None
        self.coin_label = None
        self.display = None

    # ===== COIN MANAGEMENT ===== #
    def initialize_currency(self):
        """Create the currency file if it doesn't exist."""
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
                return int(lines[-1].strip())
        except (FileNotFoundError, ValueError):
            return 0

    def update_coin_display(self):
        """Update the coin display label."""
        if self.coin_label:
            self.coin_label.configure(text=f"Current coins: {self.get_current_coins()}")

    def _save_coins(self, amount):
        """Write a coin amount to the currency file."""
        with open(self.combined_path, "w") as f:
            f.write(str(amount) + "\n")

    # ===== INVENTORY MANAGEMENT ===== #
    def initialize_inventory(self):
        """Create the inventory file if it doesn't exist."""
        if not os.path.exists(self.inventory_path):
            with open(self.inventory_path, "w") as f:
                json.dump({"Habit Revive": 0, "Double Coins": 0, "Combo Multiplier": 0}, f, indent=4)

    def get_inventory(self):
        """Read and return the current inventory."""
        self.initialize_inventory()
        with open(self.inventory_path, "r") as f:
            return json.load(f)

    def add_to_inventory(self, item_key, quantity=1):
        """Add items to the inventory."""
        inventory = self.get_inventory()
        inventory[item_key] = inventory.get(item_key, 0) + quantity
        with open(self.inventory_path, "w") as f:
            json.dump(inventory, f, indent=4)

    def remove_from_inventory(self, item_key, quantity=1):
        """Remove items from inventory. Returns True if successful."""
        inventory = self.get_inventory()
        if inventory.get(item_key, 0) >= quantity:
            inventory[item_key] -= quantity
            with open(self.inventory_path, "w") as f:
                json.dump(inventory, f, indent=4)
            return True
        return False

    # ===== BUY POWERUPS ===== #
    def buy_powerup1(self):
        """Buy Habit Revive (50 coins). Returns True if successful."""
        current_coin = self.get_current_coins()
        if current_coin < 50:
            messagebox.showerror("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
            return False
        self._save_coins(current_coin - 50)
        self.add_to_inventory("Habit Revive", 1)
        messagebox.showinfo("Purchased!", "You bought 1 Habit Revive.")
        self.update_coin_display()
        return True

    def buy_powerup2(self):
        """Buy Double Coins (50 coins). Returns True if successful."""
        current_coin = self.get_current_coins()
        if current_coin < 50:
            messagebox.showerror("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 50.")
            return False
        self._save_coins(current_coin - 50)
        self.add_to_inventory("Double Coins", 1)
        messagebox.showinfo("Purchased!", "You bought 1 Double Coins potion.")
        self.update_coin_display()
        return True

    def buy_powerup3(self):
        """Buy Combo Multiplier (15 coins). Returns True if successful."""
        current_coin = self.get_current_coins()
        if current_coin < 15:
            messagebox.showerror("Insufficient Coins", f"Not enough coins! You have {current_coin}, need 15.")
            return False
        self._save_coins(current_coin - 15)
        self.add_to_inventory("Combo Multiplier", 1)
        messagebox.showinfo("Purchased!", "You bought 1 Combo Multiplier.")
        self.update_coin_display()
        return True

    # ===== USE POWERUPS ===== #
    def use_habit_revive(self, file_path):
        """Use a Habit Revive to save a broken streak, or offer to buy one."""
        if self.remove_from_inventory("Habit Revive", 1):
            messagebox.showinfo("Habit Revive Used!", "Your streak is safe!")
        else:
            response = messagebox.askyesno("No Habit Revive", "You don't have a Habit Revive. Buy one now?")
            if response:
                if self.buy_powerup1():
                    if self.remove_from_inventory("Habit Revive", 1):
                        messagebox.showinfo("Habit Revive Used!", "Your streak is safe!")
            else:
                self.failed_streak(file_path)

    def use_double_coins(self, correct=None, wrong=None):
        """Use Double Coins. If correct/wrong provided, award score-based coins. Otherwise flat 50."""
        if not self.remove_from_inventory("Double Coins", 1):
            messagebox.showwarning("No Double Coins", "You don't have any Double Coins potions.")
            return
        if correct is not None and wrong is not None:
            bonus = max(0, correct - wrong) * 5
            messagebox.showinfo("Double Coins Used!",
                                f"You earned {bonus} bonus coins! ({correct} correct - {wrong} wrong) x5")
        else:
            bonus = 50
            messagebox.showinfo("Double Coins Used!", "You earned 50 bonus coins!")
        self._save_coins(self.get_current_coins() + bonus)
        self.update_coin_display()

    def use_combo_multiplier(self):
        """Use a Combo Multiplier to earn 25 bonus coins."""
        if not self.remove_from_inventory("Combo Multiplier", 1):
            messagebox.showwarning("No Combo Multiplier", "You don't have any Combo Multipliers.")
            return
        self._save_coins(self.get_current_coins() + 25)
        messagebox.showinfo("Combo Multiplier Used!", "25 bonus coins earned!")
        self.update_coin_display()

    # ===== INVENTORY UI ===== #
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
                      command=lambda: [self.use_habit_revive(None), refresh_labels()]).grid(
            row=1, column=1, padx=10, pady=5
        )
        ctk.CTkLabel(inventory_window, textvariable=double_var, width=200, anchor="w", font=self.REGULAR_FONT).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(inventory_window, text="Use", width=80,
                      command=lambda: [self.use_double_coins(), refresh_labels()]).grid(
            row=2, column=1, padx=10, pady=5
        )
        ctk.CTkLabel(inventory_window, textvariable=combo_var, width=200, anchor="w", font=self.REGULAR_FONT).grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        ctk.CTkButton(inventory_window, text="Use", width=80,
                      command=lambda: [self.use_combo_multiplier(), refresh_labels()]).grid(
            row=3, column=1, padx=10, pady=5
        )
        ctk.CTkButton(inventory_window, text="Close", command=inventory_window.destroy).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        poll()
        self.apply_themes_to_all(inventory_window)
        inventory_window.tkraise()
        inventory_window.attributes("-topmost", True)
        inventory_window.focus_force()

    def select_powerup(self):
        """Open the shop window."""
        self.shop_window = ctk.CTkToplevel(self.root)
        self.shop_window.title("Shop")
        self.shop_window.geometry("800x320")
        self.shop_window.attributes("-topmost", True)
        self.shop_window.focus_force()

        self.coin_label = ctk.CTkLabel(
            self.shop_window,
            text=f"Current Coins: {self.get_current_coins()}",
            font=self.REGULAR_FONT
        )
        self.coin_label.grid(row=0, column=0, columnspan=2, pady=10)

        inventory_btn = ctk.CTkButton(
            self.shop_window, text="Open Inventory", command=self.open_inventory
        )
        inventory_btn.grid(row=1, column=0, columnspan=2, pady=5)

        power_up = ctk.CTkLabel(
            self.shop_window,
            text=f"Available power-ups:\n{self.POWER_UPS}",
            font=self.REGULAR_FONT
        )
        power_up.grid(row=2, rowspan=3, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self.shop_window, text="Habit Revive (50 coins)", anchor="w", font=self.SUBTITLE_FONT).grid(
            row=5, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup1, text="Buy", width=80).grid(row=5, column=1, pady=5)

        ctk.CTkLabel(self.shop_window, text="Double Coins (50 coins)", anchor="w", font=self.SUBTITLE_FONT).grid(
            row=6, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup2, text="Buy", width=80).grid(row=6, column=1, pady=5)

        ctk.CTkLabel(self.shop_window, text="Combo Multiplier (15 coins)", anchor="w", font=self.SUBTITLE_FONT).grid(
            row=7, column=0, pady=5, sticky="w", padx=10)
        ctk.CTkButton(self.shop_window, command=self.buy_powerup3, text="Buy", width=80).grid(row=7, column=1, pady=5)

        self.apply_themes_to_all(self.shop_window)
        self.shop_window.after(100, self.shop_window.lift)
        self.shop_window.after(100, self.shop_window.focus_force)

    # ===== AFTER REVIEW PROMPT ===== #
    def ask_after_review(self, correct=0, wrong=0):
        """Ask the user if they want to use or buy powerups after a review session."""
        inventory = self.get_inventory()
        has_double = inventory.get("Double Coins", 0) >= 1

        if has_double:
            bonus = max(0, correct - wrong) * 5
            if messagebox.askyesno("Use Double Coins?",
                                   f"Use your Double Coins potion? You'll earn {bonus} coins! ({correct} correct - {wrong} wrong) x5"):
                self.use_double_coins(correct, wrong)
        else:
            bonus = max(0, correct - wrong) * 5
            if messagebox.askyesno("Buy Double Coins?",
                                   f"Buy Double Coins for 50 coins? You'd earn {bonus} bonus coins this session!"):
                if self.buy_powerup2():
                    if messagebox.askyesno("Use it now?", f"Use it now for {bonus} coins?"):
                        self.use_double_coins(correct, wrong)

    # ===== STUBS ===== #
    def update_listbox(self, display):
        """Overridden by Flashcard."""
        pass

    def failed_streak(self, file_path):
        """Overridden by Habit."""
        pass
