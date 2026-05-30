import customtkinter as ctk
import tkinter as tk


class HomePage(ctk.CTkFrame):
    def __init__(self, parent):
        self.weather = "sunny"

        self.theme = {
            "sunny": {
                "bg": "#FFF7E8",
                "weather": "☀️ 맑음 24°C",
                "music": "Happy Study Playlist",
                "message": "휴식 시간에 가볍게 산책해보세요!"
            },
            "cloudy": {
                "bg": "#EEF2F7",
                "weather": "☁️ 흐림 21°C",
                "music": "Calm Focus Playlist",
                "message": "차분하게 오늘 계획을 정리해보세요."
            },
            "rainy": {
                "bg": "#E5EAF2",
                "weather": "🌧️ 비 18°C",
                "music": "Lo-fi Rain Study",
                "message": "따뜻한 차 한 잔과 함께 집중해보세요."
            },
            "snowy": {
                "bg": "#F4F8FF",
                "weather": "❄️ 눈 0°C",
                "music": "Winter Piano",
                "message": "조용한 시간 속에서 한 걸음씩 나아가요."
            },
            "night": {
                "bg": "#243B64",
                "weather": "🌙 밤",
                "music": "Night Focus",
                "message": "오늘의 집중이 내일의 나를 만듭니다."
            }
        }

        super().__init__(
            parent,
            fg_color=self.theme[self.weather]["bg"]
        )

        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        data = self.theme[self.weather]

        # ─────────────────────────
        # SCROLL (전체 반응형 핵심)
        # ─────────────────────────
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ─────────────────────────
        # TITLE
        # ─────────────────────────
        ctk.CTkLabel(
            scroll,
            text="일기예뽀",
            font=("맑은 고딕", 30, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            scroll,
            text=data["weather"],
            font=("맑은 고딕", 15)
        ).pack()

        # ─────────────────────────
        # TIMER CARD (핵심 UI)
        # ─────────────────────────
        timer_card = ctk.CTkFrame(
            scroll,
            corner_radius=25,
            fg_color="#FFFFFF"
        )
        timer_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=25
        )

        # 🔥 반응형 핵심: 창 크기에 따라 캔버스도 확장
        canvas = tk.Canvas(
            timer_card,
            bg="white",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True, padx=20, pady=20)

        def draw(event=None):
            canvas.delete("all")

            w = canvas.winfo_width()
            h = canvas.winfo_height()

            size = min(w, h) - 40

            x1 = (w - size) / 2
            y1 = (h - size) / 2
            x2 = x1 + size
            y2 = y1 + size

            # 배경 링
            canvas.create_oval(
                x1, y1, x2, y2,
                width=12,
                outline="#E6D5C3"
            )

            # 진행 링 (데모)
            canvas.create_arc(
                x1, y1, x2, y2,
                start=90,
                extent=-120,
                width=12,
                outline="#D9B382",
                style="arc"
            )

            # 타이머 텍스트
            canvas.create_text(
                w / 2,
                h / 2 - 20,
                text="25:00",
                font=("맑은 고딕", 34, "bold"),
                fill="#5A3E2B"
            )

            canvas.create_text(
                w / 2,
                h / 2 + 20,
                text="집중 중",
                font=("맑은 고딕", 14),
                fill="#777"
            )

        canvas.bind("<Configure>", draw)

        # ─ 시작 버튼
        ctk.CTkButton(
            timer_card,
            text="시작하기",
            height=45,
            corner_radius=20
        ).pack(pady=(0, 20))

        # ─────────────────────────
        # MUSIC + MESSAGE
        # ─────────────────────────
        mid = ctk.CTkFrame(scroll, fg_color="transparent")
        mid.pack(fill="x", padx=20, pady=10)

        music = ctk.CTkFrame(mid, corner_radius=20, height=110)
        music.pack(side="left", expand=True, fill="both", padx=5)
        music.pack_propagate(False)

        ctk.CTkLabel(
            music,
            text="🎵 오늘의 음악",
            font=("맑은 고딕", 14, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            music,
            text=data["music"]
        ).pack()

        msg = ctk.CTkFrame(mid, corner_radius=20, height=110)
        msg.pack(side="left", expand=True, fill="both", padx=5)
        msg.pack_propagate(False)

        ctk.CTkLabel(
            msg,
            text="💬 오늘의 멘트",
            font=("맑은 고딕", 14, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            msg,
            text=data["message"],
            wraplength=200
        ).pack()

        # ─────────────────────────
        # STATS
        # ─────────────────────────
        stats = ctk.CTkFrame(scroll, corner_radius=20)
        stats.pack(fill="x", padx=25, pady=20)

        ctk.CTkLabel(
            stats,
            text="📊 학습 통계",
            font=("맑은 고딕", 16, "bold")
        ).pack(pady=(15, 10))

        ctk.CTkLabel(stats, text="오늘 공부 시간 : 2시간 15분").pack(pady=3)
        ctk.CTkLabel(stats, text="이번 주 공부 시간 : 11시간 40분").pack(pady=3)
        ctk.CTkLabel(stats, text="평균 집중 시간 : 28분").pack(pady=(3, 15))