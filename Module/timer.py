from config import Config


class Timer(Config):
    def __init__(self):
        super().__init__()

    def tick(self, remaining, time_label, tick, min_entry, sec_entry, start_btn, stop_btn):
        if getattr(time_label, "_stopped", False):
            return

        hours, remainder = divmod(remaining, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_label.configure(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

        if remaining > 0:
            time_label._after_id = time_label.after(1000, tick, remaining - 1)
        else:
            if not getattr(time_label, "_stopped", False):
                print("Time's up!")
                self.on_finish(min_entry, sec_entry, start_btn, stop_btn)

    def timer_function(self, total_seconds, time_label, min_entry, sec_entry, start_btn, stop_btn):
        time_label._stopped = False

        prev_after_id = getattr(time_label, "_after_id", None)
        if prev_after_id:
            try:
                time_label.after_cancel(prev_after_id)
            except Exception:
                pass
            time_label._after_id = None

        self.tick(total_seconds, time_label, self.tick, min_entry, sec_entry, start_btn, stop_btn)

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
        if mins < 0 or secs < 0 or secs >= 60:
            print("Invalid input")
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
        time_label.config(text="00:00:00")

        if after_id:
            try:
                time_label.after_cancel(after_id)
            except Exception:
                pass
            time_label._after_id = None

        min_entry.configure(state="normal")
        sec_entry.configure(state="normal")
        start_btn.configure(state="normal")
        stop_btn.configure(state="disabled")
