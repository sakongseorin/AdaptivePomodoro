from timer.timer import PomodoroTimer


def create_timer_section(root, focus_time=25, break_time=5):
    timer = PomodoroTimer(
        root,
        minutes=focus_time,
        break_minutes=break_time
    )

    timer.pack(pady=36)

    return timer