import json
import os
from tkinter import *
from tkinter import ttk
from tkinter import TclError
from .config import THEMES, THEME_PREFERENCE_FILE


def save_theme_preference(theme_name):
    """Save the user's theme preference to a file."""
    with open(THEME_PREFERENCE_FILE, "w") as f:
        json.dump({"theme": theme_name}, f)


def load_theme_preference():
    """Load the user's theme preference from file."""
    if os.path.exists(THEME_PREFERENCE_FILE):
        with open(THEME_PREFERENCE_FILE, "r") as f:
            data = json.load(f)
            return data.get("theme", "blue")
    return "blue"


def apply_theme(frame, theme_name):
    """Apply a theme to a frame by name."""
    if theme_name in THEMES:
        theme = THEMES[theme_name]
        apply_theme_to_widgets(
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


def apply_theme_to_widgets(frame, frame_bg, ctrl_bg, fg=None, listbox_color=None, 
                           entry_color=None, button_bg=None, button_hover=None, button_fg=None):
    """Apply theme colors to all widgets in a frame."""
    try:
        frame.configure(bg=frame_bg)
    except TclError:
        pass

    # Create a style object for ttk widgets
    style = ttk.Style()
    
    # Use 'clam' theme as base - it allows more customization than default
    try:
        style.theme_use('clam')
    except:
        pass

    # Configure ttk widget styles with more explicit settings
    try:
        style.configure('TLabel',
                       background=ctrl_bg,
                       foreground=fg,
                       borderwidth=0)
        style.configure('TEntry', 
                       fieldbackground=entry_color, 
                       foreground=fg,
                       bordercolor="#000000")
        style.configure('TButton', 
                       background=ctrl_bg, 
                       foreground=fg,
                       bordercolor="#000000")
        style.configure('TFrame', 
                       background=frame_bg)
        
        # Map is needed for buttons to change colors on different states
        style.map('TButton',
                  background=[('active', ctrl_bg), 
                             ('pressed', ctrl_bg), 
                             ('!active', ctrl_bg)],
                  foreground=[('active', fg), 
                             ('pressed', fg), 
                             ('!active', fg)])
        
        style.map('TLabel',
                  background=[('active', ctrl_bg), ('!active', ctrl_bg)])
                  
    except TclError:
        pass

    stack = [frame]

    while stack:
        parent = stack.pop()

        for w in parent.winfo_children():
            # Get widget class name
            widget_class = w.winfo_class()
            
            # Handle ttk.Frame explicitly
            if isinstance(w, ttk.Frame):
                try:
                    w.configure(style='TFrame')
                except TclError:
                    pass
            
            # Handle regular tkinter widgets
            elif widget_class in ('Label', 'Button', 'Entry', 'Listbox', 'Frame'):
                if fg is not None:
                    try:
                        w.configure(fg=fg)
                    except TclError:
                        pass
                
                if isinstance(w, Entry):
                    try:
                        w.configure(bg=entry_color)
                    except TclError:
                        pass

                elif isinstance(w, Listbox):
                    try:
                        w.configure(selectbackground=ctrl_bg)
                        w.configure(bg=listbox_color)
                        w.configure(selectforeground=fg or "black")
                    except TclError:
                        pass

                elif isinstance(w, Button):
                    try:
                        w.configure(bg=ctrl_bg)
                        if fg is not None:
                            w.configure(activeforeground=fg)
                            w.configure(activebackground=ctrl_bg)
                    except TclError:
                        pass

                elif isinstance(w, Label):
                    try:
                        w.configure(bg=ctrl_bg)
                    except TclError:
                        pass
                
                elif isinstance(w, Frame):
                    try:
                        w.configure(bg=frame_bg)
                    except TclError:
                        pass

            stack.append(w)


def create_theme_buttons(parent, frame1, frame2):
    """Create theme selection buttons."""
    theme_frame = ttk.Frame(parent)
    
    def change_theme(theme_name):
        """Change theme and save preference."""
        save_theme_preference(theme_name)
        apply_theme(frame1, theme_name)
        apply_theme(frame2, theme_name)
    
    # Create theme buttons
    pink_btn = ttk.Button(theme_frame, text="Pink Theme", 
                         command=lambda: change_theme("pink"))
    pink_btn.grid(row=0, column=0, padx=5, pady=5)
    
    blue_btn = ttk.Button(theme_frame, text="Blue Theme", 
                         command=lambda: change_theme("blue"))
    blue_btn.grid(row=0, column=1, padx=5, pady=5)
    
    white_btn = ttk.Button(theme_frame, text="White Theme", 
                          command=lambda: change_theme("white"))
    white_btn.grid(row=0, column=2, padx=5, pady=5)
    
    return theme_frame