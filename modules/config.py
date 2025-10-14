import os

# File Paths
flashcard_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Flashcards Files"
habit_trainer_folder_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project\Habit Trainer"
personal_project_file_path = r"D:\PyCharm 2025.2.1\Pythonfiles\Personal Project"

# Get file lists
flashcard_files = os.listdir(flashcard_folder_path)
habit_trainer_files = os.listdir(habit_trainer_folder_path)

# Timestamp format
TIMESTAMP_FORMAT = "%Y-%m-%d"

# Theme preference file
THEME_PREFERENCE_FILE = os.path.join(os.path.dirname(__file__), "..", "theme_preference.json")

# Theme configuration
THEMES = {
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
    }
}