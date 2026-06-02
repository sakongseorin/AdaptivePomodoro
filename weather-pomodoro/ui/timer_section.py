from timer.timer import PomodoroTimer


def create_timer_section(root):
    timer_section = PomodoroTimer(root)
    timer_section.pack(pady=35)
    return timer_section
