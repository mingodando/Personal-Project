import os
from tkinter import *
from tkinter import ttk
import webbrowser

# Import from modules
from modules.config import flashcard_files, habit_trainer_files
from modules.themes import apply_theme, load_theme_preference, create_theme_buttons
from modules.habits import create_habit_frontend, on_check
from modules.flashcards import (
    no_list_files, yes_list_files, create_folder_and_file,
    create_file, rename_folder, add_card, edit_card
)
from modules.review import review_frontend

from modules.rename import open_rename, add_folder_and_file, open_add_folder_and_file, edit_flashcards_frontend, edit_flashcard_cl

frame1 = None
frame2 = None
display = None

def update_listbox(display):
    """Refresh the listbox."""
    if display is None:
        return

    # Clear the whole listbox:
    display.delete(0, END)

    # Re-scan and input:
    from modules.config import flashcard_folder_path
    if os.path.exists(flashcard_folder_path):
        folders = [f for f in os.listdir(flashcard_folder_path)
                   if os.path.isdir(os.path.join(flashcard_folder_path, f))]
        for folder in sorted(folders):
            display.insert(END, folder)


def main():
    """Main application entry point."""
    global frame1, frame2, display

    root = Tk()
    root.title("Flashcard Feature")
    root.geometry("1600x600")
    root.configure(bg="#FFFFFF")

    flashcard = ttk.Notebook(root)
    flashcard.grid(row=0, column=0, sticky="nsew")

    # Frame 2 - Home (LEFT - First tab)
    frame2 = Frame(flashcard, width=1300, height=800)
    frame2.grid(row=0, column=0)
    flashcard.add(frame2, text="Home")

    # Frame 1 - Flashcards (RIGHT - Second tab)
    frame1 = Frame(flashcard, width=1203, height=570)
    frame1.grid(row=0, column=1)
    flashcard.add(frame1, text="Flashcards")

    # ===== FRAME 1 UI (FLASHCARDS PAGE) =====

    # Flashcard list
    heading1 = ttk.Label(frame1, text="Available Flashcard", font=("Arial", 20),
                         borderwidth=1, relief="solid")
    heading1.grid(row=0, column=0, rowspan=2, columnspan=3)

    list_frame = ttk.Frame(frame1)
    list_frame.grid(row=2, column=0, columnspan=3, rowspan=15, sticky="nsew")

    display = Listbox(list_frame, width=50, height=10)
    for file in flashcard_files:
        display.insert(END, file)
    display.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical")
    scrollbar.grid(row=0, column=1, rowspan=10, sticky="ns")

    display.config(yscrollcommand=scrollbar.set, font=("Arial", 12))
    scrollbar.config(command=display.yview)

    list_frame.grid_rowconfigure(0, weight=2)
    list_frame.grid_columnconfigure(0, weight=2)

    # Rename section
    rename_header = ttk.Label(frame1, text="Rename", font=("Arial", 20),
                              borderwidth=1, relief="solid", width=10)
    rename_header.grid(row=17, column=0, sticky="nsew")
    open_rename()

    # Add folder section
    add_folder_header = ttk.Label(frame1, text="Add Folder", font=("Arial", 15),
                                  borderwidth=3, relief="solid")
    add_folder_header.grid(row=17, column=1, sticky="n", rowspan=2)
    open_add_folder_and_file()

    # Edit section
    edit_title = ttk.Label(frame1, text="     Edit     ", font=("Arial", 15),
                           borderwidth=3, relief="solid")
    edit_title.grid(row=0, column=3, sticky="s", columnspan=3)
    edit_flashcards_frontend()

    # Review section
    review_heading = ttk.Label(frame1, text="     Review     ", font=("Arial", 15),
                               borderwidth=3, relief="solid")
    review_heading.grid(row=0, column=10, sticky="n", columnspan=3)
    review_frontend(frame1)

    # Theme buttons for frame1
    theme_frame1 = create_theme_buttons(frame1, frame1, frame2)
    theme_frame1.grid(row=30, column=29, columnspan=3, padx=15, pady=15, sticky="se")

    # ===== FRAME 2 UI =====

    #Introduction:

    # Welcome heading
    welcome_heading = ttk.Label(
        frame2,
        text="Welcome to Pro Bo!",
        font=("Arial", 20, "bold")
    )
    welcome_heading.grid(row=0, column=1, columnspan=3, pady=20)

    # Welcome text
    welcome_text = ttk.Label(
        frame2,
        text="""Pro Bo is a study app that helps you study better.
    I hope you find this app useful! It is free to use.

    If you have any questions or suggestions,
    please feel free to contact me:""",
        font=("Arial", 12),
        justify="center"
    )
    welcome_text.grid(row=1, column=1, columnspan=3, pady=10)

    # Function to open email
    def open_email():
        email = "mingl_2028@concordian.org"
        subject = "Feedback about Pro Bo App"
        body = "Hello,\n\nI have a question/suggestion about Pro Bo:\n\n"

        # Create mailto link with pre-filled subject and body
        mailto_link = f"mailto:{email}?subject={subject}&body={body}"
        webbrowser.open(mailto_link)

    # Clickable email label (looks like a link)
    email_label = ttk.Label(
        frame2,
        text="✉ mingl_2028@concordian.org",
        font=("Arial", 12, "underline"),
        foreground="blue",
        cursor="arrow"
    )
    email_label.grid(row=2, column=1, columnspan=3, pady=10)
    email_label.bind("<Button-1>", lambda e: open_email())

    # OR use a button instead
    email_button = ttk.Button(
        frame2,
        text="📧 Contact Me",
        command=open_email
    )
    email_button.grid(row=3, column=1, columnspan=3, pady=10)

    # Habit listbox
    habit_listbox = Listbox(frame2, width=10, height=15, font=("Arial", 16))
    for i in habit_trainer_files:
        habit_listbox.insert(END, i)
    habit_listbox.grid(row=2, column=0, rowspan=9, sticky="nsew")


    # Habit buttons
    habit_check_button = ttk.Button(frame2, text="Check Habit",
                                    command=lambda: on_check(habit_listbox))
    habit_check_button.grid(row=2, column=2)

    habit_create_button = ttk.Button(frame2, text="Create Habit",
                                     command=lambda: create_habit_frontend(frame2, habit_create_button))
    habit_create_button.grid(row=3, column=2)

    # Theme buttons for frame2
    theme_frame2 = create_theme_buttons(frame2, frame1, frame2)
    theme_frame2.grid(row=5, column=3, rowspan=2, padx=15, pady=15, sticky="e")

    # Load and apply saved theme
    saved_theme = load_theme_preference()
    apply_theme(frame1, saved_theme)
    apply_theme(frame2, saved_theme)

    root.mainloop()

main()