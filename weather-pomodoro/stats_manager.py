import json
import os
from datetime import datetime, timedelta


class StatsManager:
    FILE_NAME = "study_stats.json"

    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load(self):
        with open(self.FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def record_session(self, minutes):
        data = self.load()

        today = datetime.now().strftime("%Y-%m-%d")

        if today not in data:
            data[today] = {
                "minutes": 0,
                "sessions": 0
            }

        data[today]["minutes"] += minutes
        data[today]["sessions"] += 1

        self.save(data)

    def get_today_minutes(self):
        data = self.load()

        today = datetime.now().strftime("%Y-%m-%d")

        if today not in data:
            return 0

        return data[today]["minutes"]

    def get_today_sessions(self):
        data = self.load()

        today = datetime.now().strftime("%Y-%m-%d")

        if today not in data:
            return 0

        return data[today]["sessions"]

    def get_total_minutes(self):
        data = self.load()

        total = 0

        for day in data.values():
            total += day["minutes"]

        return total

    def get_week_minutes(self):
        data = self.load()

        total = 0

        for i in range(7):
            date = (
                datetime.now() - timedelta(days=i)
            ).strftime("%Y-%m-%d")

            if date in data:
                total += data[date]["minutes"]

        return total