import customtkinter as ctk
import tkinter as tk

FONT_FAMILY = "Malgun Gothic"


class PomodoroTimer(ctk.CTkFrame):
    def __init__(self, parent, minutes=25, **kwargs):
        super().__init__(
            parent,
            width=420,
            height=500,
            corner_radius=32,
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
            text="집중 시간",
            font=(FONT_FAMILY, 18),
            text_color="#6A6A6A",
        )
        self.title_label.pack(pady=(30, 10))

        self.canvas = tk.Canvas(
            self,
            width=260,
            height=260,
            bg="#FFFFFF",
            highlightthickness=0,
        )
        self.canvas.pack(pady=10)

        self.canvas.create_oval(
            20,
            20,
            240,
            240,
            outline="#E6D5C3",
            width=12,
        )

        self.progress_arc = self.canvas.create_arc(
            20,
            20,
            240,
            240,
            start=90,
            extent=0,
            style="arc",
            outline="#D9B382",
            width=12,
        )

        self.timer_text = self.canvas.create_text(
            130,
            130,
            text="25:00",
            font=(FONT_FAMILY, 34, "bold"),
            fill="#2C2C2C",
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="준비 완료",
            font=(FONT_FAMILY, 15),
            text_color="#777777",
        )
        self.status_label.pack(pady=(5, 20))

        button_row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        button_row.pack(pady=(0, 30))

        self.toggle_button = ctk.CTkButton(
            button_row,
            text="시작하기",
            command=self.toggle,
            width=140,
            height=46,
            corner_radius=18,
            fg_color="#D9B382",
            hover_color="#C79D69",
            font=(FONT_FAMILY, 16, "bold"),
        )
        self.toggle_button.pack(side="left", padx=8)

        self.reset_button = ctk.CTkButton(
            button_row,
            text="리셋",
            command=self.reset,
            width=110,
            height=46,
            corner_radius=18,
            fg_color="#E0E0E0",
            text_color="#333333",
            hover_color="#C8C8C8",
            font=(FONT_FAMILY, 16, "bold"),
        )
        self.reset_button.pack(side="left", padx=8)

    def toggle(self):
        if self.is_running:
            self.pause()
            return

        self.start()

    def start(self):
        if self.remaining_seconds <= 0:
            self.remaining_seconds = self.total_seconds

        self.is_running = True
        self.toggle_button.configure(text="일시정지")
        self.status_label.configure(text="집중 중")
        self._schedule_tick()

    def pause(self):
        self.is_running = False
        self.toggle_button.configure(text="시작하기")
        self.status_label.configure(text="잠시 멈춤")
        self._cancel_tick()

    def reset(self):
        self.is_running = False
        self.remaining_seconds = self.total_seconds
        self.toggle_button.configure(text="시작하기")
        self.status_label.configure(text="준비 완료")
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
            self.toggle_button.configure(text="시작하기")
            self.status_label.configure(text="완료!")
            self.after_id = None
            return

        self.after_id = self.after(1000, self._tick)

    def _update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        self.canvas.itemconfig(
            self.timer_text,
            text=f"{minutes:02d}:{seconds:02d}"
        )
 
        elapsed = self.total_seconds - self.remaining_seconds
        progress_value = elapsed / self.total_seconds if self.total_seconds else 0

        if progress_value <= 0:
            extent = 0
        else:
            extent = -(360 * progress_value)

        self.canvas.itemconfig(
            self.progress_arc,
            extent=extent
        )


def create_timer_section(root):
    timer = PomodoroTimer(root)
    timer.pack(pady=36)
    return timer