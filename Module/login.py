import json
import os

from config import Config

class Login(Config):
    def __init__(self):
        super().__init__()

    def initialize_password_file(self):
        with open(os.path.join(self.password_folder_path, "password.json"), "w") as f:
            f.write("{}")

