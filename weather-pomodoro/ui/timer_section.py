from timer.timer import PomodoroTimer


def create_timer_section(
    root,
    focus_time=40,
    break_time=5,
    stats_callback=None
):
    return PomodoroTimer(
        root,
        minutes=focus_time,
        break_minutes=break_time,
        stats_callback=stats_callback
    )