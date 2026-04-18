import os
import json
from tkinter import END, Listbox, TclError
from tkinter import messagebox
import customtkinter as ctk

from shop import Shop
from theme import Theme
from config import Config

class Flashcard:
    def __init__(self, shop: Shop, theme: Theme, config: Config):
        super().__init__(config, theme)
        self.shop = shop
        self.config = config
        self.theme = theme
        # FIX: renamed from self.flashcard to self.flashcard_tab to avoid
        # overwriting the Flashcard class methods via instance attribute shadowing
        self.parent = None
        self.folder_raw = None
        self.flashcard_tab = None
        self.display = None
        self.data_store = None   # renamed from self.data to avoid any confusion
        self.answer = None
        self.item_selection = None
        self.add_btn = None
        self.flashcard_review_frame = None
        self.flashcard_edit_frame = None
        self.flashcard_add_folder_and_file_frame = None
        self.flashcard_add_file_frame = None
        self.flashcard_rename_frame = None

    # ----- Listing Functions ----- #
    def no_list_files(self, folder_name):
        """List files in a folder if it exists."""
        file_path = os.path.join(self.config.flashcard_folder_path, folder_name)
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Invalid input. Please enter a valid folder name.")
            return
        list_file = os.listdir(file_path)
        if folder_name in self.config.flashcard_files:
            messagebox.showinfo("Info Dialog", f"Files in folder: {list_file}")
        else:
            messagebox.showerror("Error", "Please enter a valid folder name.")

    def yes_list_files(self, folder_name):
        """Check if the folder exists and list flashcard files."""
        if folder_name in self.config.flashcard_files:
            messagebox.showerror("Error", "Folder already exists. Please enter a different name.")
        else:
            messagebox.showinfo("Info Dialog", str(self.config.flashcard_files))

    # ----- Edit Flashcard Functions ----- #
    def add_card(self, file_name, folder_name, frame, edit_listbox=None):
        """Add a flashcard to a file."""
        add_card_file_path = os.path.join(self.config.flashcard_folder_path, folder_name, file_name)

        self.data_store = {}
        if os.path.exists(add_card_file_path):
            with open(add_card_file_path, "r") as d:
                try:
                    loaded = json.load(d)
                    if isinstance(loaded, dict):
                        self.data_store = loaded
                    else:
                        messagebox.showerror("Error", "Unsupported file format. Expected a JSON object.")
                        return
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Failed to load data. Starting fresh.")

        question_heading = ctk.CTkLabel(frame, text="Enter the question:", font=self.config.SUBTITLE_FONT)
        question_heading.grid(row=20, column=6, sticky="n")

        question = ctk.CTkEntry(frame, width=200, font=self.config.REGULAR_FONT)
        question.grid(row=21, column=6, sticky="n")
        question.focus_set()

        answer_heading = ctk.CTkLabel(frame, text="Enter the answer:", font=self.config.SUBTITLE_FONT)
        answer_heading.grid(row=22, column=6, sticky="n")

        self.answer = ctk.CTkEntry(frame, width=200, font=self.config.REGULAR_FONT)
        self.answer.grid(row=23, column=6, sticky="n")

        add_btn = ctk.CTkButton(
            frame,
            text="Add Card",
            command=lambda: self.on_add(question, self.answer, add_card_file_path, edit_listbox),
            width=100,
            hover=False,
            font=self.config.REGULAR_FONT
        )
        add_btn.grid(row=28, column=6, sticky="n", pady=5)

        question.bind("<Return>", lambda e: self.answer.focus_set())
        self.answer.bind("<Return>", lambda e: self.on_add(question, self.answer, add_card_file_path, edit_listbox))

        self.theme.apply_themes_to_all(frame)

    def on_add(self, question, answer, add_card_file_path, edit_listbox):
        """Handle adding a card."""
        q = question.get().strip()
        a = answer.get().strip()

        if not q or not a:
            messagebox.showerror("Error", "Both question and answer are required.")
            return

        self.data_store[q] = a

        try:
            with open(add_card_file_path, "w") as f:
                json.dump(self.data_store, f, indent=4)
        except OSError as t:
            messagebox.showerror("Error", f"Failed to save:\n{add_card_file_path}\n\n{t}")
            return

        edit_listbox.insert(END, f"{q}: {a}")
        question.delete(0, END)
        answer.delete(0, END)
        question.focus_set()

        self.theme.apply_themes_to_all(self.flashcard_tab)

    def edit_card(self, file_name, folder_name, item_selected, frame, edit_listbox):
        """Display edit inputs for the selected flashcard."""
        self.item_selection = edit_listbox.curselection()
        if not self.item_selection:
            return

        item_indices = self.item_selection[0]
        item_selected = edit_listbox.get(item_indices)

        parts = item_selected.split(":", 1)
        prefill_question = parts[0].strip()
        prefill_answer = parts[1].strip() if len(parts) > 1 else ""

        edit_question_heading = ctk.CTkLabel(frame, text="Edit the question:", font=self.config.SUBTITLE_FONT)
        edit_question_heading.grid(row=20, column=7, sticky="n", pady=5)

        edit_question = ctk.CTkEntry(frame, width=200)
        edit_question.grid(row=21, column=7, sticky="n", pady=5)
        edit_question.insert(0, prefill_question)
        edit_question.focus_set()

        edit_answer_heading = ctk.CTkLabel(frame, text="Edit the answer:", font=self.config.SUBTITLE_FONT)
        edit_answer_heading.grid(row=22, column=7, sticky="n", pady=5)

        edit_answer = ctk.CTkEntry(frame, width=200)
        edit_answer.grid(row=23, column=7, sticky="n", pady=5)
        edit_answer.insert(0, prefill_answer)

        edit_done_button = ctk.CTkButton(
            frame, text="Save Edit", width=100, font=self.config.REGULAR_FONT,
            command=lambda: self.edit_done(file_name, folder_name, edit_question, edit_answer, item_selected, edit_listbox)
        )
        edit_done_button.grid(row=28, column=7, sticky="n", pady=5)

        edit_question.bind("<Return>", lambda e: edit_answer.focus_set())
        edit_answer.bind("<Return>",
                         lambda e: self.edit_done(file_name, folder_name, edit_question, edit_answer, item_selected, edit_listbox))
        self.theme.apply_themes_to_all(frame)

    def edit_done(self, file_name, folder_name, edit_question, edit_answer, item_selected, edit_listbox):
        """Save edited flashcard."""
        target_file = f"{file_name}.json" if not file_name.lower().endswith(".json") else file_name
        final_file_path = os.path.join(self.config.flashcard_folder_path, folder_name, target_file)

        with open(final_file_path, "r") as f:
            data = json.load(f)

        new_question = edit_question.get().strip() if hasattr(edit_question, "get") else str(edit_question).strip()
        new_answer   = edit_answer.get().strip()   if hasattr(edit_answer,   "get") else str(edit_answer).strip()

        if not new_question or not new_answer:
            messagebox.showerror("Error", "Both question and answer are required.")
            return

        original_question = item_selected.split(":", 1)[0].strip()

        if original_question not in data:
            messagebox.showerror("Error", f"Original flashcard not found: '{original_question}'.")
            return

        if new_question == original_question:
            data[original_question] = new_answer
        else:
            del data[original_question]
            data[new_question] = new_answer

        with open(final_file_path, "w") as f:
            json.dump(data, f, indent=4)

        edit_listbox.delete(0, END)
        for k, v in data.items():
            edit_listbox.insert(END, f"{k}: {v}")

        messagebox.showinfo("Saved!", "Flashcard edited successfully.")

    @staticmethod
    def on_select(_, file_name, folder_name, flashcard_tab, edit_card, edit_listbox):
        item_selection = edit_listbox.curselection()
        if item_selection:
            item_indices = item_selection[0]
            item_selected = edit_listbox.get(item_indices)
            edit_card(file_name, folder_name, item_selected, flashcard_tab, edit_listbox)
    def edit_flashcard_cl(self, file_name, folder_name):
        """Load flashcards for editing."""
        self.theme.apply_themes_to_all(self.flashcard_edit_frame)

        json_file_name = f"{file_name.lower()}.json"
        folder_name    = folder_name.lower()
        final_file_path = os.path.join(self.config.flashcard_folder_path, folder_name, json_file_name)

        edit_frame = ctk.CTkFrame(self.flashcard_edit_frame)
        edit_frame.grid(row=2, column=6, rowspan=15, columnspan=3, sticky="nsew")
        edit_frame.grid_rowconfigure(0, weight=1)
        edit_frame.grid_columnconfigure(0, weight=1)

        edit_listbox = Listbox(edit_frame, width=80, height=10)
        edit_listbox.grid(row=0, column=0, sticky="nsw")

        edit_scrollbar = ctk.CTkScrollbar(edit_frame, orientation='vertical', command=edit_listbox.yview)
        edit_scrollbar.grid(row=0, column=1, sticky="nsw")
        edit_listbox.config(yscrollcommand=edit_scrollbar.set)
        edit_listbox.delete(0, END)

        try:
            with open(final_file_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found:\n{final_file_path}")
            return
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Invalid JSON:\n{final_file_path}\n\n{e}")
            return
        except OSError as e:
            messagebox.showerror("Error", f"Could not open file:\n{final_file_path}\n\n{e}")
            return

        if isinstance(data, dict):
            for key, value in data.items():
                edit_listbox.insert(END, f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                edit_listbox.insert(END, str(item))
        else:
            edit_listbox.insert(END, str(data))

        add_heading = ctk.CTkLabel(self.flashcard_edit_frame, text="Add", font=self.config.SUBTITLE_FONT)
        add_heading.grid(row=19, column=6, sticky="s")
        self.add_card(json_file_name, folder_name, self.flashcard_edit_frame, edit_listbox)

        edit_heading = ctk.CTkLabel(self.flashcard_edit_frame, text="Edit", font=self.config.SUBTITLE_FONT)
        edit_heading.grid(row=19, column=7, sticky="s")

        edit_listbox.bind(
            "<<ListboxSelect>>",
            lambda event: self.on_select(
                event, json_file_name, folder_name, self.flashcard_edit_frame, self.edit_card, edit_listbox
            )
        )
        self.theme.neutralize_button_highlight(self.flashcard_edit_frame)

    def edit_flashcard_frontend(self, display):
        for w in self.flashcard_edit_frame.winfo_children(): w.destroy()

        """Create edit flashcards interface.
        LINES CHANGED: self.display is now a ttk.Treeview, so selection reading
        uses display.focus() / display.parent() instead of curselection()/get().
        Clicking a FILE node autofills both folder and file entries.
        Clicking a FOLDER node fills only the folder entry."""

        folder_name_heading = ctk.CTkLabel(
            self.flashcard_edit_frame, text="Select Folder Name:", font=self.config.SUBTITLE_FONT
        )
        folder_name_heading.grid(row=0, column=0, sticky="n")

        folder_name_entry = ctk.CTkEntry(self.flashcard_edit_frame, width=200)
        folder_name_entry.grid(row=1, column=0, sticky="nsew")
        folder_name_entry.focus_set()

        file_name_heading = ctk.CTkLabel(self.flashcard_edit_frame, text="Select File Name:", font=self.config.SUBTITLE_FONT)
        file_name_heading.grid(row=2, column=0, sticky="n")

        file_name_entry = ctk.CTkEntry(self.flashcard_edit_frame)
        file_name_entry.grid(row=3, column=0, sticky="nsew")

        # Pre-fill if something is already selected in the tree
        selected = display.focus()
        if selected:
            parent = display.parent(selected)
            raw = display.item(selected, "text").lstrip("📁📄 ")
            if parent:  # it's a file node
                folder_raw = display.item(parent, "text").lstrip("📁 ")
                folder_name_entry.insert(0, folder_raw)
                file_name_entry.insert(0, raw)
            else:       # it's a folder node
                folder_name_entry.insert(0, raw)

        def on_tree_select(_):
            """Autofill entries when the user clicks a node in the treeview."""
            node = self.display.focus()
            if not node:
                return
            parents = self.display.parent(node)
            raw_text = self.display.item(node, "text").lstrip("📁📄 ")
            folder_name_entry.delete(0, END)
            file_name_entry.delete(0, END)
            if parents:  # file node — fill both
                folder_raww = self.display.item(parents, "text").lstrip("📁 ")
                folder_name_entry.insert(0, folder_raww)
                file_name_entry.insert(0, raw_text)
            else:       # folder node — fill folder only
                folder_name_entry.insert(0, raw_text)

        # LINE CHANGED: bind Treeview select event instead of ListboxSelect
        self.display.bind("<<TreeviewSelect>>", on_tree_select)

        file_name_submit = ctk.CTkButton(
            self.flashcard_edit_frame,
            text="Open Flashcard",
            command=lambda: self.edit_flashcard_cl(file_name_entry.get(), folder_name_entry.get())
        )
        file_name_submit.grid(row=6, column=0, sticky="n")

        folder_name_entry.bind("<Return>", lambda e: file_name_entry.focus_set())
        file_name_entry.bind("<Return>",
                             lambda e: self.edit_flashcard_cl(file_name_entry.get(), folder_name_entry.get()))

        self.theme.apply_theme(self.flashcard_edit_frame, self.theme.load_theme_preference())
        self.flashcard_edit_frame.tkraise()
        self.theme.neutralize_button_highlight(self.flashcard_edit_frame)
    # ----- Rename Functions ----- #
    def rename_folder(self, input_old_folder, input_new_folder):
        """Rename a flashcard folder."""
        input_old_folder_name = input_old_folder.get()
        input_new_folder_name = input_new_folder.get()

        old_path = os.path.join(self.config.flashcard_folder_path, input_old_folder_name)
        new_path = os.path.join(self.config.flashcard_folder_path, input_new_folder_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            self.config.flashcard_files = os.listdir(self.config.flashcard_folder_path)
            messagebox.showinfo("Info Dialog", f"Folder '{input_old_folder_name}' renamed to '{input_new_folder_name}'.")
        else:
            messagebox.showerror("Error", "Invalid input. Please enter a valid folder name!")

    def open_rename(self):
        """Create a rename folder interface."""
        for w in self.flashcard_rename_frame.winfo_children(): w.destroy()

        heading_rename1 = ctk.CTkLabel(self.flashcard_rename_frame, text="Old Folder Name:", font=self.config.SUBTITLE_FONT)
        heading_rename1.grid(row=1, column=0, sticky="n")

        heading_rename2 = ctk.CTkLabel(self.flashcard_rename_frame, text="New Folder Name:", font=self.config.SUBTITLE_FONT)
        heading_rename2.grid(row=3, column=0, sticky="n")

        input_old_folder = ctk.CTkEntry(self.flashcard_rename_frame)
        input_old_folder.grid(row=2, column=0, sticky="n")
        input_old_folder.focus_set()

        input_new_folder = ctk.CTkEntry(self.flashcard_rename_frame)
        input_new_folder.grid(row=4, column=0, sticky="n")

        def on_display_select(_):
            # LINE CHANGED: Treeview selection for rename — always resolve to folder name
            node = self.display.focus()
            if not node:
                return
            parent = self.display.parent(node)
            raw = self.display.item(node, "text").lstrip("📁📄 ")
            input_old_folder.delete(0, END)
            if parent:
                input_old_folder.insert(0, self.display.item(parent, "text").lstrip("📁 "))
            else:
                input_old_folder.insert(0, raw)

        self.display.bind("<<TreeviewSelect>>", on_display_select)

        rename_submit = ctk.CTkButton(
            self.flashcard_rename_frame,
            text="Rename Folder",
            command=lambda: [
                self.rename_folder(input_old_folder, input_new_folder),
                self.update_listbox(self.display),
                input_old_folder.delete(0, END),
                input_new_folder.delete(0, END),
                self.flashcard_rename_frame.lower()
            ]
        )
        rename_submit.grid(row=5, column=0, sticky="n")

        input_old_folder.bind("<Return>", lambda e: input_new_folder.focus_set())
        input_new_folder.bind("<Return>", lambda e: [
            self.rename_folder(input_old_folder, input_new_folder),
            self.update_listbox(self.display),
            input_old_folder.delete(0, END),
            input_new_folder.delete(0, END),
            self.flashcard_rename_frame.lower()
        ])
        self.theme.apply_theme(self.flashcard_rename_frame, self.theme.load_theme_preference())
        self.flashcard_rename_frame.tkraise()


    # ----- Add Folder and File Feature ----- #
    def create_file(self, folder_name, file_name):
        file_path = os.path.join(self.config.flashcard_folder_path, folder_name, f"{file_name}.json")
        if not os.path.exists(os.path.dirname(file_path)):
            messagebox.showerror("Error", f"Folder '{folder_name}' does not exist.")
            return
        with open(file_path, "w") as f:
            json.dump({}, f)

    def create_folder_and_file(self, folder_name, file_name):
        """Create both a folder and a flashcard file."""
        folder_path = os.path.join(self.config.flashcard_folder_path, folder_name)
        if os.path.exists(folder_path):
            messagebox.showerror("Error", f"Folder '{folder_name}' already exists.")
            return
        os.mkdir(folder_path)
        self.create_file(folder_name, file_name)
        messagebox.showinfo("Info Dialog", f"Folder '{folder_name}' created successfully.")

    def add_folder_and_file(self):
        for w in self.flashcard_add_folder_and_file_frame.winfo_children(): w.destroy()

        """Handle folder and file creation."""
        folder_name_heading = ctk.CTkLabel(
            self.flashcard_add_folder_and_file_frame, text="Enter the folder name:", font=self.config.SUBTITLE_FONT
        )
        folder_name_heading.grid(row=0, column=0, sticky="n", padx=10)

        folder_name = ctk.CTkEntry(self.flashcard_add_folder_and_file_frame, width=200)
        folder_name.grid(row=1, column=0, sticky="n")
        folder_name.focus_set()

        file_name_heading = ctk.CTkLabel(
            self.flashcard_add_folder_and_file_frame, text="Enter the file name:", font=self.config.SUBTITLE_FONT
        )
        file_name_heading.grid(row=2, column=0, sticky="n", padx=10)

        file_name_entry = ctk.CTkEntry(self.flashcard_add_folder_and_file_frame, width=200)
        file_name_entry.grid(row=3, column=0, sticky="n")

        file_name_submit = ctk.CTkButton(
            self.flashcard_add_folder_and_file_frame,
            text="Create Folder and File",
            command=lambda: [
                self.create_folder_and_file(folder_name.get(), file_name_entry.get()),
                self.update_listbox(self.display),
                self.flashcard_add_folder_and_file_frame.lower()
            ]
        )
        file_name_submit.grid(row=4, column=0, sticky="n")

        folder_name.bind("<Return>", lambda e: file_name_entry.focus_set())
        file_name_entry.bind("<Return>", lambda e: [
            self.create_folder_and_file(folder_name.get(), file_name_entry.get()),
            self.update_listbox(self.display),
            self.flashcard_add_folder_and_file_frame.lower()
        ])

        self.theme.apply_theme(self.flashcard_add_folder_and_file_frame, self.theme.load_theme_preference())
        self.theme.apply_themes_to_all(self.flashcard_add_folder_and_file_frame)
        self.flashcard_add_folder_and_file_frame.tkraise()

    def add_file(self):
        for w in self.flashcard_add_file_frame.winfo_children(): w.destroy()

        """Handle file creation inside an existing folder."""
        folder_name_heading = ctk.CTkLabel(
            self.flashcard_add_file_frame, text="Enter the name of your folder: ", font=self.config.SUBTITLE_FONT
        )
        folder_name_heading.grid(row=0, column=0, sticky="n", padx=10)

        folder_name_input = ctk.CTkEntry(self.flashcard_add_file_frame, width=200)
        folder_name_input.grid(row=1, column=0, sticky="n")
        folder_name_input.focus_set()

        file_name_heading = ctk.CTkLabel(
            self.flashcard_add_file_frame, text="Enter the name for your flashcard file:", font=self.config.SUBTITLE_FONT
        )
        file_name_heading.grid(row=2, column=0, sticky="n")

        file_name = ctk.CTkEntry(self.flashcard_add_file_frame, width=200)
        file_name.grid(row=3, column=0, sticky="n")

        def on_display_select(_):
            # LINE CHANGED: Treeview selection — only fill if a folder node is picked
            node = self.display.focus()
            if not node:
                return
            parent = self.display.parent(node)
            raw = self.display.item(node, "text").lstrip("📁📄 ")
            folder_name_input.delete(0, END)
            if parent:  # file node — use its parent folder
                folder_name_input.insert(0, self.display.item(parent, "text").lstrip("📁 "))
            else:
                folder_name_input.insert(0, raw)

        self.display.bind("<<TreeviewSelect>>", on_display_select)

        file_name_submit = ctk.CTkButton(
            self.flashcard_add_file_frame,
            text="Create File",
            command=lambda: [
                self.create_file(folder_name_input.get(), file_name.get()),
                self.update_listbox(self.display),
                self.flashcard_add_file_frame.lower()
            ]
        )
        file_name_submit.grid(row=4, column=0, sticky="n")

        folder_name_input.bind("<Return>", lambda e: file_name.focus_set())
        file_name.bind("<Return>", lambda e: [
            self.create_file(folder_name_input.get(), file_name.get()),
            self.update_listbox(self.display),
            self.flashcard_add_file_frame.lower()
        ])

        self.theme.apply_theme(self.flashcard_add_file_frame, self.theme.load_theme_preference())
        self.flashcard_add_file_frame.tkraise()

    # ----- Review Functions ----- #
    def review_frontend(self):
        for w in self.flashcard_review_frame.winfo_children(): w.destroy()

        """Create the review interface."""
        folder_name_heading = ctk.CTkLabel(
            self.flashcard_review_frame, text="Enter the name of the folder:", font=self.config.SUBTITLE_FONT
        )
        folder_name_heading.grid(row=1, column=10, sticky="n")

        folder_name = ctk.CTkEntry(self.flashcard_review_frame)
        folder_name.grid(row=2, column=10, sticky="n")
        folder_name.focus_set()

        def on_display_select(_):
            # LINE CHANGED: Treeview selection — only fill if a folder node is picked
            node = self.display.focus()
            if not node:
                return
            parent = self.display.parent(node)
            raw = self.display.item(node, "text").lstrip("📁📄 ")
            folder_name.delete(0, END)
            if parent:  # file node — use its parent folder
                folder_name.insert(0, self.display.item(parent, "text").lstrip("📁 "))
            else:
                folder_name.insert(0, raw)

        self.display.bind("<<TreeviewSelect>>", on_display_select)

        file_name_heading = ctk.CTkLabel(
            self.flashcard_review_frame, text="Enter the name for your flashcard file:", font=self.config.SUBTITLE_FONT
        )
        file_name_heading.grid(row=3, column=10, sticky="n")

        file_name = ctk.CTkEntry(self.flashcard_review_frame)
        file_name.grid(row=4, column=10, sticky="n")

        file_name_submit = ctk.CTkButton(
            self.flashcard_review_frame, text="Start Review",
            command=lambda: self.review_listbox_backend(folder_name, file_name)
        )
        file_name_submit.grid(row=5, column=10, sticky="n")

        folder_name.bind("<Return>", lambda e: file_name.focus_set())
        file_name.bind("<Return>", lambda e: self.review_listbox_backend(folder_name, file_name))

        self.flashcard_review_frame.tkraise()

    def list_folder_files(self, folder_name):
        """List files in the specified folder."""
        file_path = os.path.join(self.config.flashcard_folder_path, folder_name)
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Folder not found.")
            return
        files = os.listdir(file_path)
        messagebox.showinfo("Info", f"Files in folder: {files}")

    def review_listbox_backend(self, folder_name, file_name):
        """Start the review quiz."""
        target_folder = folder_name.get()
        target_file   = f"{file_name.get()}.json"
        final_file_path = os.path.join(self.config.flashcard_folder_path, target_folder, target_file)

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

        question_heading = ctk.CTkLabel(self.flashcard_review_frame, text=f"1. : {items[0][0]}", font=self.config.SUBTITLE_FONT)
        question_heading.grid(row=8, column=10, sticky="n")

        question_entry = ctk.CTkEntry(self.flashcard_review_frame)
        question_entry.grid(row=9, column=10, sticky="n")
        question_entry.focus_set()
        question_entry.bind("<Return>", lambda event: self.question_check(question_entry, question_heading))

        question_submit = ctk.CTkButton(
            self.flashcard_review_frame, text="Check Answer",
            command=lambda: self.question_check(question_entry, question_heading)
        )
        question_submit.grid(row=10, column=10, sticky="n")

        saved_theme = self.theme.load_theme_preference()
        self.theme.apply_theme(self.flashcard_review_frame, saved_theme)

        question_heading.items      = items
        question_heading.idx        = 0
        question_heading.correct    = 0
        question_heading.wrong      = 0
        question_heading.submit_btn = question_submit
        question_heading.streak = 0
        question_heading.combo_count = 0

    def question_check(self, question_entry, question_heading):
        """Check the answer and move to the next question."""
        items   = getattr(question_heading, "items",  [])
        idx     = getattr(question_heading, "idx",     0)
        correct = getattr(question_heading, "correct", 0)
        wrong   = getattr(question_heading, "wrong",   0)
        streak  = getattr(question_heading, "streak",  0)
        combo_count = getattr(question_heading, "combo_count", 0)

        if not items:
            messagebox.showerror("Error", "No review state found.")
            return

        _, expected_answer = items[idx]
        user_answer = question_entry.get().strip()

        if user_answer == expected_answer:
            question_entry.delete(0, END)
            idx     += 1
            correct += 1
            streak  += 1
            question_heading.idx     = idx
            question_heading.correct = correct
            question_heading.streak  = streak

            if streak > 0 and streak % 5 == 0:
                inventory = self.get_inventory()
                if combo_count == 0 and inventory.get("Combo Multiplier", 0) >= 1:
                    self.remove_from_inventory("Combo Multiplier", 1)

                if combo_count >= 0 and (combo_count > 0 or inventory.get("Combo Multiplier", 0) >= 1):
                    combo_count += 1
                    question_heading.combo_count = combo_count
                    coins = 10 if combo_count == 1 else 20
                    self._save_coins(self.get_current_coins() + coins)
                    messagebox.showinfo("Combo!", f"{streak} in a row! +{coins} coins!")
                    self.update_coin_display()

            if idx < len(items):
                question_heading.configure(text=f"{idx + 1}. : {items[idx][0]}")
                question_entry.focus_set()
            else:
                total = len(items)
                messagebox.showinfo("Finished!",
                f"All questions completed!\nCorrect: {correct}, Wrong: {wrong}, Total: {total}")
                messagebox.showinfo("Results", f"Correct: {correct}, Wrong: {wrong}, Total: {total}")
                self.ask_after_review(correct, wrong)
                try:
                    submit_btn = getattr(question_heading, "submit_btn", None)
                    question_heading.destroy()
                    question_entry.destroy()
                    if submit_btn:
                        submit_btn.destroy()
                except TclError:
                    pass
        else:
            wrong += 1
            streak = 0
            question_heading.wrong = wrong
            question_heading.streak = streak
            if wrong > 5:
                messagebox.showinfo("Hint", f"The answer is {expected_answer}.")
            question_entry.delete(0, END)
            question_entry.focus_set()

    # ----- UI Helper ----- #
    def update_listbox(self, display):
        """Refresh the flashcard folder treeview.
        Because self.display is now a ttk.Treeview."""
        if hasattr(self, "populate_tree") and callable(self.populate_tree):
            self.populate_tree()