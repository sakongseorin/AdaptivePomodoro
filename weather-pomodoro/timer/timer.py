import customtkinter as ctk


def setup_timer(root, timer_frame, timer_label):
    running = False
    remaining = [25 * 60]
    after_id = [None]

    def update_display():
        m = remaining[0] // 60
        s = remaining[0] % 60
        timer_label.configure(text=f"{m:02d}:{s:02d}")

    def tick():
        nonlocal running

        if remaining[0] > 0:
            remaining[0] -= 1
            update_display()
            after_id[0] = timer_frame.after(1000, tick)
        else:
            running = False
            start_btn.configure(text="시작")
            timer_label.configure(text="완료!")

    def toggle():
        nonlocal running

        if running:
            running = False
            start_btn.configure(text="시작")

            if after_id[0]:
                timer_frame.after_cancel(after_id[0])
                after_id[0] = None

        else:
            running = True
            start_btn.configure(text="일시정지")
            tick()

    def reset():
        nonlocal running

        running = False

        if after_id[0]:
            timer_frame.after_cancel(after_id[0])
            after_id[0] = None

        remaining[0] = 25 * 60
        update_display()
        start_btn.configure(text="시작")

    start_btn = ctk.CTkButton(
        timer_frame,
        text="시작",
        command=toggle,
        width=100,
        corner_radius=15
    )
    start_btn.pack(pady=(10, 5))

    reset_btn = ctk.CTkButton(
        timer_frame,
        text="리셋",
        command=reset,
        width=80,
        corner_radius=15,
        fg_color="#E0E0E0",
        text_color="#333",
        hover_color="#C8C8C8"
    )
    reset_btn.pack()

    return start_btn, reset_btn