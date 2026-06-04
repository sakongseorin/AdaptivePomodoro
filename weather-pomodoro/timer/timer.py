import customtkinter as ctk
import tkinter as tk

from stats_manager import StatsManager

FONT_FAMILY = "Malgun Gothic"


class PomodoroTimer(ctk.CTkFrame):
    def __init__(self, parent, minutes=25, break_minutes=5, stats_callback=None):
        super().__init__(
            parent,
            width=380,
            height=360,
            fg_color="transparent",
        )

        self.focus_minutes = minutes
        self.break_minutes = break_minutes

        self.mode = "focus"
        self.is_running = False

        self.remaining_seconds = self.focus_minutes * 60
        self.total_seconds = self.focus_minutes * 60

        self.stats_manager = StatsManager()
        self.stats_callback = stats_callback

        self._build_ui()
        self._update_display()

    def _build_ui(self):
        self.phase_label = ctk.CTkLabel(
            self,
            text="집중 시간",
            font=(FONT_FAMILY, 16, "bold")
        )
        self.phase_label.pack(pady=(0, 2))

        self.canvas = tk.Canvas(
            self,
            width=240,
            height=240,
            bg="#FFF7E8",
            highlightthickness=0,
        )
        self.canvas.pack(pady=5)

        self.canvas.create_oval(
            15,
            15,
            225,
            225,
            outline="#E6D5C3",
            width=10,
        )

        self.arc = self.canvas.create_arc(
            15,
            15,
            225,
            225,
            start=90,
            extent=0,
            style="arc",
            outline="#D9B382",
            width=10,
        )

        self.time_text = self.canvas.create_text(
            120,
            120,
            text="25:00",
            font=(FONT_FAMILY, 28, "bold"),
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="준비 완료",
            font=(FONT_FAMILY, 12),
        )
        self.status_label.pack(pady=2)

        btn_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        btn_frame.pack(pady=2)

        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="시작",
            width=110,
            command=self.toggle,
        )
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(
            btn_frame,
            text="리셋",
            width=110,
            command=self.reset,
        )
        self.reset_btn.pack(side="left", padx=5)

    def toggle(self):
        if self.is_running:
            self.pause()
        else:
            self.start()

    def start(self):
        if self.is_running:
            return

        self.is_running = True

        self.status_label.configure(text="진행 중")
        self.start_btn.configure(text="일시정지")

        self.after(1000, self._tick)

    def pause(self):
        self.is_running = False

        self.status_label.configure(text="일시정지")
        self.start_btn.configure(text="재개")

    def reset(self):
        self.is_running = False

        self.mode = "focus"

        self.remaining_seconds = self.focus_minutes * 60
        self.total_seconds = self.focus_minutes * 60

        self.phase_label.configure(text="집중 시간")
        self.status_label.configure(text="준비 완료")
        self.start_btn.configure(text="시작")

        self._update_display()

    def _tick(self):
        if not self.is_running:
            return

        self.remaining_seconds -= 1

        self._update_display()

        if self.remaining_seconds <= 0:
            self._switch_mode()
            return

        self.after(1000, self._tick)

    def _switch_mode(self):
        if self.mode == "focus":

            self.stats_manager.record_session(
                self.focus_minutes
            )
            
            if self.stats_callback:
                self.stats_callback()

            self.mode = "break"

            self.remaining_seconds = (
                self.break_minutes * 60
            )

            self.total_seconds = (
                self.break_minutes * 60
            )

            self.phase_label.configure(
                text="휴식 시간"
            )

        else:
            self.mode = "focus"

            self.remaining_seconds = (
                self.focus_minutes * 60
            )

            self.total_seconds = (
                self.focus_minutes * 60
            )

            self.phase_label.configure(
                text="집중 시간"
            )

        self._update_display()
        self.after(1000, self._tick)

    def _update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        self.canvas.itemconfig(
            self.time_text,
            text=f"{minutes:02d}:{seconds:02d}"
        )

        progress = (
            self.total_seconds
            - self.remaining_seconds
        ) / self.total_seconds

        extent = -360 * progress

        self.canvas.itemconfig(
            self.arc,
            extent=extent
        )

    def update_times(
        self,
        focus_minutes,
        break_minutes
    ):
        self.focus_minutes = focus_minutes
        self.break_minutes = break_minutes

        self.reset()