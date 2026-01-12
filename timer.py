# timer.py
class PomodoroTimer:
    def __init__(self, work_duration=25*60, short_break=5*60, long_break=15*60, cycles_before_long_break=4):
        self.work_duration = work_duration
        self.short_break = short_break
        self.long_break = long_break
        self.cycles_before_long_break = cycles_before_long_break
        self.current_cycle = 0
        self.is_running = False
        self.time_left = self.work_duration
        self.on_complete = None  # Callback when timer ends

    def start(self):
        self.is_running = True

    def pause(self):
        self.is_running = False

    def reset(self):
        self.is_running = False
        self.time_left = self.work_duration
        self.current_cycle = 0

    def tick(self):
        """Call this every second to update the timer"""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
        elif self.is_running and self.time_left == 0:
            self._handle_session_complete()

    def _handle_session_complete(self):
        self.current_cycle += 1
        if self.current_cycle % self.cycles_before_long_break == 0:
            self.time_left = self.long_break
        else:
            self.time_left = self.short_break
        if self.on_complete:
            self.on_complete()
