import os
import datetime
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from .config import habit_trainer_folder_path, TIMESTAMP_FORMAT


def read_last_timestamp(file_path: str):
    """Read the last timestamp from a habit file."""
    with open(file_path, "r") as f:
        content = f.readlines()
        content = content[-1].strip()
        return datetime.datetime.strptime(content, TIMESTAMP_FORMAT)


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
        pass  # Just clear the file


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

    # Check if the habit already exists
    if os.path.exists(new_habit_file_path):
        messagebox.showinfo("Info", "Habit already exists.")
        return

    # Create the habit file
    with open(new_habit_file_path, "w") as f:
        pass  # Create empty file

    messagebox.showinfo("Success", f"New habit added: {new_habit}.")
    print("Habit added successfully")


def create_habit_frontend(frame, habit_add_button: Button):
    """Frontend UI for creating a new habit."""
    # Creating a heading
    new_habit_heading = ttk.Label(frame, text="Enter a new habit: ")
    new_habit_heading.grid(row=7, column=2)

    # Create entry box
    new_habit_input = ttk.Entry(frame, width=30)
    new_habit_input.grid(row=8, column=2)

    habit_add_button.destroy()

    # Creating button
    new_habit_submit_button = ttk.Button(
        frame,
        text="Submit",
        command=lambda: create_habit_backend(new_habit_input)
    )
    new_habit_submit_button.grid(row=9, column=2)


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
    except:
        pass

    selected_habit = habit_selected.split(":", 1)[0]
    target_file = f"{selected_habit}.txt" if not selected_habit.lower().endswith(".txt") else selected_habit
    file_path = os.path.join(habit_trainer_folder_path, target_file)

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Habit not found.")
        return

    # For first time users: Start streak at 1 and write timestamp
    if new_streak(file_path):
        messagebox.showinfo("First Check", f"Congrats, this is your first check for {selected_habit}.")
        write_timestamp(file_path, datetime.datetime.now())
        return

    now = datetime.datetime.now()
    last = read_last_timestamp(file_path)
    days_diff = (now.date() - last.date()).days

    if days_diff == 0:
        # Already checked today
        current_streak = read_streak(file_path)
        messagebox.showinfo("Info",
                            f"You've already completed this habit today. Current streak: {current_streak}")
        print(f"Already checked today. Streak = {current_streak}")

    elif days_diff == 1:
        # Consecutive day: increment streak
        streak = check_streak(file_path)
        streak += 1
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"Nice! Streak increased to {streak}.")
        print(f"Recorded today. Streak = {streak}")

    elif days_diff >= 2:
        # Missed one or more days: reset streak to 1
        streak = 1
        failed_streak(file_path)
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"You're late by {days_diff} day(s). Streak reset to {streak}.")
        print(f"Streak reset = {streak}")

    else:
        # Negative diff (clock or timezone change)
        streak = max(1, check_streak(file_path))
        write_timestamp(file_path, now)
        messagebox.showinfo("Info", f"Time anomaly detected. Streak preserved at {streak}.")
        print(f"Anomaly detected. Streak = {streak}")