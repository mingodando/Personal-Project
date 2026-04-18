import customtkinter as ctk
from tkinter import messagebox

from theme import Theme
from config import Config

class Timer:
    def __init__(self, config: Config, theme: Theme):
        self.config = config
        self.theme = theme
        self.timer_window = None
        self.root = None

    def tick(self, remaining, time_label, min_entry, sec_entry, start_btn, stop_btn):
        if getattr(time_label, "_stopped", False):
            return

        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_label.configure(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

        if remaining > 0:
            time_label._after_id = time_label.after(
                1000, self.tick, remaining - 1, time_label, min_entry, sec_entry, start_btn, stop_btn)
        else:
            if not getattr(time_label, "_stopped", False):
                messagebox.showinfo("Time's up!", "The timer has finished.")
                self.on_finish(min_entry, sec_entry, start_btn, stop_btn)

    def timer_function(self, total_seconds, time_label, min_entry, sec_entry, start_btn, stop_btn):
        time_label._stopped = False

        prev_after_id = getattr(time_label, "_after_id", None)
        if prev_after_id:
            try:
                time_label.after_cancel(prev_after_id)
            except KeyError:
                pass
            time_label._after_id = None

        self.tick(total_seconds, time_label, min_entry, sec_entry, start_btn, stop_btn)

    @staticmethod
    def on_finish(min_entry, sec_entry, start_btn, stop_btn):
        min_entry.configure(state="normal")
        sec_entry.configure(state="normal")
        start_btn.configure(state="normal")
        stop_btn.configure(state="disabled")

    @staticmethod
    def calculate_seconds(min_entry, sec_entry):
        try:
            mins = int((min_entry.get() or "0").strip())
            secs = int((sec_entry.get() or "0").strip())
        except ValueError:
            print("Invalid input")
            return None
        if mins < 0 or secs < 0:
            messagebox.showerror("Error", "Minutes and seconds cannot be negative.")
        elif secs >= 60:
            messagebox.showerror("Error", "Seconds must be less than 60.")
            return None
        return mins * 60 + secs

    def start_timer(self, min_entry, sec_entry, time_label, start_btn, stop_btn):
        total = self.calculate_seconds(min_entry, sec_entry)
        if total is None:
            return
        min_entry.configure(state="disabled")
        sec_entry.configure(state="disabled")
        start_btn.configure(state="disabled")
        stop_btn.configure(state="normal")
        self.timer_function(total, time_label, min_entry, sec_entry, start_btn, stop_btn)

    @staticmethod
    def stop_timer(min_entry, sec_entry, time_label, start_btn, stop_btn):
        time_label._stopped = True
        after_id = getattr(time_label, "_after_id", None)
        time_label.configure(text="00:00:00")

        if after_id:
            try:
                time_label.after_cancel(after_id)
            except KeyError:
                pass
            time_label._after_id = None

        min_entry.configure(state="normal")
        sec_entry.configure(state="normal")
        start_btn.configure(state="normal")
        stop_btn.configure(state="disabled")

    def pause_timer(self, time_label, min_entry, sec_entry, start_btn, stop_btn, pause_btn):
        if getattr(time_label, "_stopped", False):
            # Currently paused — resume
            time_label._stopped = False
            pause_btn.configure(text="Pause")
            text = time_label.cget("text")
            h, m, s = map(int, text.split(":"))
            remaining = h * 3600 + m * 60 + s
            self.tick(remaining, time_label, min_entry, sec_entry, start_btn, stop_btn)
        else:
            # Currently running — pause
            after_id = getattr(time_label, "_after_id", None)
            if after_id:
                try:
                    time_label.after_cancel(after_id)
                except KeyError:
                    pass
                time_label._after_id = None
            time_label._stopped = True
            pause_btn.configure(text="Resume")

    def main_timer(self):
        if self.timer_window and self.timer_window.winfo_exists():
            self.timer_window.focus()
            return

        timer_window = ctk.CTkToplevel(self.root)
        timer_window.attributes("-topmost", True)
        timer_window.title("Timer")
        timer_window.geometry("300x500")

        # ===== TIMER TAB ===== #
        time_panel = ctk.CTkFrame(timer_window, width=300, height=400)
        time_panel.grid(row=2, column=0, sticky="nsew")
        time_panel.grid_propagate(False)
        time_panel.grid_columnconfigure(0, weight=1)
        time_panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(time_panel, text="Minutes:", font=self.config.SUBTITLE_FONT, width=300).grid(
            row=0, column=0, columnspan=4, padx=10, pady=5, sticky="we"
        )
        min_entry = ctk.CTkEntry(time_panel, font=self.config.SUBTITLE_FONT, width=300)
        min_entry.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="we")

        ctk.CTkLabel(time_panel, text="Seconds:", font=self.config.SUBTITLE_FONT, width=300).grid(
            row=2, column=0, columnspan=4, padx=10, pady=5, sticky="we"
        )
        sec_entry = ctk.CTkEntry(time_panel, font=self.config.SUBTITLE_FONT, width=300)
        sec_entry.grid(row=3, column=0, columnspan=4, padx=10, pady=5, sticky="we")

        time_label = ctk.CTkLabel(time_panel, text="00:00:00", font=self.config.SUBTITLE_FONT, width=300)
        time_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        start_btn = ctk.CTkButton(
            time_panel, text="Start", width=80,
            command=lambda: self.start_timer(min_entry, sec_entry, time_label, start_btn, stop_btn)
        )
        start_btn.grid(row=5, column=0, padx=10, pady=(5, 10))

        stop_btn = ctk.CTkButton(
            time_panel, text="Stop", width=80,
            command=lambda: self.stop_timer(min_entry, sec_entry, time_label, start_btn, stop_btn)
        )
        stop_btn.grid(row=5, column=1, padx=10, pady=(5, 10))

        pause_btn = ctk.CTkButton(
            time_panel, text="Pause", width=80,
            command=lambda: self.pause_timer(time_label, min_entry, sec_entry, start_btn, stop_btn, pause_btn)
        )
        pause_btn.grid(row=5, column=2, padx=10, pady=(5, 10))

        time_panel.grid_columnconfigure(0, weight=1)
        time_panel.grid_columnconfigure(1, weight=1)
        time_panel.grid_columnconfigure(2, weight=1)

        self.timer_window = timer_window

        self.theme.apply_themes_to_all(self.timer_window)
        self.timer_window.tkraise()
        self.timer_window.focus_force()