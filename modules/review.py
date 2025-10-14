import os
import json
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import TclError
from .config import flashcard_folder_path


def review_frontend(frame):
    """Create the review interface."""
    folder_name_heading = ttk.Label(frame, text="Enter the name of the folder:", borderwidth=1)
    folder_name_heading.grid(row=1, column=10, sticky="n")

    folder_name = ttk.Entry(frame)
    folder_name.grid(row=2, column=10, sticky="n")
    folder_name.focus_set()

    folder_name_submit = ttk.Button(
        frame,
        text="Submit",
        command=lambda: list_folder_files(folder_name.get())
    )
    folder_name_submit.grid(row=3, column=10, sticky="n")

    file_name_heading = ttk.Label(frame, text="Enter the name for your flashcard file:", borderwidth=1)
    file_name_heading.grid(row=4, column=10, sticky="n")

    file_name = ttk.Entry(frame)
    file_name.grid(row=5, column=10, sticky="n")

    file_name_submit = ttk.Button(
        frame,
        text="Submit",
        command=lambda: review_listbox_backend(folder_name, file_name, frame)
    )
    file_name_submit.grid(row=6, column=10, sticky="n")


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
    question_heading = ttk.Label(frame, text=f"1. : {items[0][0]}")
    question_heading.grid(row=8, column=10, sticky="n", borderwidth=1)

    question_entry = ttk.Entry(frame)
    question_entry.grid(row=9, column=10, sticky="n")
    question_entry.focus_set()

    question_submit = ttk.Button(
        frame,
        text="Submit",
        command=lambda: question_check(question_entry, question_heading)
    )
    question_submit.grid(row=10, column=10, sticky="n")

    # Store state
    question_heading.items = items
    question_heading.idx = 0
    question_heading.correct = 0
    question_heading.wrong = 0
    question_heading.submit_btn = question_submit


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
            question_heading.config(text=f"{idx + 1}. : {next_question}")
            question_entry.focus_set()
        else:
            total = correct + wrong
            messagebox.showinfo("Info Dialog", "All questions completed!")
            messagebox.showinfo("Info Dialog",
                                f"Correct: {correct}, Wrong: {wrong}, Total: {correct}/{total}")
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