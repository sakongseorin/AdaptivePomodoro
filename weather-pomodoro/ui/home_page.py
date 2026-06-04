import customtkinter as ctk

from ui.timer_section import create_timer_section
from weather.weather import WeatherTimerAnalyzer
from stats_manager import StatsManager

FONT_FAMILY = "Malgun Gothic"


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.analyzer = WeatherTimerAnalyzer()
        self.stats = StatsManager()

        self.focus_time = 40
        self.break_time = 5

        self.current_location = ""
        self.adapted = False

        self.timer = None

        self.theme = {
            "맑음": "#FFF4D6",
            "구름 많음/흐림": "#EEF1F5",
            "비": "#DDE8F5",
            "눈": "#F4F7FB",
            "천둥번개": "#D3DAE6"
        }

        self.pack(fill="both", expand=True)

        self._build_ui()

        self.auto_refresh_stats()

        self.after(300, self.open_weather_popup)

    def open_weather_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.geometry("340x220")
        popup.title("지역 입력")

        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="지역 입력",
            font=(FONT_FAMILY, 16, "bold")
        ).pack(pady=15)

        entry = ctk.CTkEntry(
            popup,
            width=220
        )
        entry.pack(pady=10)

        entry.focus()

        error = ctk.CTkLabel(
            popup,
            text="",
            text_color="red"
        )
        error.pack()

        def submit(event=None):
            location = entry.get().strip()

            result = self.analyzer.fetch_and_analyze(
                location,
                self.adapted
            )

            if not result["success"]:
                error.configure(text=result["message"])
                return

            self.current_location = location

            self.apply_weather(result)

            popup.destroy()

        ctk.CTkButton(
            popup,
            text="확인",
            command=submit
        ).pack(pady=10)

        popup.bind("<Return>", submit)

    def apply_weather(self, result):
        self.focus_time = result["recommended_focus"]
        self.break_time = result["recommended_break"]

        bg = self.theme.get(
            result["weather_status"],
            "#FFF7E8"
        )

        self.configure(fg_color=bg)
        self.scroll.configure(
            fg_color=bg
        )

        self.weather_card.configure(
            text=(
                f"📍 {result['location']}\n"
                f"🌤 {result['weather_status']} | "
                f"🌡 {result['temperature']}°C | "
                f"💧 {result['humidity']}%\n\n"
                f"⏱ 집중 {self.focus_time}분 / "
                f"휴식 {self.break_time}분"
            )
        )

        self.music_label.configure(
            text=result["music"]
        )

        self.message_label.configure(
            text=result["message"]
        )

        if self.timer:
            self.timer.update_times(
                self.focus_time,
                self.break_time
            )

        self.update_stats()

    def toggle_adaptation(self):
        self.adapted = bool(
            self.adapt_switch.get()
        )

        if self.current_location:
            result = self.analyzer.fetch_and_analyze(
                self.current_location,
                self.adapted
            )

            if result["success"]:
                self.apply_weather(result)

    def update_stats(self):
        today = self.stats.get_today_minutes()
        week = self.stats.get_week_minutes()
        total = self.stats.get_total_minutes()
        sessions = self.stats.get_today_sessions()

        self.stats_label.configure(
            text=(
                f"오늘 공부 시간: "
                f"{today // 60}시간 "
                f"{today % 60}분\n"

                f"이번 주 공부 시간: "
                f"{week // 60}시간 "
                f"{week % 60}분\n"

                f"누적 공부 시간: "
                f"{total // 60}시간 "
                f"{total % 60}분\n"

                f"오늘 완료 세션: "
                f"{sessions}회"
            )
        )

    def auto_refresh_stats(self):
        self.update_stats()
        self.after(5000, self.auto_refresh_stats)

    def _build_ui(self):
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.scroll,
            text="일기예뽀",
            font=(FONT_FAMILY, 34, "bold")
        ).pack(pady=(20, 10))

        self.weather_card = ctk.CTkLabel(
            self.scroll,
            text="날씨 정보를 입력하세요",
            width=340,
            height=100,
            corner_radius=18,
            fg_color="#FFFFFF",
            justify="left"
        )

        self.weather_card.pack(
            pady=(10, 5)
        )

        self.adapt_switch = ctk.CTkSwitch(
            self.scroll,
            text="실내 환경 적응 완료",
            command=self.toggle_adaptation
        )

        self.adapt_switch.pack(
            pady=(0, 10)
        )
        ctk.CTkButton(
            self.scroll,
            text="🌍 지역 다시 검색",
            command=self.open_weather_popup,
            width=180
        ).pack(pady=(0, 10))

        self.timer = create_timer_section(
            self.scroll,
            self.focus_time,
            self.break_time,
            self.update_stats
        )

        self.timer.pack(
            pady=(5, 5)
        )

        stats_frame = ctk.CTkFrame(
            self.scroll,
            width=340,
            height=120,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        stats_frame.pack(
            pady=(5, 5)
        )

        stats_frame.pack_propagate(False)

        ctk.CTkLabel(
            stats_frame,
            text="📊 공부 통계",
            font=(FONT_FAMILY, 14, "bold")
        ).pack(pady=(10, 5))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="통계 로딩 중..."
        )

        self.stats_label.pack()

        self.update_stats()

        music_frame = ctk.CTkFrame(
            self.scroll,
            width=340,
            height=90,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        music_frame.pack(
            pady=(5, 5)
        )

        music_frame.pack_propagate(False)

        ctk.CTkLabel(
            music_frame,
            text="🎵 추천 음악",
            font=(FONT_FAMILY, 13, "bold")
        ).pack(pady=(10, 5))

        self.music_label = ctk.CTkLabel(
            music_frame,
            text="날씨를 입력하세요"
        )

        self.music_label.pack()

        message_frame = ctk.CTkFrame(
            self.scroll,
            width=340,
            height=180,
            corner_radius=18,
            fg_color="#FFFFFF"
        )

        message_frame.pack(
            pady=(5, 10)
        )

        message_frame.pack_propagate(False)

        ctk.CTkLabel(
            message_frame,
            text="💬 오늘의 멘트",
            font=(FONT_FAMILY, 13, "bold")
        ).pack(pady=(10, 5))

        self.message_label = ctk.CTkLabel(
            message_frame,
            text="오늘도 화이팅!",
            wraplength=300,
            justify="left"
        )

        self.message_label.pack()