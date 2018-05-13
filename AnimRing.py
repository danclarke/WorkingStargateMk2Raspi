from time import sleep
import config


class AnimRing:
    def __init__(self, light_control):
        self.light_control = light_control
        self.current_chevron = 0

    def animate(self, reset):
        if reset:
            self.current_chevron = 0
            self.light_control.all_off()

        self.light_control.light_chevron(self.current_chevron)
        sleep(0.02)

        if self.current_chevron > 0:
            self.light_control.darken_chevron(self.current_chevron - 1)
        else:
            self.light_control.darken_chevron(config.num_chevrons - 1)

        self.current_chevron += 1
        if self.current_chevron >= config.num_chevrons:
            self.current_chevron = 0

        return 0.12
