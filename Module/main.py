import os
from tkinter import *
from tkinter import ttk
import customtkinter as ctk

from flashcard import Flashcard
from habit import Habit
from timer import Timer

class Probo(Timer, Flashcard, Habit):
    def __init__(self):
        super().__init__()

        # ----- UI State ----- #
        self.populate_tree = None
        self.root         = None
        self.shop_window  = None
        self.coin_label   = None

        # ----- Page Frames (named with _tab/_frame suffix to avoid class name collision) ----- #
        self.home_frame      = None
        self.flashcard_tab   = None   # NOT self.flashcard — that would shadow Flashcard methods
        self.shop_frame      = None   # NOT self.shop      — that would shadow Shop methods
        self.timer_frame     = None   # NOT self.timer     — that would shadow Timer methods
        self.settings_frame  = None

        # ----- Shared UI refs ----- #
        self.display      = None
        self.stacking_frame   = None
        self.habit_create_frame = None

        # ----- Flashcard sub-frames ----- #
        self.flashcard_review_frame              = None
        self.flashcard_edit_frame                = None
        self.flashcard_add_folder_and_file_frame = None
        self.flashcard_add_file_frame            = None
        self.flashcard_rename_frame              = None

    # ----- Main UI ----- #
    def main(self):
        """Main application entry point."""
        self.initialize_currency()
        self.initialize_inventory()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        root = self.root

        root.title("Pro Bo")
        self.center_window(root, 1200, 800)

        container = ctk.CTkFrame(root)
        container.pack(fill="both", expand=True)

        menubar = Menu(root)
        root.config(menu=menubar)

        pages = {
            "Home":       ctk.CTkFrame(container),
            "Flashcards": ctk.CTkFrame(container),
            "Shop":       ctk.CTkFrame(container),
            "Timer":      ctk.CTkFrame(container),
            "Settings":   ctk.CTkFrame(container),
        }

        self.home_frame     = pages["Home"]
        self.flashcard_tab  = pages["Flashcards"]
        self.shop_frame     = pages["Shop"]
        self.timer_frame    = pages["Timer"]
        self.settings_frame = pages["Settings"]

        for p in pages.values():
            p.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.home_frame.grid_columnconfigure(0, weight=0)
        self.home_frame.grid_columnconfigure(3, weight=1)
        self.home_frame.grid_rowconfigure(0, weight=0)
        self.home_frame.grid_rowconfigure(1, weight=1)

        def show_page(name):
            pages[name].tkraise()

        show_page("Home")

        # ===== HOME PAGE ===== #
        list_frame = ctk.CTkFrame(self.home_frame)
        list_frame.grid(row=0, column=0, columnspan=3, rowspan=2, sticky="nsew")

        # Welcome panel
        welcome_frame = ctk.CTkFrame(self.home_frame)
        welcome_frame.grid(row=0, column=3, sticky="nsew")
        welcome_frame.grid_columnconfigure(0, weight=1)

        welcome_heading = ctk.CTkLabel(welcome_frame, text="Welcome to Pro Bo!", font=self.TITLE_FONT)
        welcome_heading.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.coin_label = ctk.CTkLabel(
            welcome_frame,
            text=f"Current Coins: {self.get_current_coins()}",
            font=self.TITLE_FONT
        )
        self.coin_label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text=(
                "Productivity Booster or known as Pro Bo is a study app that helps you study better.\n"
                "Pro Bo is aimed for students but it is useful to all people.\n\n"
                "Version 1 contains Flashcards, Habits, Shop with boosters, and a Timer.\n"
                "Contact: mingl_2028@concordian.org"
            ),
            font=self.REGULAR_FONT
        )
        welcome_text.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5)

        # Stacking frame (right side, row 1)
        self.stacking_frame = ctk.CTkFrame(self.home_frame)
        self.stacking_frame.grid(row=1, column=3, sticky="nsew")
        self.stacking_frame.grid_columnconfigure(0, weight=1)
        self.stacking_frame.grid_rowconfigure(0, weight=1)

        self.habit_create_frame = ctk.CTkFrame(self.stacking_frame)
        self.habit_create_frame.grid(row=0, column=0, sticky="nsew")

        # ----- Habit listbox ----- #
        available_habit_label = ctk.CTkLabel(list_frame, text="Your daily habits", font=self.TITLE_FONT)
        available_habit_label.grid(row=0, column=0, sticky="nsew", columnspan=3)

        habit_listbox = Listbox(list_frame, width=25, height=15, font=self.REGULAR_FONT)
        for i in self.habit_trainer_files:
            habit_listbox.insert(END, i)
        habit_listbox.grid(row=1, column=0, columnspan=2, sticky="nsw", padx=5)

        habit_scroll = ctk.CTkScrollbar(list_frame, orientation="vertical", command=habit_listbox.yview)
        habit_scroll.grid(row=1, column=2, sticky="ns")
        habit_listbox.config(yscrollcommand=habit_scroll.set)

        # Habit menu
        habit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Habit", menu=habit_menu)
        habit_menu.add_command(label="Check Habit",  command=lambda: self.on_check(habit_listbox))
        habit_menu.add_command(label="Create Habit", command=lambda: (
            self.create_habit_frontend(self.habit_create_frame),
            self.habit_create_frame.tkraise()
        ))
        habit_menu.add_command(label="Delete Habit", command=lambda: self.delete_habit(habit_listbox))

        # ----- Flashcard stacked frames ----- #
        self.flashcard_rename_frame = ctk.CTkFrame(self.stacking_frame)
        self.flashcard_rename_frame.grid(row=0, column=0, sticky="nsew")

        self.flashcard_add_folder_and_file_frame = ctk.CTkFrame(self.stacking_frame)
        self.flashcard_add_folder_and_file_frame.grid(row=0, column=0, sticky="nsew")

        self.flashcard_add_file_frame = ctk.CTkFrame(self.stacking_frame)
        self.flashcard_add_file_frame.grid(row=0, column=0, sticky="nsew")

        self.flashcard_edit_frame = ctk.CTkFrame(self.stacking_frame)
        self.flashcard_edit_frame.grid(row=0, column=0, sticky="nsew")

        self.flashcard_review_frame = ctk.CTkFrame(self.stacking_frame)
        self.flashcard_review_frame.grid(row=0, column=0, sticky="nsew")

        # Flashcard menu
        flashcard_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Flashcard", menu=flashcard_menu)
        flashcard_menu.add_command(label="Rename",
                                   command=lambda: (show_page("Home"), self.open_rename(), self.apply_theme(self.flashcard_rename_frame, self.load_theme_preference())))

        flashcard_menu.add_command(label="Add Folder and File",
                                   command=lambda: (show_page("Home"), self.add_folder_and_file(), self.apply_theme(self.flashcard_add_folder_and_file_frame, self.load_theme_preference())))

        flashcard_menu.add_command(label="Add File",
                                   command=lambda: (show_page("Home"), self.add_file(), self.apply_theme(self.flashcard_add_file_frame, self.load_theme_preference())))

        flashcard_menu.add_command(label="Edit Flashcard",
                                   command=lambda: (show_page("Home"), self.edit_flashcard_frontend(self.display), self.apply_theme(self.flashcard_edit_frame, self.load_theme_preference())))

        flashcard_menu.add_command(label="Review",
                                   command=lambda: (show_page("Home"), self.review_frontend(), self.apply_theme(self.flashcard_review_frame, self.load_theme_preference())))
        # Shop menu
        shop_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Shop", menu=shop_menu)
        shop_menu.add_command(label="Open Inventory", command=lambda: self.open_inventory())
        shop_menu.add_command(label="Buy Powerups",   command=lambda: self.select_powerup())

        # ----- Flashcard folder tree ----- #
        # LINE ~174 CHANGED: replaced plain Listbox with ttk.Treeview (expandable folders)
        heading1 = ctk.CTkLabel(list_frame, text="Available Flashcards", font=self.TITLE_FONT)
        heading1.grid(row=2, column=0, columnspan=3)

        display = ttk.Treeview(list_frame, show="tree", height=15, selectmode="browse")
        display.column("#0", width=230)
        display.grid(row=3, column=0, sticky="nsw", padx=5, columnspan=2)

        scrollbar = ctk.CTkScrollbar(list_frame, orientation="vertical", command=display.yview)
        scrollbar.grid(row=3, column=2, rowspan=10, sticky="nsw", pady=5)
        display.config(yscrollcommand=scrollbar.set)
        self.display = display

        def populate_tree():
            """Clear and reload the treeview from the disk."""
            for item in display.get_children():
                display.delete(item)
            if os.path.exists(self.flashcard_folder_path):
                folders = sorted([
                    f for f in os.listdir(self.flashcard_folder_path)
                    if os.path.isdir(os.path.join(self.flashcard_folder_path, f))])
                if not folders:
                    display.insert("", END, text="No flashcards yet!")
                else:
                    for folder in folders:
                        folder_id = display.insert("", END, text="📁 " + folder, open=False)
                        folder_path = os.path.join(self.flashcard_folder_path, folder)
                        for fname in sorted(os.listdir(folder_path)):
                            if fname.endswith(".json"):
                                display.insert(folder_id, END, text="📄 " + fname[:-5])

        populate_tree()
        self.populate_tree = populate_tree  # stored so update_listbox can refresh the tree

        root.update_idletasks()

        # ----- Timer Frame ----- #
        timer_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Timer", menu=timer_menu)
        timer_menu.add_command(label="Focus", command=lambda: self.main_timer())

        # ===== SETTINGS TAB ===== #
        theme_frame_settings = self.create_theme_buttons(
            self.settings_frame,
            self.flashcard_tab,
            self.home_frame,
            self.shop_frame,
            self.timer_frame
        )
        theme_frame_settings.grid(row=2, column=0, padx=20, pady=20, sticky="nwes")

        theme_label = ctk.CTkLabel(self.settings_frame, text="Theme", font=self.REGULAR_FONT)
        theme_label.grid(row=1, column=0, sticky="nwe", padx=20, pady=20)

        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.settings_frame.grid_rowconfigure(0, weight=0)

        self.create_theme_menu(
            menubar,
            self.flashcard_tab,
            self.home_frame,
            self.shop_frame,
            self.settings_frame,
            self.timer_frame
        )


        # ----- Apply saved theme across all tabs ----- #
        saved_theme = self.load_theme_preference()
        for tab in (self.flashcard_tab, self.home_frame, self.shop_frame, self.settings_frame, self.timer_frame):
            self.apply_theme(tab, saved_theme)

        root.update_idletasks()
        self.neutralize_button_highlight(root)
        self.habit_listbox_checked(self.habit_trainer_files, self.habit_trainer_folder_path, habit_listbox)
        habit_listbox.config(fg="black", font=("Arial", 13, "bold"))
        root.mainloop()

if __name__ == "__main__":
    app = Probo()
    app.main()
