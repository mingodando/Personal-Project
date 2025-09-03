import os
import json
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkinter import TclError
import datetime

flashcard_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Flashcards Files"
habit_trainer_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Habit Trainer"
flashcard_files = os.listdir(flashcard_folder_path)
habit_trainer_files = os.listdir(habit_trainer_folder_path)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M"

#######################################################################################

def read_last_timestamp(file_path: str) -> datetime.datetime | None:
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
        # Try to parse the entire file as a single timestamp in our format.
        # If the file contains something else (e.g., just the habit name), parsing will fail and we return None.
        return datetime.datetime.strptime(content, TIMESTAMP_FORMAT)
    except Exception:
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

#Frontend Functions
def create_habit_frontend():
    new_habit_heading = Label(root, text="Enter a new habit: ")
    new_habit_heading.grid(row=0, column=1)

    new_habit_input = Entry(root, width=30)
    new_habit_input.grid(row=1, column=1)

    habit_add_button.destroy()

    new_habit_submit_button = Button(root, text="Submit", command=lambda: create_habit_backend(new_habit_input))
    new_habit_submit_button.grid(row=6, column=1)

def create_habit_backend(new_habit_input):
    new_habit = new_habit_input.get()
    habit = new_habit

    with open(f"{habit}.txt", "w") as f:
        f.write(habit)
        print("Habit added successfully.")
        print("New habit added:", new_habit)

def get_selected_habit():
    selected_habit = habit_listbox.get(habit_listbox.curselection())
    print("Selected habit:", selected_habit)
    return selected_habit

def check():
    def on_check():
        habit_selection = habit_listbox.curselection()
        if habit_selection:
            habit_indices = habit_selection[0]
            habit_selected = habit_listbox.get(habit_indices)
            print(f"Selected habit: {habit_selected}")
            if not habit_selection:
                print("Please enter a habit name.")
                return

            file_path = habit_selection
            print(file_path)

            if os.path.exists(file_path):
                print(f"File found: {file_path}")
            else:
                print(f"File not found: {file_path}")
                return

            now = datetime.datetime.now()
            last = read_last_timestamp(file_path)

            if last and _same_calendar_day(last, now):
                print(f"Already checked today at {last.strftime('%H:%M')}.")
                return

            if last:
                days_diff = (now.date() - last.date()).days
                if days_diff >= 1:
                    print(f"Warning: you are {days_diff} day(s) late. Last check was {last.strftime(TIMESTAMP_FORMAT)}.")
            else:
                print("No previous check timestamp found in the file.")

            # Record immediately on button click
            write_timestamp(file_path, now)
            print(f"Recorded today at {now.strftime(TIMESTAMP_FORMAT)}.")
        else:
            messagebox.showerror("Error", "Please select a habit.")

    habit_check_button.destroy()

    check_now_btn = Button(frame2, text="Check Now", command=lambda: on_check()
)
    check_now_btn.grid(row=6, column=1)
    check_now_btn.grid(row=5, column=1)

#######################################################################################

def open_rename():
    heading_rename1 = Label(frame1,
                            text="Old Folder Name:",
                            font = ("Arial", 15),
                            borderwidth=1)
    heading_rename1.grid(row=19,
                         column=0,
                         sticky="n",
                         columnspan=3)
    heading_rename1.configure(bg="#FFFFFF")
    heading_rename2 = Label(frame1,
                            text="New Folder Name:",
                            font = ("Arial", 15),
                            borderwidth=1)
    heading_rename2.grid(row=21,
                         column=0,
                         sticky="n",
                         columnspan=3)
    heading_rename2.configure(bg="#FFFFFF")
    #Input
    input_old_folder = Entry(frame1,borderwidth=1)
    input_new_folder = Entry(frame1,borderwidth=1)
    input_old_folder.grid(row=20,
                          column=0,
                          sticky="n",
                          columnspan=3)
    input_old_folder.configure(bg="#FFFFFF")
    input_old_folder.focus_set()
    input_new_folder.grid(row=22,
                          column=0,
                          sticky="n",
                          columnspan=3)
    input_new_folder.configure(bg="#FFFFFF")
    #Submit Button
    rename_submit = (Button
                     (frame1,
                      text="Submit",
                      command=lambda: rename(input_old_folder, input_new_folder),
                      bg="#FFFFFF"
                      ))
    rename_submit.grid(row=23,
                       column=0,
                       sticky="n",
                       columnspan=3)
    rename_submit.configure(bg="#FFFFFF")

