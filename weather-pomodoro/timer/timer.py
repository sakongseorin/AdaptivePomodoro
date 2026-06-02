import customtkinter as ctk


class PomodoroTimer(ctk.CTkFrame):
    def __init__(self, parent, minutes=25, **kwargs):
        super().__init__(
            parent,
            width=320,
            height=260,
            corner_radius=25,
            fg_color="#FFFFFF",
            **kwargs,
        )

        self.total_seconds = minutes * 60
        self.remaining_seconds = self.total_seconds
        self.is_running = False
        self.after_id = None

        self.pack_propagate(False)
        self._build_ui()
        self._update_display()

    def _build_ui(self):
        self.title_label = ctk.CTkLabel(
            self,
            text="Focus Time",
            font=("Arial", 15),
            text_color="#6A6A6A",
        )
        self.title_label.pack(pady=(28, 8))

        self.timer_label = ctk.CTkLabel(
            self,
            text="25:00",
            font=("Arial", 56, "bold"),
            text_color="#2C2C2C",
        )
        self.timer_label.pack()

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Arial", 13),
            text_color="#777777",
        )
        self.status_label.pack(pady=(0, 14))

        self.progress = ctk.CTkProgressBar(
            self,
            width=220,
            height=10,
            progress_color="#D9B382",
            fg_color="#E6D5C3",
        )
        self.progress.pack(pady=(0, 16))

        button_row = ctk.CTkFrame(self, fg_color="transparent")
        button_row.pack()

        self.toggle_button = ctk.CTkButton(
            button_row,
            text="Start",
            command=self.toggle,
            width=100,
            height=36,
            corner_radius=15,
            fg_color="#D9B382",
            hover_color="#C79D69",
        )
        self.toggle_button.pack(side="left", padx=5)

        self.reset_button = ctk.CTkButton(
            button_row,
            text="Reset",
            command=self.reset,
            width=80,
            height=36,
            corner_radius=15,
            fg_color="#E0E0E0",
            text_color="#333333",
            hover_color="#C8C8C8",
        )
        self.reset_button.pack(side="left", padx=5)

    def toggle(self):
        if self.is_running:
            self.pause()
            return

        self.start()

    def start(self):
        if self.remaining_seconds <= 0:
            self.remaining_seconds = self.total_seconds

        self.is_running = True
        self.toggle_button.configure(text="Pause")
        self.status_label.configure(text="Focusing")
        self._schedule_tick()

    def pause(self):
        self.is_running = False
        self.toggle_button.configure(text="Start")
        self.status_label.configure(text="Paused")
        self._cancel_tick()

    def reset(self):
        self.is_running = False
        self.remaining_seconds = self.total_seconds
        self.toggle_button.configure(text="Start")
        self.status_label.configure(text="Ready")
        self._cancel_tick()
        self._update_display()

    def _schedule_tick(self):
        self._cancel_tick()
        self.after_id = self.after(1000, self._tick)

    def _cancel_tick(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def _tick(self):
        if not self.is_running:
            return

        self.remaining_seconds -= 1
        self._update_display()

        if self.remaining_seconds <= 0:
            self.is_running = False
            self.toggle_button.configure(text="Start")
            self.status_label.configure(text="Done!")
            self.after_id = None
            return

        self.after_id = self.after(1000, self._tick)

    def _update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        elapsed = self.total_seconds - self.remaining_seconds
        progress_value = elapsed / self.total_seconds if self.total_seconds else 0
        self.progress.set(progress_value)


def create_timer_section(root):
    timer = PomodoroTimer(root)
    timer.pack(pady=35)
    return timer
