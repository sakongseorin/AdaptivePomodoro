from timer.timer import PomodoroTimer


def create_timer_section(root):
    timer = PomodoroTimer(root)
    timer.pack(pady=36)
    return timer