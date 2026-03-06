import os
from tkinter import END, messagebox
from datetime import datetime, date
import customtkinter as ctk

from shop import Shop


class Habit(Shop):
    def __init__(self):
        super().__init__()
        self.habit_create_frame = None

    # ----- Streak File Helpers ----- #
    def read_last_timestamp(self, file_path: str):
        """Read the last timestamp from a habit file."""
        with open(file_path, "r") as f:
            content = f.readlines()
            if content:
                last = content[-1].strip()
                return datetime.strptime(last, self.TIMESTAMP_FORMAT)
        return None

    def write_timestamp(self, file_path: str, timestamp: datetime):
        """Write a timestamp to a habit file."""
        with open(file_path, "a") as f:
            f.write(timestamp.strftime(self.TIMESTAMP_FORMAT) + "\n")

    @staticmethod
    def read_streak(file_path: str):
        """Read current streak count from a habit file."""
        with open(file_path, "r") as f:
            return len(f.readlines())

    @staticmethod
    def failed_streak(file_path: str):
        """Reset the streak by clearing the file."""
        with open(file_path, "w"):
            pass

    @staticmethod
    def new_streak(file_path: str):
        """Check if this is a new streak (empty file)."""
        with open(file_path, "r") as f:
            return not f.read()

    @staticmethod
    def check_streak(_streak_path: str) -> int:
        """Get current streak count."""
        with open(_streak_path, "r") as f:
            return int(len(f.readlines()))

    # ----- Habit CRUD ----- #
    def create_habit_backend(self, new_habit_input: ctk.CTkEntry, habit_listbox):
        """Backend logic for creating new habits."""
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

    def create_habit_frontend(self, frame, habit_listbox):
        """Build the Create Habit UI form."""
        new_habit_heading = ctk.CTkLabel(
            self.habit_create_frame,
            text="Enter a new habit:",
            font=self.SUBTITLE_FONT
        )
        new_habit_heading.grid(row=0, column=0, padx=10, pady=(10, 2), sticky="w")

        new_habit_input = ctk.CTkEntry(self.habit_create_frame, width=200, font=self.REGULAR_FONT)
        new_habit_input.grid(row=1, column=0, padx=10, pady=(2, 5), sticky="w")
        new_habit_input.focus_set()

        new_habit_submit_button = ctk.CTkButton(
            self.habit_create_frame,
            text="Submit",
            font=self.REGULAR_FONT,
            command=lambda: self.create_habit_backend(new_habit_input, habit_listbox)
        )
        new_habit_submit_button.grid(row=2, column=0, padx=10, pady=(2, 10), sticky="w")

        saved_theme = self.load_theme_preference()
        self.apply_theme(frame, saved_theme)

    def delete_habit(self, habit_listbox):
        """Delete a habit by removing the file and updating the listbox."""
        habit_selection = habit_listbox.curselection()
        if not habit_selection:
            messagebox.showinfo("Info Dialog", "No habit selected.")
            return

        habit_index = habit_selection[0]
        habit_entry = habit_listbox.get(habit_index)
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

        try:
            habit_listbox.delete(habit_index)
        except Exception:
            pass

        messagebox.showinfo("Success", "Habit deleted.")

    def on_check(self, habit_listbox):
        """Check a habit to update the streak."""
        habit_selection = habit_listbox.curselection()
        if not habit_selection:
            messagebox.showinfo("Info Dialog", "No habit selected.")
            return

        habit_indices = habit_selection[0]
        habit_selected = habit_listbox.get(habit_indices)
        print(f"Selected habit: {habit_selected}")

        try:
            habit_listbox.itemconfig(habit_indices, bg="green")
        except Exception:
            pass

        selected_habit = habit_selected.split(":", 1)[0]
        target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
        file_path = os.path.join(self.habit_trainer_folder_path, target_file)

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Habit not found.")
            return

        if self.new_streak(file_path):
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
            messagebox.showinfo("Info", f"You've already completed this habit today. Current streak: {current_streak}")

        elif days_diff == 1:
            streak = self.check_streak(file_path) + 1
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"Nice! Streak increased to {streak}.")

        elif days_diff == 2:
            inventory = self.get_inventory()
            if inventory.get("Habit Revive", 0) >= 1:
                self.habit_revive_function(file_path)
                self.write_timestamp(file_path, now)
            else:
                response = messagebox.askyesno("Buy More?", "Do you want to buy more powerups?")
                if not response:
                    self.failed_streak(file_path)
                else:
                    self.buy_powerup1()
                    messagebox.showinfo("Success", "Now Recheck your habit to confirm!")

        elif days_diff > 2:
            self.failed_streak(file_path)
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"You're late by {days_diff} day(s). Streak reset to 1.")

        else:
            streak = max(1, self.check_streak(file_path))
            self.write_timestamp(file_path, now)
            messagebox.showinfo("Info", f"Time anomaly detected. Streak preserved at {streak}.")

    @staticmethod
    def habit_listbox_checked(habit_trainer_files, habit_trainer_folder_path, habit_listbox):
        """Color habit listbox entries green/red based on today's check."""
        today = str(date.today())
        for i, f in enumerate(habit_trainer_files):
            file_path = os.path.join(habit_trainer_folder_path, f)
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r") as file:
                lines = file.readlines()
                if not lines:
                    habit_listbox.itemconfig(i, bg="red")
                    continue
                last_line = lines[-1].strip()
                if last_line == today:
                    habit_listbox.itemconfig(i, bg="green")
                else:
                    habit_listbox.itemconfig(i, bg="red")
