import json
import os
from tkinter import Entry, Listbox, Button, Label, Frame, TclError, ttk, Menu
import customtkinter as ctk

from config import Config


class Theme(Config):
    def __init__(self):
        super().__init__()

    # ----- Theme Persistence ----- #
    def save_theme_preference(self, theme_name):
        """Save the user's theme preference to a file."""
        with open(self.THEME_PREFERENCE_FILE, "w") as f:
            json.dump({"theme": theme_name}, f)

    def load_theme_preference(self):
        """Load the user's theme preference from the file."""
        try:
            if os.path.exists(self.THEME_PREFERENCE_FILE):
                with open(self.THEME_PREFERENCE_FILE, "r") as f:
                    data = json.load(f)
                    theme = data.get("theme", "blue")
                    return theme if theme else "blue"
        except (json.JSONDecodeError, OSError):
            pass
        return "blue"

    # ----- Theme Application ----- #
    def apply_theme(self, frame, theme_name):
        if theme_name in self.THEMES:
            theme = self.THEMES[theme_name]
            self.apply_theme_to_widgets(
                frame,
                theme["frame_bg"],
                theme["ctrl_bg"],
                fg=theme["fg"],
                listbox_color=theme["listbox_color"],
                entry_color=theme["entry_color"],
                button_bg=theme["button_bg"],
                button_hover=theme["button_hover"],
                button_fg=theme["button_fg"]
            )
            # Apply theme to Treeview globally
            self.apply_treeview_theme(
                bg=theme["listbox_color"],
                fg=theme["fg"],
                selected_bg=theme["button_bg"],
                selected_fg=theme["button_fg"],
                field_bg=theme["listbox_color"]
            )
            self.neutralize_button_highlight(frame)

    def apply_theme_to_widgets(self, frame, frame_bg, ctrl_bg, fg=None, listbox_color=None,
                               entry_color=None, button_bg=None, button_hover=None, button_fg=None):
        """Apply theme colors recursively to all widgets in a frame."""
        try:
            frame.configure(fg_color=frame_bg)
        except TclError:
            pass

        ctk.set_appearance_mode("light")

        stack = [frame]
        while stack:
            parent = stack.pop()
            for w in parent.winfo_children():
                widget_class = w.winfo_class()

                if isinstance(w, ctk.CTkFrame):
                    try:
                        w.configure(fg_color=frame_bg)
                    except (TclError, AttributeError):
                        pass

                elif isinstance(w, ctk.CTkLabel):
                    try:
                        w.configure(text_color=fg, fg_color=ctrl_bg)
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkButton):
                    try:
                        w.configure(
                            fg_color=button_bg,
                            hover=False,
                            hover_color=button_bg,
                            text_color=button_fg,
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkEntry):
                    try:
                        w.configure(fg_color=entry_color, text_color=fg, border_color=button_bg)
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkScrollbar):
                    try:
                        w.configure(
                            fg_color=ctrl_bg,
                            button_color=button_bg,
                            button_hover_color=button_hover
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                elif isinstance(w, ctk.CTkOptionMenu):
                    try:
                        w.configure(
                            fg_color=ctrl_bg,
                            button_color=button_bg,
                            button_hover_color=button_hover,
                            text_color=fg,
                            font=self.SUBTITLE_FONT
                        )
                    except (TclError, AttributeError, ValueError):
                        pass

                elif widget_class in ('Label', 'Button', 'Entry', 'Listbox', 'Frame'):
                    if fg is not None:
                        try:
                            w.configure(fg=fg)
                        except (TclError, ValueError, AttributeError):
                            pass

                    if isinstance(w, Entry):
                        try:
                            w.configure(bg=entry_color)
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Listbox):
                        try:
                            w.configure(selectbackground=ctrl_bg)
                            w.configure(bg=listbox_color)
                            w.configure(selectforeground=fg or "black")
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Button):
                        try:
                            w.configure(
                                bg=ctrl_bg,
                                activebackground=ctrl_bg,
                                activeforeground=fg if fg is not None else w.cget("fg"),
                                highlightthickness=0,
                                bd=0,
                                relief="flat",
                            )
                            try:
                                w.configure(default="normal", takefocus=0)
                            except (TclError, ValueError, AttributeError):
                                pass
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Label):
                        try:
                            w.configure(bg=ctrl_bg)
                        except (TclError, ValueError, AttributeError):
                            pass

                    elif isinstance(w, Frame):
                        try:
                            w.configure(bg=frame_bg)
                        except (TclError, ValueError, AttributeError):
                            pass

                stack.append(w)

    @staticmethod
    def apply_treeview_theme(bg, fg, selected_bg, selected_fg, field_bg):
        """Apply theme colors to all ttk.Treeview widgets globally."""
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background=bg,
                        foreground=fg,
                        fieldbackground=field_bg,
                        borderwidth=0,
                        font=("Arial", 13)
                        )
        style.configure("Treeview.Heading",
                        background=bg,
                        foreground=fg
                        )
        style.map("Treeview",
                  background=[("selected", selected_bg)],
                  foreground=[("selected", selected_fg)]
                  )

    @staticmethod
    def neutralize_button_highlight(root_widget):
        """Remove hover/active/focus highlights from all buttons in the widget tree."""
        try:
            root_widget.option_add("*Button.highlightThickness", 0)
            root_widget.option_add("*highlightThickness", 0)
            try:
                bg_color = root_widget.cget("bg")
            except (ValueError, Exception):
                bg_color = "SystemButtonFace"
            root_widget.option_add("*Button.activeBackground", bg_color)
            root_widget.option_add("*Button.activeForeground", "SystemButtonText")
        except (KeyError, TclError):
            pass

        stack = [root_widget]
        while stack:
            parent = stack.pop()
            for w in parent.winfo_children():
                try:
                    if isinstance(w, ctk.CTkButton):
                        try:
                            w.configure(hover=False, hover_color=w.cget("fg_color"))
                        except (KeyError, TclError):
                            pass
                        try:
                            w.configure(border_width=w.cget("border_width"))
                        except (KeyError, TclError):
                            pass

                    elif w.winfo_class() == "Button":
                        try:
                            normal_bg = w.cget("bg")
                            normal_fg = w.cget("fg")
                            w.configure(
                                activebackground=normal_bg,
                                activeforeground=normal_fg,
                                highlightthickness=0,
                                bd=0,
                                relief="flat",
                            )
                            try:
                                w.configure(default="normal", takefocus=0)
                            except (KeyError, TclError):
                                pass
                        except (KeyError, TclError):
                            pass
                except (KeyError, TclError):
                    pass
                stack.append(w)

    def create_theme_buttons(self, parent, *targets):
        """Create theme-selection buttons inside a frame."""
        theme_frame = ctk.CTkFrame(parent)

        def change_theme(theme_name):
            self.save_theme_preference(theme_name)
            tgt_list = list(targets)
            if parent not in tgt_list:
                tgt_list.insert(0, parent)

            for t in tgt_list:
                if t is None:
                    continue
                try:
                    self.apply_theme(t, theme_name)
                except (KeyError, TclError):
                    pass

            try:
                mode = self.CTK_APPEARANCE_MODES.get(theme_name, "light")
                ctk.set_appearance_mode(mode)
            except (KeyError, TclError):
                pass

            for t in tgt_list:
                try:
                    self.neutralize_button_highlight(t)
                except (KeyError, TclError):
                    pass
            try:
                parent.update_idletasks()
            except (KeyError, TclError):
                pass

        theme_names = ["Pink", "Blue", "White", "Green", "Purple", "Yellow", "orange"]
        for i, name in enumerate(theme_names):
            btn = ctk.CTkButton(
                theme_frame,
                text=f"{name} Theme",
                command=lambda n=name.lower(): change_theme(n),
                width=100
            )
            btn.grid(row=i, column=0, padx=5, pady=5, sticky="sew")

        return theme_frame

    def create_theme_menu(self, menubar, *targets):
        theme_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Themes", menu=theme_menu)  # ← directly "Themes", no submenu

        def change_theme(theme_name):
            self.save_theme_preference(theme_name)
            for t in targets:
                if t is None:
                    continue
                try:
                    self.apply_theme(t, theme_name)
                except (KeyError, TclError):
                    pass
            try:
                mode = self.CTK_APPEARANCE_MODES.get(theme_name, "light")
                ctk.set_appearance_mode(mode)
            except (KeyError, TclError):
                pass
            for t in targets:
                try:
                    self.neutralize_button_highlight(t)
                except (KeyError, TclError):
                    pass

        for name in self.THEMES.keys():
            theme_menu.add_command(
                label=name.capitalize(),
                command=lambda n=name: change_theme(n)
            )
    def apply_themes_to_all(self, frame):
        theme = self.load_theme_preference()
        self.apply_theme(frame, theme)
        self.neutralize_button_highlight(frame)