#######################################################################################

def rename(input_old_folder, input_new_folder):
    input_old_folder_name = input_old_folder.get()
    input_new_folder_name = input_new_folder.get()
    if input_old_folder_name in flashcard_files:
        #Rename
        os.rename(os.path.join(flashcard_folder_path, input_old_folder_name),
                  os.path.join(flashcard_folder_path, input_new_folder_name))
        messagebox.showinfo("Info Dialog",
                            f"Folder '{input_old_folder_name}' renamed to '{input_new_folder_name}'.")
        return
    else:
        messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")
#######################################################################################


def create_folder_and_file(folder_name, file_name):
    os.mkdir(os.path.join(flashcard_folder_path, folder_name))
    messagebox.showinfo("Info Dialog", f"Folder '{folder_name}' created successfully.")
    create_file(folder_name, file_name)

def create_file(folder_name, file_name):
    with open(os.path.join(flashcard_folder_path, folder_name, f"{file_name}.json"), "w") as e:
        json.dump({}, e)
        messagebox.showinfo("Info Dialog", f"File '{file_name}.json' created successfully.")

def yes_list_files(folder_name):
    if folder_name in flashcard_files:
        messagebox.showerror("Error", "Folder already exists. Please enter a different name.")
        return
    elif folder_name not in flashcard_files:
        messagebox.showinfo("Info Dialog", "Please Go On!")

def no_list_files(folder_name):
    if folder_name in flashcard_files:
        messagebox.showinfo("Info Dialog", f"Files in folder : {os.listdir(folder_name)}")
    else:
        messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")

#######################################################################################

