import customtkinter as ctk


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