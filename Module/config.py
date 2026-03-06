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
        self.THEME_PREFERENCE_FILE = os.path.join(os.getcwd(), "theme_preference.json")

        self.TIMESTAMP_FORMAT = "%Y-%m-%d"

        self.POWER_UPS = """
            1. Habit Revive: Revives a broken habit streak (50 Coins)
            2. Double Coins: Double reward for next review session (25 Coins)
            3. Combo Multiplier (review): Get 30 coins immediately when getting 10 correct answers in a row (15 Coins)    
        """

        # ----- Theme Configurations ----- #
        self.THEMES = {
            "pink": {
                "frame_bg": "#FFD6E8",
                "ctrl_bg": "#FFE5F0",
                "fg": "#8B0045",
                "listbox_color": "#FFB8D9",
                "entry_color": "#FFFFFF",
                "button_bg": "#FF1493",
                "button_hover": "#C71585",
                "button_fg": "#FFFFFF"
            },
            "blue": {
                "frame_bg": "#B8E6FF",
                "ctrl_bg": "#D4F1FF",
                "fg": "#003D5C",
                "listbox_color": "#7DD3FC",
                "entry_color": "#FFFFFF",
                "button_bg": "#0EA5E9",
                "button_hover": "#0284C7",
                "button_fg": "#FFFFFF"
            },
            "white": {
                "frame_bg": "#F5F5F5",
                "ctrl_bg": "#FFFFFF",
                "fg": "#1F2937",
                "listbox_color": "#E5E7EB",
                "entry_color": "#FFFFFF",
                "button_bg": "#4B5563",
                "button_hover": "#374151",
                "button_fg": "#FFFFFF"
            },
            "green": {
                "frame_bg": "#9AFF82",
                "ctrl_bg": "#B4FFA1",
                "fg": "#111111",
                "listbox_color": "#94FFB2",
                "entry_color": "#FFFFFF",
                "button_bg": "#00781C",
                "button_hover": "#06691F",
                "button_fg": "#FFFFFF"
            },
            "purple": {
                "frame_bg": "#D9B3FF",
                "ctrl_bg": "#ECB9FF",
                "fg": "#6B21A8",
                "listbox_color": "#C0B6FD",
                "entry_color": "#FFFFFF",
                "button_bg": "#8B5CF6",
                "button_hover": "#7C3AED",
                "button_fg": "#FFFFFF"
            },
            "yellow": {
                "frame_bg": "#FFFF99",
                "ctrl_bg": "#FFFFCC",
                "fg": "#996600",
                "listbox_color": "#FFE29D",
                "entry_color": "#FFE309",
                "button_bg": "#FFCC00",
                "button_hover": "#CC9900",
                "button_fg": "#000000"
            }
        }

        self.CTK_APPEARANCE_MODES = {
            "pink": "light",
            "blue": "light",
            "white": "light",
            "green": "light",
            "purple": "light",
            "yellow": "light"
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
