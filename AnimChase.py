import config


class AnimChase:
    def __init__(self, light_control):
        self.light_control = light_control
        self.current_chevron = 0
        self.current_state = 0

    def animate(self, reset):
        if reset:
            self.current_chevron = 0
            self.current_state = 0
            self.light_control.all_off()

        if self.current_state == 0:
            self.light_control.light_chevron(self.current_chevron)
            self.current_chevron += 1
            if self.current_chevron >= config.num_chevrons:
                self.current_chevron = 0
                self.current_state = 1

        elif self.current_state == 1:
            self.light_control.darken_chevron(self.current_chevron)
            self.current_chevron += 1
            if self.current_chevron >= config.num_chevrons:
                self.current_chevron = config.num_chevrons - 1
                self.current_state = 2

        elif self.current_state == 2:
            self.light_control.light_chevron(self.current_chevron)
            self.current_chevron -= 1
            if self.current_chevron < 0:
                self.current_chevron = config.num_chevrons - 1
                self.current_state = 3

        elif self.current_state == 3:
            self.light_control.darken_chevron(self.current_chevron)
            self.current_chevron -= 1
            if self.current_chevron < 0:
                self.current_chevron = 0
                self.current_state = 0

        else:
            self.current_chevron = 0
            self.current_state = 0
            return 0

        return 0.25
