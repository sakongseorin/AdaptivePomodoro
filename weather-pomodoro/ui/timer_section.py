import customtkinter as ctk
import tkinter as tk

def create_timer_section(root):
    timer_frame = ctk.CTkFrame(
        root,
        width=320,
        height=220,
        corner_radius=30,
        fg_color="#EAF2FF"
    )
    timer_frame.pack(pady=35)
    timer_frame.pack_propagate(False)

    focus_label = ctk.CTkLabel(
        timer_frame,
        text="집중 시간",
        font=("맑은 고딕", 15),
        text_color="#6A6A6A"
    )
    focus_label.pack(pady=(35, 10))

    timer_label = ctk.CTkLabel(
        timer_frame,
        text="25:00",
        font=("맑은 고딕", 60, "bold"),
        text_color="#2C2C2C"
    )
    timer_label.pack()

    # ── 여기서부터 추가 ──
    running = False
    remaining = [25 * 60]  # 25분
    after_id = [None]

    def tick():
        if remaining[0] > 0:
            remaining[0] -= 1
            m = remaining[0] // 60
            s = remaining[0] % 60
            timer_label.configure(text=f"{m:02d}:{s:02d}")
            after_id[0] = root.after(1000, tick)
        else:
            timer_label.configure(text="완료!")
            btn.configure(text="시작")

    def toggle():
        nonlocal running
        if running:
            running = False
            btn.configure(text="시작")
            if after_id[0]:
                root.after_cancel(after_id[0])
        else:
            running = True
            btn.configure(text="일시정지")
            tick()

    def reset():
        nonlocal running
        running = False
        btn.configure(text="시작")
        remaining[0] = 25 * 60
        timer_label.configure(text="25:00")
        if after_id[0]:
            root.after_cancel(after_id[0])

    btn = ctk.CTkButton(timer_frame, text="시작", command=toggle, width=100, corner_radius=15)
    btn.pack(pady=(10, 5))

    ctk.CTkButton(timer_frame, text="리셋", command=reset, width=80, corner_radius=15,
                  fg_color="#E0E0E0", text_color="#333", hover_color="#C8C8C8").pack()
