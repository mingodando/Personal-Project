import os
import json
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from .config import flashcard_folder_path, flashcard_files



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
    
    # Update the display


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


def add_card(edit_listbox, file_name, folder_name, frame):
    """Add a flashcard to a file."""
    final_file_path = os.path.join(flashcard_folder_path, folder_name, file_name)

    # Load existing data or start fresh
    data = {}
    if os.path.exists(final_file_path):
        with open(final_file_path, "r") as d:
            try:
                loaded = json.load(d)
                if isinstance(loaded, dict):
                    data = loaded
                else:
                    messagebox.showerror("Error", "Unsupported file format. Expected a JSON object.")
                    return
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"Invalid JSON in file:\n{final_file_path}\n\n{e}")
                return

    # Create inputs
    question_heading = ttk.Label(frame, text="Enter the question:", borderwidth=1)
    question_heading.grid(row=20, column=6, sticky="n")
    question = ttk.Entry(frame)
    question.grid(row=21, column=6, sticky="n")

    answer_heading = ttk.Label(frame, text="Enter the answer:", borderwidth=1)
    answer_heading.grid(row=22, column=6, sticky="n")
    answer = ttk.Entry(frame)
    answer.grid(row=23, column=6, sticky="n")

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
            with open(final_file_path, "w") as f:
                json.dump(data, f, indent=4)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to save:\n{final_file_path}\n\n{e}")
            return

        # Update listbox
        edit_listbox.insert(END, f"{q}: {a}")

        # Clear inputs
        question.delete(0, END)
        answer.delete(0, END)
        question.focus_set()

    add_btn = ttk.Button(frame, text="Add Card", command=on_add)
    add_btn.grid(row=28, column=6, sticky="n")


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
    edit_question_heading = ttk.Label(frame, text="Enter the question:", borderwidth=1)
    edit_question_heading.grid(row=20, column=7, sticky="n")
    edit_question = ttk.Entry(frame)
    edit_question.grid(row=21, column=7, sticky="n")
    edit_question.insert(0, selected_question)

    edit_answer_heading = ttk.Label(frame, text="Enter the answer:", borderwidth=1)
    edit_answer_heading.grid(row=22, column=7, sticky="n")
    edit_answer = ttk.Entry(frame)
    edit_answer.grid(row=23, column=7, sticky="n")
    edit_answer.insert(0, selected_answer)

    edit_done_button = ttk.Button(
        frame,
        text="Done",
        command=lambda: edit_done(file_name, folder_name, edit_question, edit_answer, item_selected)
    )
    edit_done_button.grid(row=28, column=7, sticky="n")


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