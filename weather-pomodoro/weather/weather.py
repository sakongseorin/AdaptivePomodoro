import requests


class WeatherTimerAnalyzer:
    def __init__(self):
        self.BASE_FOCUS = 40
        self.BASE_BREAK = 5

    def get_coordinates(self, location_name):
        location_name = location_name.strip()

        # 🔥 한글 입력 보정
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

            # 🔥 한국 우선 선택
            for r in response["results"]:
                if r.get("country_code") == "KR":
                    return {
                        "lat": r["latitude"],
                        "lon": r["longitude"],
                        "name": r.get("name", location_name),
                    }

            # fallback
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
        elif code in [65, 71, 73, 75, 77, 82, 85, 86, 95, 96, 99]:
            return "폭우/눈/천"
        return "구름 많음/흐림"

    def calculate_timer_values(self, weather, temp, humidity):
        focus = 0
        brk = 0

        if weather == "맑음":
            focus += 5
        elif weather == "비":
            focus -= 5
            brk += 2
        elif weather == "폭우/눈/천":
            focus -= 10
            brk += 5

        if 15 <= temp <= 23:
            focus += 3
        elif temp >= 29 or temp <= 10:
            focus -= 3

        if 61 <= humidity <= 75:
            focus -= 2
            brk += 1
        elif humidity >= 76:
            focus -= 5
            brk += 2

        return max(1, self.BASE_FOCUS + focus), max(1, self.BASE_BREAK + brk)

    def fetch_and_analyze(self, location_name):
        coords = self.get_coordinates(location_name)
        if not coords:
            return {"success": False, "message": "지역을 찾을 수 없습니다."}

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={coords['lat']}&longitude={coords['lon']}"
            "&current=temperature_2m,relative_humidity_2m,weather_code"
            "&timezone=auto"
        )

        try:
            data = requests.get(url).json()["current"]

            weather = self.parse_weather_status(data["weather_code"])
            focus, brk = self.calculate_timer_values(
                weather,
                data["temperature_2m"],
                data["relative_humidity_2m"],
            )

            return {
                "success": True,
                "location": coords["name"],
                "weather_status": weather,
                "temperature": data["temperature_2m"],
                "humidity": data["relative_humidity_2m"],
                "recommended_focus": focus,
                "recommended_break": brk,
            }

        except Exception as e:
            return {"success": False, "message": str(e)}