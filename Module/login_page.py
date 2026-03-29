from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTk
from tkinter import messagebox
import json
import os

from login import Login
from config import Config

class Loginpage(Config):
    def __init__(self):
        super().__init__()
        self.login = Login()
        self.password_file = os.path.join(self.password_folder_path, "users.json")

    def create_login_page(self):
        root = CTk()

        login = CTkFrame(root)
        login.grid(padx=20, pady=20)

        my_frame = CTkFrame(login)
        my_frame.grid(row=0, column=0, padx=10, pady=10)

        username_label = CTkLabel(my_frame, text="Username:")
        username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        username_entry = CTkEntry(my_frame, width=200)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_label = CTkLabel(my_frame, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        password_entry = CTkEntry(my_frame, width=200, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        login_button = CTkButton(my_frame, text="Login", command=lambda: self.check_login(username_entry, password_entry))
        login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def check_login(self, username_entry=None, password_entry=None):
        if username_entry is None or password_entry is None:
            return

        username = username_entry.get()
        password = password_entry.get()

        if not os.path.exists(self.password_file):
            self.login_failed()
            return
        with open(self.password_file, 'r') as file:
            y = json.load(file.read())
        usernames = y["people"]
        lines = [person for person in usernames if person["name"] == username]
        if len(lines) == 0:
            self.login_failed()
            return
        else:
            for line in lines:
                if line["password"] == password:
                    self.login_success()
                    return
                else:
                    self.login_failed()
                    return

    @staticmethod
    def login_success():
        messagebox.showinfo("Login Success", "You have successfully logged in!")

    @staticmethod
    def login_failed():
        messagebox.showerror("Login Failed", "Invalid username or password.")