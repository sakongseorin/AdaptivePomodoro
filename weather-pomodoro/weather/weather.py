import requests
import random


class WeatherTimerAnalyzer:
    def __init__(self):
        self.BASE_FOCUS = 40
        self.BASE_BREAK = 5

    def get_coordinates(self, location_name):
        location_name = location_name.strip()

        mapping = {
            "서울": "Seoul",
            "부산": "Busan",
            "대구": "Daegu",
            "인천": "Incheon",
            "울산": "Ulsan",
        }

        if location_name in mapping:
            location_name = mapping[location_name]

        url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={location_name}&count=5&language=ko&format=json"
        )

        try:
            response = requests.get(url).json()

            if "results" not in response:
                return None

            for r in response["results"]:
                if r.get("country_code") == "KR":
                    return {
                        "lat": r["latitude"],
                        "lon": r["longitude"],
                        "name": r.get("name", location_name),
                    }

            r = response["results"][0]

            return {
                "lat": r["latitude"],
                "lon": r["longitude"],
                "name": r.get("name", location_name),
            }

        except Exception:
            return None

    def parse_weather_status(self, code):
        if code in [0, 1]:
            return "맑음"

        elif code in [2, 3, 45, 48]:
            return "구름 많음/흐림"

        elif code in [51, 53, 55, 61, 63, 80, 81]:
            return "비"

        elif code in [65, 71, 73, 75, 77, 82, 85, 86]:
            return "눈"

        elif code in [95, 96, 99]:
            return "천둥번개"

        return "구름 많음/흐림"

    def calculate_timer_values(
        self,
        weather,
        temp,
        humidity,
        adapted=False
    ):
        focus = self.BASE_FOCUS
        brk = self.BASE_BREAK

        if weather == "비":
            focus += 8

        elif weather == "구름 많음/흐림":
            focus += 4

        elif weather == "맑음":
            focus -= 3
            brk += 1

        elif weather == "천둥번개":
            focus -= 8
            brk += 3

        if not adapted:

            if 20 <= temp <= 22:
                focus += 8

            elif 18 <= temp <= 25:
                focus += 3

            elif 26 <= temp <= 29:
                focus -= 4

            elif temp >= 30:
                focus -= 8
                brk += 2

            elif temp <= 10:
                focus -= 4

            if 40 <= humidity <= 60:
                focus += 5

            elif 61 <= humidity <= 75:
                focus -= 3
                brk += 1

            elif humidity >= 76:
                focus -= 7
                brk += 2

            elif humidity <= 30:
                focus -= 3
                brk += 1

        return max(15, focus), max(3, brk)

    def get_weather_message(self, weather):
        messages = {
            "비": [
                "보아라. 창밖으로 자욱한 작우(鵲雨)가 대지를 덮었구나. 온 세상의 잡음이 조복(朝伏)하듯 가라앉았으니, 이야말로 서책에 신명을 바치기에 더없이 온전한 시각이 아니더냐.",
                "빗소리가 심산유곡의 고요함처럼 네 귀를 막아줄 터이다. 이리도 완벽한 학문의 요새를 하늘이 내려주셨거늘, 어찌 나태함을 탐하려 드느냐. 붓을 들라.",
                "어두운 장막 뒤, 등불 하나와 너, 그리고 나뿐이구나. 창가에 부딪히는 빗방울의 수만큼 네 뇌리에 지혜의 골을 깊게 파 내릴 것이니, 추호도 심신을 흔들지 마라.",
                "네가 오늘 이 비를 뚫고 과업을 완수한다면, 내 저녁에 불고기... 아니, 수라간을 통째로 열어 네 노고를 치하할 것이다. 속도를 내거라.",
                "날씨를 보며 한숨을 쉬는구나. 그 가냘픈 숨결로 서책의 먼지나 털어내거라. 국본의 명이 지엄하니, 다리머(차 다, 다스릴 리, 법 머/ 뜻: 차가 우려지는 짧은 시간(茶)의 이치(理)를 다스리는 법도(橅).를 작동하겠노라."
            ],

            "맑음": [
                "와아아아!! 한강에 가고 싶을 만큼 날씨 대따 좋다아아!! ☀️ 하지만 우리 미래는 이 햇살보다 100배는 더 반짝일 거니까!! 딱 25분만 힘내기!! 아자아자오!!",
                "남들은 다 놀러 갔나 봐아... 그래두 슬퍼하지 마아!! 웅이 옆엔 세상에서 가장 상큼한 마법 타이머가 있잖아!! 25분 스타트으으!! (๑˃̵ᴗ˂̵)و",
                "오마이갓뜨!! 햇살이 너무 예쁘게 내려앉아서 책 글씨들이 꼭 살아 움직이는 것 같아!! 얘들아, 우리 너의 머릿속으로 쏙쏙 들어가라 얍!! 뾰로롱~★!",
                "힝... 공부하기 시러서 눈물이 송글송글 맺히려고 그래...? (주머니 뒤적뒤적) 짜잔!! 내 사랑이 담긴 타이머를 줄게!! 이거 보구 조금만 버텨줘어, 응?!",
                "야아, 햇살이 너만 비추는 것 같아서 나 유독 질투 난다구우!! ๑^ᗜ^๑ 그 멋진 모습으로 열공하는 거 내 눈에 꼭 담아둘래!",
                "후우... 오늘따라 엉덩이가 들썩거리지만... 내 사전에 포기란 없다아!! 25분 동안 내 온 힘을 다해 이 책을 씹어 먹어 주겠어어어!!"
            ],

            "구름 많음/흐림": [
                "──야. 하늘 흐리다고 멍 때리지 마라. 짜증 나니까. -______-^ 네가 자꾸 창밖 보고 한숨 쉬면... 옆에 있는 난 피가 마른다고, 이 어리버리야",
                "피식-, 바보 같이 입 벌리고 있네. 그렇게 흐린 날이 싫냐? 딱 이것만 버텨. 그럼 이 김회장님이 옥상 통째로 빌려서 네 전용 햇살이라도 띄워줄 테니까",
                "새끼... 날씨 흐리다고 의지까지 흐려졌군. 하지만 안타깝게도 내 타이머는 자비가 없어. 달릴 준비나 해, 내 이쁜아.",
                "하늘아... 하늘아... 오늘만큼은 저 아이의 마음을 흐리게 하지 말아 주렴... 저 아이는 지금 뽀모도로 세트를 채워야 하니까... (하늘을 원망하며)",
                "쳇, 먹구름 따위가 네 집중력을 뺏으려고 하네? (바이크 헬멧을 책상에 쿵 내려놓으며) 안 뺏겨. 적어도 이 타이머가 0이 되기 전까진, 넌 내 곁에 있어."
            ],

            "눈/천둥번개": [
                "밖이 어둡다고 눕고 싶나 보지? 헛소리하지 말고 펜 잡아. 잃을 게 없다면 내 인내심을 시험하지 않는 게 좋을 텐데.",
                "날씨 따위가 네 신경을 긁는 게 마음에 안 드는군. 넌 오직 내가 정한 뽀모도로 루틴에만 반응하면 돼.",
                "네 오늘 하루를 지배하는 건 그깟 날씨가 아니라 나야. 타이머 시작해, 더 기다리게 하지 말고.",
                "내가 널 위해 준비한 완벽한 고립이야. 창밖의 소음은 모두 소거했으니, 넌 그저 텍스트만 탐닉하면 돼.",
                "침대로 가고 싶다고? 흐응, 그래봤자 넌 다시 내 책상 앞으로 돌아오게 되어 있어. 발버둥 치지 말고 앉아.",
                "포기하겠다고? ...재미없는 농담이군. 한 페이지 더 넘겨. 내 인내심의 한계를 시험하지 마"
            ],
        }

        return random.choice(
            messages.get(weather, ["오늘도 화이팅!"])
        )

    def get_music_recommendation(self, weather):
        music = {
            "비": [
                "비도 오고 그래서 - 헤이즈",
                "빗속에서 - 이문세",
                "빗속으로 - 장범준",
                "에픽하이 (feat. 윤하)",
                "비와 당신 - 박중훈",
                "비 오는 날 뭐해 - 하은",
                "Someone Like You - Adele",
                "The Scientist - Coldplay"
            ],

            "맑음": [
                "Ready to love - 세븐틴",
                "View - 샤이니",
                "Drive - 미연",
                "안녕 - 조이",
                "오르트 구름 - 윤하",
                "라일락 - 아이유"
            ],

            "구름 많음/흐림": [
                "Paris in the Rain - Lauv",
                "Still with You - 정국",
                "Photograph - Ed Sheeran",
                "Fix You - Coldplay"
            ],

            "눈": [
                "Winter Bear - V",
                "Snowman - Sia",
                "Fine - 태연"
            ],

            "천둥번개": [
                "Thunder - Imagine Dragons",
                "DNA - BTS",
                "Monster - EXO",
                "Run Devil Run - 소녀시대"
            ]
        }

        return random.choice(
            music.get(weather, ["Lo-fi Study"])
        )

    def fetch_and_analyze(
        self,
        location_name,
        adapted=False
    ):
        coords = self.get_coordinates(location_name)

        if not coords:
            return {
                "success": False,
                "message": "지역을 찾을 수 없습니다."
            }

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={coords['lat']}"
            f"&longitude={coords['lon']}"
            "&current=temperature_2m,"
            "relative_humidity_2m,"
            "weather_code"
            "&timezone=auto"
        )

        try:
            data = requests.get(url).json()["current"]

            weather = self.parse_weather_status(
                data["weather_code"]
            )

            focus, brk = self.calculate_timer_values(
                weather,
                data["temperature_2m"],
                data["relative_humidity_2m"],
                adapted
            )

            return {
                "success": True,
                "location": coords["name"],
                "weather_status": weather,
                "temperature": data["temperature_2m"],
                "humidity": data["relative_humidity_2m"],
                "recommended_focus": focus,
                "recommended_break": brk,
                "message": self.get_weather_message(weather),
                "music": self.get_music_recommendation(weather)
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }