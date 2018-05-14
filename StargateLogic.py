from AnimChase import AnimChase
from AnimRing import AnimRing
from AnimClock import AnimClock
from time import sleep


class StargateLogic:
    def __init__(self, audio, light_control, stargate_control, dial_program):
        self.audio = audio
        self.light_control = light_control
        self.stargate_control = stargate_control
        self.dial_program = dial_program
        self.anim_chase = AnimChase(light_control)
        self.anim_ring = AnimRing(light_control)
        self.anim_clock = AnimClock(light_control)
        self.state = 3
        self.address = []
        self.state_changed = True

    def execute_command(self, command):
        self.state_changed = True
        self.state = command['anim']

        if self.state == 2:
            address = command['sequence']
            if len(address) != 7:
                self.state = 0
                return
            self.address = address

        if self.state > 3:
            self.state = 0

    def loop(self):
        while True:
            state_changed = self.state_changed
            self.state_changed = False

            # Call relevant logic depending on state
            if self.state == 2:
                self.light_control.all_off()
                self.dial_program.dial(self.address)
                self.state = 0
            elif self.state == 0:
                delay = self.anim_chase.animate(state_changed)
                sleep(delay)
            elif self.state == 1:
                delay = self.anim_ring.animate(state_changed)
                sleep(delay)
            elif self.state == 3:
                delay = self.anim_clock.animate(state_changed)
                sleep(delay)
            else:
                sleep(1)
