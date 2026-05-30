import customtkinter as ctk


def create_weather_card(root):
    weather_card = ctk.CTkFrame(
        root,
        width=340,
        height=140,
        corner_radius=25,
        fg_color="#FFFFFF"
    )

    weather_card.pack(pady=10)
    weather_card.pack_propagate(False)

    weather_icon = ctk.CTkLabel(
        weather_card,
        text="☀️",
        font=("맑은 고딕", 38)
    )
    weather_icon.pack(pady=(18, 5))

    weather_text = ctk.CTkLabel(
        weather_card,
        text="맑음 · 24°C · 습도 60%",
        font=("맑은 고딕", 14),
        text_color="#4B4B4B"
    )

    weather_text.pack()