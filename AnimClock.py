from datetime import datetime
from LightingControl import LightingControl


# Chevrons to show for specific number positions
dial_lookup = [
    [4],        # 0
    [4, 5],     # 1
    [5, 6],     # 2
    [6],        # 3
    [7],        # 4
    [7, 8],     # 5
    [8, 0],     # 6
    [0, 1],     # 7
    [1],        # 8
    [2],        # 9
    [2, 3],     # 10
    [3, 4],     # 11
    [4]         # 12
]


class AnimClock:
    def __init__(self, light_control):
        self.light_control = light_control
        self.hr = 0
        self.mins = 0

    def animate(self, reset):
        if reset:
            self.hr = -1
            self.mins = -1
            self.light_control.all_off()

        now = datetime.now().time()
        hour = now.hour
        mins = now.minute
        if hour > 12:
            hour -= 12
        mins = int(round(((float(mins) / 59.0) * 12.0)))

        if hour != self.hr or mins != self.mins:
            self.light_control.all_off()
            print('Time: {}:{}, Calc Time: {}:{}'.format(now.hour, now.minute, hour, mins))

            self.show_hr(hour)
            self.hr = hour
            self.show_min(mins)
            self.mins = mins

        return 1

    def show_hr(self, hr):
        for chevron in dial_lookup[hr]:
            self.light_control.light_chevron(chevron)

    def show_min(self, mins):
        for chevron in dial_lookup[mins]:
            LightingControl.chevrons[chevron].blink()
