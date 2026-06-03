import customtkinter as ctk
import tkinter as tk

FONT_FAMILY = "Malgun Gothic"


class PomodoroTimer(ctk.CTkFrame):
    def __init__(self, parent, minutes=25, break_minutes=5):
        super().__init__(
            parent,
            width=380,
            height=360,
            fg_color="transparent",
        )

        self.focus_minutes = minutes
        self.break_minutes = break_minutes

        self.mode = "focus"
        self.remaining_seconds = self.focus_minutes * 60
        self.is_running = False

        self._build_ui()

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        self.phase_label = ctk.CTkLabel(self, text="집중", font=(FONT_FAMILY, 16, "bold"))
        self.phase_label.pack(pady=(0, 2))

        self.canvas = tk.Canvas(
            self,
            width=240,
            height=240,
            bg="#FFF7E8",
            highlightthickness=0,
        )
        self.canvas.pack(pady=5)

        self.canvas.create_oval(15, 15, 225, 225, outline="#E6D5C3", width=10)

        self.arc = self.canvas.create_arc(
            15, 15, 225, 225,
            start=90,
            extent=0,
            style="arc",
            outline="#D9B382",
            width=10,
        )

        self.text = self.canvas.create_text(
            120, 120,
            text=f"{self.focus_minutes:02d}:00",
            font=(FONT_FAMILY, 28, "bold"),
        )

        self.status = ctk.CTkLabel(self, text="준비 완료")
        self.status.pack(pady=2)

        btn = ctk.CTkFrame(self, fg_color="transparent")
        btn.pack(pady=2)

        self.start_btn = ctk.CTkButton(btn, text="시작", command=self.toggle, width=110)
        self.start_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(btn, text="리셋", command=self.reset, width=110)
        self.reset_btn.pack(side="left", padx=5)

    # =========================
    # control
    # =========================
    def toggle(self):
        if self.is_running:
            self.pause()
        else:
            self.start()

    def start(self):
        self.is_running = True
        self.status.configure(text="진행 중")
        self.start_btn.configure(text="일시정지")
        self._tick()

    def pause(self):
        self.is_running = False
        self.status.configure(text="일시정지")
        self.start_btn.configure(text="재개")

    def reset(self):
        self.is_running = False
        self.mode = "focus"
        self.remaining_seconds = self.focus_minutes * 60

        self.status.configure(text="준비 완료")
        self.phase_label.configure(text="집중")
        self.start_btn.configure(text="시작")

        self._update()

    # =========================
    # timer loop
    # =========================
    def _tick(self):
        if not self.is_running:
            return

        self.remaining_seconds -= 1
        self._update()

        if self.remaining_seconds <= 0:
            self._switch()
            return

        self.after(1000, self._tick)

    def _switch(self):
        if self.mode == "focus":
            self.mode = "break"
            self.remaining_seconds = self.break_minutes * 60
            self.phase_label.configure(text="휴식")
        else:
            self.mode = "focus"
            self.remaining_seconds = self.focus_minutes * 60
            self.phase_label.configure(text="집중")

        self._tick()

    def _update(self):
        m = self.remaining_seconds // 60
        s = self.remaining_seconds % 60
        self.canvas.itemconfig(self.text, text=f"{m:02d}:{s:02d}")