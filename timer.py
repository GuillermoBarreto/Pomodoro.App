# timer.py
class PomodoroTimer:
    """Countdown timer for Pomodoro sessions.

    Call ``tick()`` once per second while ``is_running``; ``on_complete`` is
    invoked each time a work session ends.
    """

    def __init__(self, work_duration=25*60, short_break=5*60, long_break=15*60, cycles_before_long_break=4):
        for name, value in (
            ("work_duration", work_duration),
            ("short_break", short_break),
            ("long_break", long_break),
        ):
            if value <= 0:
                raise ValueError(f"{name} must be positive, got {value!r}")
        if cycles_before_long_break < 1:
            raise ValueError(
                f"cycles_before_long_break must be at least 1, got {cycles_before_long_break!r}"
            )
        self.work_duration = work_duration
        self.short_break = short_break
        self.long_break = long_break
        self.cycles_before_long_break = cycles_before_long_break
        self.current_cycle = 0
        self.is_running = False
        self._on_break = False
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
        self._on_break = False

    def tick(self):
        """Call this every second to update the timer"""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
        elif self.is_running and self.time_left == 0:
            self._handle_session_complete()

    def _handle_session_complete(self):
        if self._on_break:
            # A break finished: go back to work; do not advance the cycle.
            self._on_break = False
            self.time_left = self.work_duration
        else:
            self.current_cycle += 1
            self._on_break = True
            if self.current_cycle % self.cycles_before_long_break == 0:
                self.time_left = self.long_break
            else:
                self.time_left = self.short_break
        if self.on_complete:
            self.on_complete()