def edit_flashcard_cl(file_name, folder_name):
    file_name = f"{file_name.lower()}.json"
    folder_name = folder_name.lower()
    final_file_path = os.path.join(flashcard_folder_path, folder_name, file_name)

    #listbox
    edit_frame = Frame(frame1)
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
                      sticky="nsew")

    edit_scrollbar = Scrollbar(edit_frame, orient='vertical')
    edit_scrollbar.grid(row=0,
                        column=1,
                        sticky="ns")

    edit_listbox.config(yscrollcommand=edit_scrollbar.set)
    edit_scrollbar.config(command=edit_listbox.yview)

    # Populate the Listbox with the contents of the JSON file
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

    # Insert items based on expected structure (dict of question -> answer)
    if isinstance(data, dict):
        for key, value in data.items():
            edit_listbox.insert(END, f"{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            edit_listbox.insert(END, str(item))
    else:
        edit_listbox.insert(END, str(data))

    edit_listbox.bind("<<ListboxSelect>>", lambda event: listbox_select(edit_listbox, file_name, folder_name, event.widget.get(event.widget.curselection())))

#######################################################################################

def listbox_select(edit_listbox, file_name, folder_name, item_selected):
    item_selection = edit_listbox.curselection()
    if item_selection:
        item_indices = item_selection[0]
        item_selected = edit_listbox.get(item_indices)
        print(f"Selected item: {item_selected}")

    else:
        messagebox.showinfo("Info Dialog", "No item selected.")

    add_heading = Label(frame1, text="Add", font=("Arial", 15), borderwidth=1, relief="solid")
    add_heading.grid(row=19,
                     column=6,
                     sticky="s")

    add_card(edit_listbox, file_name, folder_name)

    edit_heading = Label(frame1, text="Edit", font=("Arial", 15), borderwidth=1, relief="solid")
    edit_heading.grid(row=19,
                      column=7,
                      sticky="s")

    edit_card(edit_listbox, file_name, folder_name, item_selected)

#######################################################################################

def add_card(edit_listbox, file_name, folder_name):
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

    # Create inputs once
    question_heading = Label(frame1,
                             text="Enter the question: ",
                             borderwidth=1)
    question_heading.grid(row=21,
                          column=6,
                          sticky="n")
    question = Entry(frame1, borderwidth=1)
    question.grid(row=22,
                  column=6,
                  sticky="n")

    answer_heading = Label(frame1,
                           text="Enter the answer: ",
                           borderwidth=1)
    answer_heading.grid(row=23,
                        column=6,
                        sticky="n")
    answer = Entry(frame1, borderwidth=1)
    answer.grid(row=24,
                column=6,
                sticky="n")

    def on_add():
        q = question.get().strip()
        a = answer.get().strip()
        if not q or not a:
            messagebox.showerror("Error", "Both question and answer are required.")
            return
        data[q] = a  # store strings, not Entry widgets
        # Persist immediately
        try:
            with open(final_file_path, "w") as f:
                json.dump(data, f, indent=4)
        except OSError as q:
            messagebox.showerror("Error", f"Failed to save:\n{final_file_path}\n\n{q}")
            return
        # Update listbox for immediate feedback
        edit_listbox.insert(END, f"{q}: {a}")
        # Clear inputs for next entry
        question.delete(0, END)
        answer.delete(0, END)
        question.focus_set()

    add_btn = Button(frame1,
                     text="Add Card",
                     command=on_add)
    add_btn.grid(row=28,
                 column=6,
                 sticky="n")

    def on_done():
        # Optionally ensure latest edits are saved (already saved on Add)
        # Clean up the input widgets
        for w in (question_heading, question, answer_heading, answer, add_btn, done_button):
            try:
                w.destroy()
            except TclError:
                pass

    done_button = Button(frame1, text="Done", command=on_done)
    done_button.grid(row=20,
                     column=6,
                     sticky="n",
                     columnspan=2)

    #######################################################################################

def edit_card(edit_listbox, file_name, folder_name, item_selected):
    item_selection = edit_listbox.curselection()
    if item_selection:
        item_indices = item_selection[0]
        item_selected = edit_listbox.get(item_indices)
        print(f"Selected item: {item_selected}")
        selected_question = item_selected.split(":", 1)[0].strip()
        selected_answer = item_selected.split(":", 1)[1].strip() if ":" in item_selected else ""

        edit_heading = Label(frame1, text="Edit", font=("Arial", 15), borderwidth=1, relief="solid")
        edit_heading.grid(row=19,
                          column=7,
                          sticky="s")

        edit_question_heading = Label(frame1, text="Enter the question: ", borderwidth=1)
        edit_question_heading.grid(row=21,
                                   column=7,
                                   sticky="n")
        edit_question = Entry(frame1, borderwidth=1)
        edit_question.grid(row=22,
                           column=7,
                           sticky="n")
        edit_question.insert(0, selected_question)

        edit_answer_heading = Label(frame1, text="Enter the answer: ", borderwidth=1)
        edit_answer_heading.grid(row=23,
                                 column=7,
                                 sticky="n")
        edit_answer = Entry(frame1, borderwidth=1)
        edit_answer.grid(row=24,
                         column=7,
                         sticky="n")
        edit_answer.insert(0, selected_answer)

        edit_done_button = Button(frame1, text="Done", command=lambda: edit_done(file_name, folder_name, edit_question, edit_answer, item_selected))
        edit_done_button.grid(row=28,
                              column=7,
                              sticky="n")

    else:
        messagebox.showerror("Info Dialog", "No item selected.")

#######################################################################################

def edit_done(file_name, folder_name, edit_question, edit_answer, item_selected):
    target_file = f"{file_name}.json" if not file_name.lower().endswith(".json") else file_name
    final_file_path = os.path.join(flashcard_folder_path, folder_name, target_file)

    data = {}
    with open(final_file_path, "r") as f:
        data = json.load(f)

    # Extract text values from the Entry widgets
    new_question = edit_question.get().strip() if hasattr(edit_question, "get") else str(edit_question).strip()
    new_answer = edit_answer.get().strip() if hasattr(edit_answer, "get") else str(edit_answer).strip()

    # Validate inputs
    if not new_question or not new_answer:
        messagebox.showerror("Error", "Both question and answer are required.")
        return

    # Derive the original question key from the listbox item ("Question: Answer")
    original_question = item_selected.split(":", 1)[0].strip()
    print(original_question)

    if original_question not in data:
        messagebox.showerror("Error",
                             f"Original flashcard not found: '{original_question}'. It may have been renamed or removed.")
        return

    # If the question text hasn't changed, just update the answer
    if new_question == original_question:
        data[original_question] = new_answer
    else:
        del data[original_question]
        data[new_question] = new_answer

    with open(final_file_path, "w") as f:
        json.dump(data, f, indent=4)
        messagebox.showinfo("Info Dialog", "Flashcard edited successfully.")

#######################################################################################

def edit_flashcards_frontend():
    folder_name_heading = Label(frame1,
                                text="Enter the name of the folder: ",
                                borderwidth=1)
    folder_name_heading.grid(row=11,
                             column=4,
                             sticky="n")

    folder_name = Entry(frame1, borderwidth=1)
    folder_name.grid(row=12,
                     column=4,
                     sticky="n")

    folder_name_submit = Button(frame1,
                                text="Submit",
                                command=lambda: no_list_files(folder_name.get()))
    folder_name_submit.grid(row=13,
                            column=4,
                            sticky="n")

    file_name_heading = Label(frame1,
                              text="Enter the name for your flashcard file: ",
                              borderwidth=1)
    file_name_heading.grid(row=14,
                           column=4,
                           sticky="n")

    file_name = Entry(frame1, borderwidth=1)
    file_name.grid(row=15,
                   column=4,
                   sticky="n")

    file_name_submit = Button(frame1,
                              text="Submit",
                              command=lambda: edit_flashcard_cl(file_name.get(),
                                                                folder_name.get()))
    file_name_submit.grid(row=16,
                          column=4,
                          sticky="n")

def done():
    return

#######################################################################################
def open_add_folder_and_file():
    command_header = Label(frame1,text="Do you want to create a new folder? (y/n): ")
    command_header.grid(row=0,
                        column=6,
                        columnspan=3)

    command = Entry(frame1,borderwidth=1)
    command.grid(row=1,
                 column=6,
                 columnspan=3)

    command_submit = Button(frame1,
                            text="Submit",
                            command=lambda: add_folder_and_file(command))
    command_submit.grid(row=3,
                        column=6,
                        sticky="n",
                        columnspan=3)

#######################################################################################


def add_folder_and_file(command):
    command_request = command.get().lower()

    if command_request == "y" or command_request == "yes":
        folder_name_heading = Label(frame1,
                                    text="Enter the name of the folder: ",
                                    borderwidth=1)
        folder_name_heading.grid(row=2,
                                 column=4,
                                 sticky="n")

        folder_name = Entry(frame1, borderwidth=1)
        folder_name.grid(row=3,
                         column=4,
                         sticky="n")
        folder_name.focus_set()
        print(folder_name)

        folder_name_submit = Button(frame1,
                                    text="Submit",
                                    command=lambda: yes_list_files(folder_name.get()),
                                    borderwidth=1)

        folder_name_submit.grid(row=4,
                                column=4,
                                sticky="n")
        folder_name_submit.bind("<Enter>", done())

        file_name_heading = Label(frame1,
                                  text="Enter the name for your flashcard file: ",
                                  borderwidth=1)
        file_name_heading.grid(row=5,
                               column=4,
                               sticky="n")

        file_name = Entry(frame1,
                          borderwidth=1,
                          width=10)
        file_name.grid(row=6,
                       column=4,
                       sticky="n")

        file_name_submit = Button(frame1,
                                  text="Submit",
                                  command=lambda: create_folder_and_file(folder_name.get(),
                                                                         file_name.get()),
                                  borderwidth=1)
        file_name_submit.grid(row=7,
                              column=4,
                              sticky="n")
        file_name_submit.bind("<Enter>", done())

    elif command_request == "n" or command_request == "no":
        folder_name_heading = Label(frame1, text="Enter the name of the folder: ")
        folder_name_heading.grid(row=2,
                                 column=4,
                                 sticky="n")

        folder_name = Entry(frame1,
                            borderwidth=1)
        folder_name.grid(row=3,
                         column=4,
                         sticky="n")

        folder_name_submit = Button(frame1,
                                    text="Submit",
                                    command=lambda: no_list_files(folder_name.get()))
        folder_name_submit.grid(row=4,
                                column=4,
                                sticky="n")
        folder_name_submit.bind("<Enter>", done())

        file_name_heading = Label(frame1, text="Enter the name for your flashcard file: ")
        file_name_heading.grid(row=5,
                               column=4,
                               sticky="n")

        file_name = Entry(frame1, borderwidth=1, width=10)
        file_name.grid(row=6,
                       column=4,
                       sticky="n")

        file_name_submit = Button(frame1, text="Submit", command=lambda: create_file(folder_name.get(), file_name.get()))
        file_name_submit.grid(row=7,
                              column=4,
                              sticky="n")
        file_name_submit.bind("<Enter>", done())
    else:
        messagebox.showerror("Error", "Invalid input. Please enter 'y' or 'n'.")

#######################################################################################


def themes_1(frame1, frame1_bg, ctrl_bg, fg=None, listbox_color=None, entry_color=None):
    try:
        frame1.configure(bg=frame1_bg)
    except TclError:
        pass  # Ignore widgets/options that don't accept this config

    stack = [frame1]

    while stack:  # Loop until there are no more widgets to process
        parent = stack.pop()  # Take one widget off the stack

        # Iterate over all direct children of the current widget
        for w in parent.winfo_children():

            # If a text color was provided, try to apply it
            if fg is not None:
                try:
                    w.configure(fg=fg)
                except TclError:
                    pass  # Not all widgets accept 'fg'
            # Entry-specific tweak: set the caret (insertion cursor) color for visibility
            if isinstance(w, Entry):
                w.configure(bg=entry_color)

            # Listbox-specific tweak: improve selection visibility
            elif isinstance(w, Listbox):
                w.configure(selectbackground=ctrl_bg)
                w.configure(bg=listbox_color)
                w.configure(selectforeground=fg or "black")

            # Button-specific tweak: make active colors match the theme
            elif isinstance(w, Button):
                w.configure(bg=ctrl_bg)
                if fg is not None:
                    w.configure(activeforeground=fg)

            elif isinstance(w, Label):
                w.configure(bg=ctrl_bg)

            stack.append(w)

#######################################################################################

def review_frontend():
    folder_name_heading = Label(frame1,
                                text="Enter the name of the folder: ",
                                borderwidth=1)
    folder_name_heading.grid(row=2,
                             column=10,
                             sticky="n")
    folder_name = Entry(frame1, borderwidth=1)
    folder_name.grid(row=3,
                     column=10,
                     sticky="n")
    folder_name.focus_set()

    folder_name_submit = Button(frame1,
                                text="Submit",
                                command=lambda: no_list_files(folder_name.get()),
                                borderwidth=1)

    folder_name_submit.grid(row=4,
                            column=10,
                            sticky="n")

    file_name_heading = Label(frame1,
                              text="Enter the name for your flashcard file: ",
                              borderwidth=1)
    file_name_heading.grid(row=5,
                           column=10,
                           sticky="n")
    file_name = Entry(frame1, borderwidth=1)
    file_name.grid(row=6,
                   column=10,
                   sticky="n")

    file_name_submit = Button(frame1,
                              text="Submit",
                              command=lambda: review_listbox_backend(folder_name, file_name))
    file_name_submit.grid(row=7,
                          column=10,
                          sticky="n"
                          )

def review_listbox_backend(folder_name, file_name):
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


    r_1, r_2, r_3 = 8, 9, 10

    if not items:
        messagebox.showinfo("Info Dialog", "No flashcards found in this file.")
        return

    # Show first question
    question_heading = Label(frame1, text=f"1. : {items[0][0]}")
    question_heading.grid(row=r_1, column=10, sticky="n")

    question_entry = Entry(frame1, borderwidth=1)
    question_entry.grid(row=r_2, column=10, sticky="n")
    question_entry.focus_set()

    question_submit = Button(frame1, text="Submit",
                             command=lambda: question_check(question_entry, question_heading))
    question_submit.grid(row=10, column=10, sticky="n")

    # Persist state on the label
    question_heading.items = items
    question_heading.idx = 0
    question_heading.correct = 0
    question_heading.wrong = 0
    question_heading.submit_btn = question_submit
    return

def question_check(question_entry, question_heading):
    # Retrieve state
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
        # If there are more questions, update the label text to the next one
        if idx < len(items):
            next_question = items[idx][0]
            question_heading.config(text=f"{idx + 1}. : {next_question}")
            question_entry.focus_set()
        else:
            total = correct + wrong
            messagebox.showinfo("Info Dialog", "All questions completed!")
            messagebox.showinfo("Info Dialog",
                                f"Correct: {correct}, Wrong: {wrong}, a total of {correct} / {total} questions.")
            try:
                question_heading.destroy()
            except TclError:
                pass
            try:
                question_entry.destroy()
            except TclError:
                pass
            try:
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
####################################################################################################################################

#Tkinter Window
root = Tk()

#Tabs
flashcard = ttk.Notebook(root)

frame1 = Frame(flashcard,
               width=1203,
               height=570)
frame1.grid(row=0,
            column=1)

flashcard.add(frame1, text="Flashcards")

flashcard.grid(row=0,
               column=0,
               sticky="nsew")

frame2 = Frame(flashcard,
               width=1300,
               height=800)
frame2.grid(row=0,
            column=0)
flashcard.add(frame2, text="Home")

####################################################################################################################################

#Heading
heading1 = Label(frame1,
                 text="Available Flashcard",
                 font = ("Arial", 20),
                 bg="#FFFFFF",
                 borderwidth=1,
                 relief="solid")
heading1.grid(row=0,
              column=0,
              rowspan=2,
              columnspan=3)

frame = Frame(frame1)
frame.grid(row=2,
           column=0,
           rowspan=15,
           columnspan=3,
           sticky="nsew")


display = Listbox(frame, width=50, height=15)
for file in flashcard_files:
    display.insert(END, file)
display.grid(row=2,
             column=0,
             rowspan=15,
             sticky="nsew")

scrollbar = (Scrollbar
             (frame,
                      orient="vertical",
                      bg="#FFFFFF"
                      ))
scrollbar.grid(
            row=2,
                    column=1,
                    sticky="ns",
                    rowspan=15
                    )

display.config(yscrollcommand=scrollbar.set,
               font=("Arial", 12),
               bg="#FFFFFF")
scrollbar.config(command=display.yview)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

####################################################################################################################################

#Rename Button
rename_header = Label(frame1,
                      text="Rename",
                      font = ("Arial", 20),
                      borderwidth=1,
                      relief="solid",
                      width=10,
                      bg="#FFFFFF"
                      )
rename_header.grid(row=17, column=0, columnspan=3)

open_rename()

####################################################################################################################################

#Add Folder Section:
add_folder_header = Label(frame1,
                           text="Add Folder",
                           font = ("Arial", 15),
                           borderwidth=3,
                           relief="solid",
                            )
add_folder_header.grid(row=0,
                       column=3,
                       sticky="n",
                       columnspan=3,
                       rowspan=2)

open_add_folder_and_file()


####################################################################################################################################

edit_title = Label(frame1, text="     Edit     ",
                   font=("Arial", 15),
                   borderwidth=3,
                   relief="solid")
edit_title.grid(row=9,
                column=3,
                sticky="s",
                columnspan=3)

edit_flashcards_frontend()

####################################################################################################################################

review_heading = Label(frame1, text="     Review     ",
                       font=("Arial", 15),
                       borderwidth=3,
                       relief="solid")
review_heading.grid(row=0,
                    column=10,
                    sticky="n",
                    columnspan=3)

review_frontend()

####################################################################################################################################

#Change Themes Frame 1:
button_red = Button(frame1, text="Change to Pink", command=lambda: themes_1(frame1,
                                                                        "#ffb3c6",
                                                                        "#ffe5ec",
                                                                        fg="black",
                                                                        listbox_color="#ff87ab",
                                                                        entry_color="#ffb8d1"))
button_red.grid(row=30, column=30)

button_blue = Button(frame1, text="Change to Blue", command=lambda: themes_1(frame1,
                                                                         "#75d3eb",
                                                                         "#a4dcf4",
                                                                         fg="black",
                                                                         listbox_color="#8eecf5",
                                                                         entry_color="#98f5e1"))
button_blue.grid(row=31, column=30)

####################################################################################################################################

#Home Page
pro_bo_heading = Label(frame2,
                       text="Welcome to Pro Bo!",
                       font=("Arial", 15),
                       borderwidth=1,
                       relief="solid")
pro_bo_heading.grid(row=1,
                    column=1,
                    columnspan=3,
                    sticky="nsew")

pro_bo_text = Label(frame2, text="""
Pro Bo is a study app that helps you study,
how you find this app useful. It is a free app,
and you can use it for free. Furthermore, if you
have any questions or suggestions, please contact
me at 
mingl_2028@concordian.org
    Hope you find this app useful!    
""",
                    font=("Arial", 12),
                    borderwidth=1,
                    relief="solid"
                    )
pro_bo_text.grid(row=2,
                 column=1,
                 columnspan=3,
                 sticky="nsew",
                 padx=500,
                 pady=10)

####################################################################################################################################

button_red = Button(frame2, text="Change to Pink", command=lambda: themes_1(frame2,

                                                                        "#ffb3c6",
                                                                        "#ffe5ec",
                                                                        fg="black",
                                                                        listbox_color="#ff87ab",
                                                                        entry_color="#ffb8d1"))
button_red.grid(row=5, column=3)

button_blue = Button(frame2, text="Change to Blue", command=lambda: themes_1(frame2,
                                                                         "#75d3eb",
                                                                         "#a4dcf4",
                                                                         fg="black",
                                                                         listbox_color="#8eecf5",
                                                                         entry_color="#98f5e1"))
button_blue.grid(row=6,
                 column=3,
                 padx=100,
                 pady=100)

#Habit Trainer TKINTER
habit_check_button = Button(frame2, text="Check Habit", command=check)
habit_check_button.grid(row=4, column=1)

habit_add_button = Button(frame2, text="Add Habit", command=create_habit_frontend)
habit_add_button.grid(row=5, column=1)

habit_listbox = Listbox(frame2,
                        width=10,
                        height=15,
                        font=("Arial", 16),
                        )
habit_listbox.grid(row=5,
                   column=1,
                   rowspan=15,
                   sticky="nsew")
for i in habit_trainer_files:
    habit_listbox.insert(END,i)
habit_listbox.grid(row=4,
                   column=1,
                   sticky="nsew")




habit_button = Button(frame2, text="check", command=check)
habit_button.grid(row=5, column=2)


#TODO : Create a function to check habit with just 1 click

root.title("Flashcard Feature")
root.geometry("1300x650")
root.configure(bg="#FFFFFF")
root.mainloop()