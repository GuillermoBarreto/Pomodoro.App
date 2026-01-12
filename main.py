import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import time
import threading
from PIL import Image, ImageTk
import winsound

# ----------------- CONFIG -----------------
WORK_COLOR = "#4CAF50"      # Green
SHORT_BREAK_COLOR = "#2196F3"  # Blue
LONG_BREAK_COLOR = "#FF9800"   # Orange
BG_COLOR = "#2C2F33"
FONT = ("Helvetica", 16)
SESSION_HISTORY_LIMIT = 5
# -----------------------------------------

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro App ☕")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("400x600")

        self.is_running = False
        self.timer_thread = None
        self.current_time = 0
        self.current_phase = "Work"
        self.sessions_completed = 0
        self.session_history = []

        # Default times in seconds
        self.work_time = 25 * 60
        self.short_break_time = 5 * 60
        self.long_break_time = 15 * 60

        # UI Elements
        self.title_label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 24, "bold"), fg="white", bg=BG_COLOR)
        self.title_label.pack(pady=20)

        # Coffee cup canvas
        self.cup_canvas = tk.Canvas(root, width=150, height=200, bg=BG_COLOR, highlightthickness=0)
        self.cup_canvas.pack(pady=10)
        self.cup_outline = self.cup_canvas.create_rectangle(20, 20, 130, 180, outline="white", width=3)
        self.cup_fill = self.cup_canvas.create_rectangle(23, 180, 127, 180, fill=WORK_COLOR, width=0)

        # Timer label
        self.timer_label = tk.Label(root, text="00:00", font=("Helvetica", 48, "bold"), fg="white", bg=BG_COLOR)
        self.timer_label.pack(pady=20)

        # Buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer, width=10, bg="#7289DA", fg="white", font=FONT)
        self.start_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer, width=10, bg="#99AAB5", fg="white", font=FONT)
        self.pause_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, width=10, bg="#F04747", fg="white", font=FONT)
        self.reset_button.pack(pady=5)

        self.custom_button = tk.Button(root, text="Set Custom Times", command=self.set_custom_times, width=20, bg="#FAA61A", fg="white", font=FONT)
        self.custom_button.pack(pady=10)

        # Session history
        self.history_label = tk.Label(root, text="Session History:", font=FONT, fg="white", bg=BG_COLOR)
        self.history_label.pack(pady=10)
        self.history_text = tk.Text(root, height=5, width=40, bg="#23272A", fg="white", font=("Helvetica", 12))
        self.history_text.pack(pady=5)
        self.history_text.config(state=tk.DISABLED)

        self.update_timer_label()

    # ---------------- TIMER FUNCTIONS ----------------
    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            if not self.timer_thread or not self.timer_thread.is_alive():
                self.timer_thread = threading.Thread(target=self.run_timer)
                self.timer_thread.start()

    def pause_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.set_phase(self.current_phase)
        self.update_timer_label()
        self.update_cup_fill()

    def set_custom_times(self):
        work = simpledialog.askinteger("Work Time", "Enter work time in minutes:", minvalue=1, maxvalue=180)
        short_break = simpledialog.askinteger("Short Break", "Enter short break time in minutes:", minvalue=1, maxvalue=60)
        long_break = simpledialog.askinteger("Long Break", "Enter long break time in minutes:", minvalue=1, maxvalue=60)

        if work and short_break and long_break:
            self.work_time = work * 60
            self.short_break_time = short_break * 60
            self.long_break_time = long_break * 60
            self.reset_timer()

    def run_timer(self):
        while self.current_time > 0 and self.is_running:
            mins, secs = divmod(self.current_time, 60)
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
            self.update_cup_fill()
            time.sleep(1)
            self.current_time -= 1

        if self.current_time == 0:
            winsound.Beep(1000, 500)
            self.complete_phase()

    def complete_phase(self):
        if self.current_phase == "Work":
            self.sessions_completed += 1
            self.session_history.append("Work session completed")
            if len(self.session_history) > SESSION_HISTORY_LIMIT:
                self.session_history.pop(0)
            self.update_history()
            # Decide next break
            if self.sessions_completed % 4 == 0:
                self.set_phase("Long Break")
            else:
                self.set_phase("Short Break")
        else:
            self.set_phase("Work")
        self.is_running = False
        self.start_timer()

    def set_phase(self, phase):
        self.current_phase = phase
        if phase == "Work":
            self.current_time = self.work_time
            self.cup_color = WORK_COLOR
        elif phase == "Short Break":
            self.current_time = self.short_break_time
            self.cup_color = SHORT_BREAK_COLOR
        else:
            self.current_time = self.long_break_time
            self.cup_color = LONG_BREAK_COLOR
        self.update_timer_label()
        self.update_cup_fill()

    def update_timer_label(self):
        mins, secs = divmod(self.current_time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    # ---------------- CUP FILL ----------------
    def update_cup_fill(self):
        total_height = 160  # cup height
        if self.current_phase == "Work":
            fill_ratio = 1 - self.current_time / self.work_time if self.work_time else 0
        elif self.current_phase == "Short Break":
            fill_ratio = 1 - self.current_time / self.short_break_time if self.short_break_time else 0
        else:
            fill_ratio = 1 - self.current_time / self.long_break_time if self.long_break_time else 0

        fill_height = 160 * fill_ratio
        self.cup_canvas.coords(self.cup_fill, 23, 180 - fill_height, 127, 180)
        self.cup_canvas.itemconfig(self.cup_fill, fill=self.cup_color)

    # ---------------- HISTORY ----------------
    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for entry in self.session_history:
            self.history_text.insert(tk.END, entry + "\n")
        self.history_text.config(state=tk.DISABLED)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
