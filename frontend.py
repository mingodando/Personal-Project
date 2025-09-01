from tkinter import *
import datetime
import os

folder_path = r"C:\Users\Ming\PycharmProjects\Personal Project\Habit Trainer"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

#Frontend Functions
def create_habit_frontend():
    new_habit_heading = Label(root, text="Enter a new habit: ")
    new_habit_heading.grid(row=0, column=1)

    new_habit_input = Entry(root, width=30)
    new_habit_input.grid(row=1, column=1)

def create_habit_backend(new_habit_input):
    new_habit = new_habit_input.get()
    habit = new_habit

    with open(f"{habit}.txt", "w") as f:
        f.write(habit)
        print("Habit added successfully.")
        f.close()
        print("New habit added:", new_habit)

#Backend Functions
def read_last_timestamp(file_path: str) -> datetime.datetime | None:
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                return datetime.datetime.strptime(last_line.strip(), TIMESTAMP_FORMAT)
    except FileNotFoundError:
        pass
    return None

def write_timestamp(file_path: str, dt: datetime.datetime) -> None:
    with open(file_path, "w") as f:
        f.write(dt.strftime(TIMESTAMP_FORMAT))

def _same_calendar_day(a: datetime.datetime, b: datetime.datetime) -> bool:
    return a.date() == b.date()

def yes(new_habit):
    # Kept for compatibility, but now writes a properly formatted timestamp if you still use it.
    file_path = f"{new_habit}.txt"
    current = datetime.datetime.now()
    write_timestamp(file_path, current)
    print("Habit started:", current.strftime(TIMESTAMP_FORMAT))

def check():
    habit_input_heading = Label(root, text="Enter the habit you want to check: ")
    habit_input_heading.grid(row=0, column=1)

    habit_input = Entry(root, width=30)
    habit_input.grid(row=1, column=1)


    habit_name = input("Enter the habit you want to check: ").strip()
    file_path = f"{habit_name}.txt"

    if not os.path.exists(file_path):
        print("File does not exist. Please create it first; that will count as the first appearance.")
        return

    now = datetime.datetime.now()
    last = read_last_timestamp(file_path)

    if last and _same_calendar_day(last, now):
        print(f"Already checked today at {last.strftime('%H:%M')}.")
    else:
        if last:
            days_diff = (now.date() - last.date()).days
            if days_diff >= 1:
                # Show a warning when at least one calendar day has passed since last check
                print(f"Warning: you are {days_diff} day(s) late. Last check was {last.strftime(TIMESTAMP_FORMAT)}.")
        else:
            print("No previous check timestamp found in the file.")

    choice = input('Type "exit" to record today\'s check and exit, or press Enter to cancel: ').strip().lower()
    if choice == "exit":
        write_timestamp(file_path, now)
        print(f"Recorded today at {now.strftime(TIMESTAMP_FORMAT)}.")
    else:
        print("No changes saved.")


#Tkinter window
root = Tk()

check()

root.title("Habit Trainer")
root.geometry("400x500")

