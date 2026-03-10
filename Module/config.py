import os

class Config:
    def __init__(self):
        # ----- Font Size ----- #
        self.TITLE_FONT = ("Arial", 20, "bold")
        self.SUBTITLE_FONT = ("Arial", 15, "bold")
        self.REGULAR_FONT = ("Arial", 13)
        self.DROPDOWN_FONT = ("Arial", 8)

        # ----- Folder Names ----- #
        self.flashcard_folder = "Flashcards Files"
        self.habit_folder = "Habit Trainer"
        self.game_folder = "Game"

        # ----- File Paths ----- #
        self.current_directory = os.getcwd()
        self.flashcard_folder_path = os.path.join(self.current_directory, self.flashcard_folder)
        self.habit_trainer_folder_path = os.path.join(self.current_directory, self.habit_folder)
        self.game_folder_path = os.path.join(self.current_directory, self.game_folder)

        currency_file_name = "current_currency.txt"
        self.combined_path = os.path.join(self.game_folder, currency_file_name)
        self.inventory_path = os.path.join(self.game_folder, "inventory.json")

        # FIX: use getcwd() so the path always exists
        self.THEME_PREFERENCE_FILE = os.path.join(os.getcwd(), "../theme_preference.json")

        self.TIMESTAMP_FORMAT = "%Y-%m-%d"

        self.POWER_UPS = """
            1. Habit Revive: Revives a broken habit streak (50 Coins)
            2. Double Coins: Earn (correct - wrong) x5 coins after each review session (50 Coins)
            3. Combo Multiplier: Get 10 coins for every 5 correct answers in a row,
               20 coins for the next 5 in the same session (15 Coins)
        """
        # ----- Theme Configurations ----- #
        self.THEMES = {
            "pink": {
                "frame_bg": "#FFE4F0",
                "ctrl_bg": "#FFF0F7",
                "fg": "#000000",
                "listbox_color": "#FFB8D9",
                "entry_color": "#FFFFFF",
                "button_bg": "#E91E8C",
                "button_hover": "#C71585",
                "button_fg": "#FFFFFF"
            },
            "blue": {
                "frame_bg": "#DAEEFF",
                "ctrl_bg": "#EEF7FF",
                "fg": "#000000",
                "listbox_color": "#A8D8F0",
                "entry_color": "#FFFFFF",
                "button_bg": "#0078D4",
                "button_hover": "#005A9E",
                "button_fg": "#FFFFFF"
            },
            "white": {
                "frame_bg": "#F0F0F0",
                "ctrl_bg": "#FAFAFA",
                "fg": "#000000",
                "listbox_color": "#E0E0E0",
                "entry_color": "#FFFFFF",
                "button_bg": "#333333",
                "button_hover": "#111111",
                "button_fg": "#FFFFFF"
            },
            "green": {
                "frame_bg": "#C8F5C0",
                "ctrl_bg": "#E4FAE0",
                "fg": "#000000",
                "listbox_color": "#A0E890",
                "entry_color": "#FFFFFF",
                "button_bg": "#2E7D32",
                "button_hover": "#1B5E20",
                "button_fg": "#FFFFFF"
            },
            "purple": {
                "frame_bg": "#EDD9FF",
                "ctrl_bg": "#F7F0FF",
                "fg": "#000000",
                "listbox_color": "#D4AAFF",
                "entry_color": "#FFFFFF",
                "button_bg": "#7B2FBE",
                "button_hover": "#5C1A9E",
                "button_fg": "#FFFFFF"
            },
            "yellow": {
                "frame_bg": "#FFF9C4",
                "ctrl_bg": "#FFFDE7",
                "fg": "#000000",
                "listbox_color": "#FFF176",
                "entry_color": "#FFFFFF",
                "button_bg": "#F9A800",
                "button_hover": "#C97F00",
                "button_fg": "#FFFFFF"
            },
            "orange": {
                "frame_bg": "#FFD0A0",
                "ctrl_bg": "#FFE4C4",
                "fg": "#000000",
                "listbox_color": "#FFBA70",
                "entry_color": "#FFFFFF",
                "button_bg": "#FF8C00",
                "button_hover": "#E07800",
                "button_fg": "#FFFFFF"
            }
        }

        self.CTK_APPEARANCE_MODES = {
            "pink": "light",
            "blue": "light",
            "white": "light",
            "green": "light",
            "purple": "light",
            "yellow": "light",
            "orange": "light"
        }

        self.check_path(self.flashcard_folder_path, self.habit_trainer_folder_path, self.game_folder_path)

        self.flashcard_files = os.listdir(self.flashcard_folder_path)
        self.habit_trainer_files = os.listdir(self.habit_trainer_folder_path)

    @staticmethod
    def check_path(flashcard_folder_path, habit_trainer_folder_path, game_folder_path):
        if not os.path.exists(flashcard_folder_path):
            os.makedirs(flashcard_folder_path, exist_ok=True)
        if not os.path.exists(habit_trainer_folder_path):
            os.makedirs(habit_trainer_folder_path, exist_ok=True)
        if not os.path.exists(game_folder_path):
            os.makedirs(game_folder_path, exist_ok=True)

    @staticmethod
    def check_empty(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
            return not content

    @staticmethod
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int(screen_width / 2) - (width / 2)
        center_y = int(screen_height / 2) - (height / 2)
        window.geometry(f'{width}x{height}+{int(center_x)}+{int(center_y)}')
