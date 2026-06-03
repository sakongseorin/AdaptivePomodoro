import customtkinter as ctk

from ui.timer_section import create_timer_section


FONT_FAMILY = "Malgun Gothic"


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        self.weather = "sunny"

        self.theme = {
            "sunny": {
                "bg": "#FFF7E8",
                "weather": "맑음 24°C",
                "music": "Happy Study Playlist",
                "message": "휴식 시간에 가볍게 산책해보세요!",
            },
            "cloudy": {
                "bg": "#EEF2F7",
                "weather": "흐림 21°C",
                "music": "Calm Focus Playlist",
                "message": "차분하게 오늘 계획을 정리해보세요.",
            },
            "rainy": {
                "bg": "#E5EAF2",
                "weather": "비 18°C",
                "music": "Lo-fi Rain Study",
                "message": "따뜻한 차 한 잔과 함께 집중해보세요.",
            },
            "snowy": {
                "bg": "#F4F8FF",
                "weather": "눈 0°C",
                "music": "Winter Piano",
                "message": "조용한 시간 속에서 한 걸음씩 나아가요.",
            },
            "night": {
                "bg": "#243B64",
                "weather": "밤",
                "music": "Night Focus",
                "message": "오늘의 집중이 내일의 나를 만듭니다.",
            },
        }

        super().__init__(
            parent,
            fg_color=self.theme[self.weather]["bg"],
        )

        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        data = self.theme[self.weather]

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(
            scroll,
            text="일기예뽀",
            font=(FONT_FAMILY, 34, "bold"),
        ).pack(pady=(34, 8))

        ctk.CTkLabel(
            scroll,
            text=data["weather"],
            font=(FONT_FAMILY, 17),
        ).pack(pady=(0, 20))

        create_timer_section(scroll)

        mid = ctk.CTkFrame(scroll, fg_color="transparent")
        mid.pack(fill="x", padx=40, pady=(24, 18))

        music = ctk.CTkFrame(mid, corner_radius=24, height=140)
        music.pack(side="left", expand=True, fill="both", padx=(0, 10))
        music.pack_propagate(False)

        ctk.CTkLabel(
            music,
            text="오늘의 음악",
            font=(FONT_FAMILY, 17, "bold"),
        ).pack(pady=(28, 12))

        ctk.CTkLabel(
            music,
            text=data["music"],
            font=(FONT_FAMILY, 15),
        ).pack()

        msg = ctk.CTkFrame(mid, corner_radius=24, height=140)
        msg.pack(side="left", expand=True, fill="both", padx=(10, 0))
        msg.pack_propagate(False)

        ctk.CTkLabel(
            msg,
            text="오늘의 멘트",
            font=(FONT_FAMILY, 17, "bold"),
        ).pack(pady=(24, 10))

        ctk.CTkLabel(
            msg,
            text=data["message"],
            font=(FONT_FAMILY, 15),
            wraplength=260,
        ).pack()

        stats = ctk.CTkFrame(scroll, corner_radius=24, height=210)
        stats.pack(fill="x", padx=40, pady=(18, 42))
        stats.pack_propagate(False)

        ctk.CTkLabel(
            stats,
            text="학습 통계",
            font=(FONT_FAMILY, 20, "bold"),
        ).pack(pady=(30, 18))

        ctk.CTkLabel(
            stats,
            text="오늘 공부 시간 : 2시간 15분",
            font=(FONT_FAMILY, 15),
        ).pack(pady=6)
        ctk.CTkLabel(
            stats,
            text="이번 주 공부 시간 : 11시간 40분",
            font=(FONT_FAMILY, 15),
        ).pack(pady=6)
        ctk.CTkLabel(
            stats,
            text="평균 집중 시간 : 28분",
            font=(FONT_FAMILY, 15),
        ).pack(pady=6)
