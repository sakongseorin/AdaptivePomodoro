import customtkinter as ctk
from ui.timer_section import create_timer_section
from weather.weather import WeatherTimerAnalyzer

FONT_FAMILY = "Malgun Gothic"


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFF7E8")

        self.analyzer = WeatherTimerAnalyzer()

        self.focus_time = 25
        self.break_time = 5

        self.timer = None

        self.pack(fill="both", expand=True)

        self._build_ui()
        self.after(300, self.open_weather_popup)

    # =========================
    # popup
    # =========================
    def open_weather_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.geometry("340x200")
        popup.title("지역 입력")

        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="지역 입력",
            font=(FONT_FAMILY, 16, "bold")
        ).pack(pady=15)

        entry = ctk.CTkEntry(popup)
        entry.pack(pady=10)
        entry.focus()

        error = ctk.CTkLabel(popup, text="", text_color="red")
        error.pack()

        def submit(event=None):
            location = entry.get().strip()

            result = self.analyzer.fetch_and_analyze(location)

            if not result["success"]:
                error.configure(text=result["message"])
                return

            self.focus_time = result["recommended_focus"]
            self.break_time = result["recommended_break"]

            self.weather_card.configure(
                text=(
                    f"📍 {result['location']}\n"
                    f"🌤 {result['weather_status']}  |  🌡 {result['temperature']}°C  |  💧 {result['humidity']}%\n"
                    f"⏱ 집중 {result['recommended_focus']}분 / 휴식 {result['recommended_break']}분"
                )
            )

            if self.timer:
                self.timer.focus_minutes = self.focus_time
                self.timer.break_minutes = self.break_time
                self.timer.reset()

            popup.destroy()

        ctk.CTkButton(popup, text="확인", command=submit).pack(pady=10)
        popup.bind("<Return>", submit)

    # =========================
    # UI
    # =========================
    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scroll,
            text="일기예뽀",
            font=(FONT_FAMILY, 34, "bold"),
        ).pack(pady=(20, 10))

        # 날씨 카드
        self.weather_card = ctk.CTkLabel(
            scroll,
            text="날씨 정보를 입력하세요",
            width=340,
            height=100,
            corner_radius=18,
            fg_color="#FFFFFF",
            justify="left",
        )
        self.weather_card.pack(pady=(10, 5))

        # 🔥 타이머 (간격 줄임 핵심)
        self.timer = create_timer_section(
            scroll,
            self.focus_time,
            self.break_time
        )
        self.timer.pack(pady=(8, 6))

        # 🔥 통계 (위쪽 간격 제거)
        stats = ctk.CTkFrame(
            scroll,
            width=340,
            height=110,
            corner_radius=18,
            fg_color="#FFFFFF",
        )
        stats.pack(pady=(0, 6))
        stats.pack_propagate(False)

        ctk.CTkLabel(
            stats,
            text="📊 공부 통계",
            font=(FONT_FAMILY, 14, "bold"),
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            stats,
            text=(
                "오늘 공부 시간: 2시간 15분\n"
                "이번 주 총 공부: 11시간 40분\n"
                "날씨별 평균 집중: 28분"
            ),
            font=(FONT_FAMILY, 12),
            justify="left",
        ).pack()

        # 하단
        bottom_row = ctk.CTkFrame(scroll, fg_color="transparent")
        bottom_row.pack(pady=(0, 8))

        music_box = ctk.CTkFrame(
            bottom_row,
            width=160,
            height=90,
            corner_radius=15,
            fg_color="#FFFFFF",
        )
        music_box.pack(side="left", padx=5)
        music_box.pack_propagate(False)

        ctk.CTkLabel(
            music_box,
            text="🎵 음악",
            font=(FONT_FAMILY, 13, "bold"),
        ).pack(pady=8)

        ctk.CTkLabel(
            music_box,
            text="재생 없음",
            font=(FONT_FAMILY, 11),
        ).pack()

        memo_box = ctk.CTkFrame(
            bottom_row,
            width=160,
            height=90,
            corner_radius=15,
            fg_color="#FFFFFF",
        )
        memo_box.pack(side="left", padx=5)
        memo_box.pack_propagate(False)

        ctk.CTkLabel(
            memo_box,
            text="💬 멘트",
            font=(FONT_FAMILY, 13, "bold"),
        ).pack(pady=8)

        ctk.CTkLabel(
            memo_box,
            text="오늘도 집중해보자",
            font=(FONT_FAMILY, 11),
        ).pack()