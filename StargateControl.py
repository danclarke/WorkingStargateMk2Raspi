from Adafruit_MotorHAT_Motors import Adafruit_MotorHAT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from gpiozero import LED
import config


class StargateControl:
    FORWARD = 0
    BACKWARD = 1

    cal_led = LED(config.pin_cal_led)
    cal_brightness = config.cal_brightness
    adc = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(config.spi_port, config.spi_device))
    mh = Adafruit_MotorHAT()
    motor_gate = mh.getStepper(200, config.motor_gate)
    motor_chevron = mh.getStepper(200, config.motor_chevron)

    def __init__(self, lighting):
        self.lighting = lighting
        self.motor_gate.setSpeed(config.motor_rpm)
        self.motor_chevron.setSpeed(config.motor_rpm)
        self.current_symbol = 0
        self.steps_per_symbol = config.cal_steps_per_symbol

        self.cal_led.off()

    # Perform a full calibration to get all relevant data for reliable operation
    def full_calibration(self):
        print('Performing full calibration')
        self.cal_brightness = self.get_target_cal_brightness()

        # Count how many steps to move around the entire gate
        self.move_home()
        self.cal_led.on()

        # Initially move away from home position so we don't see the home light and think
        # it's 0 steps for a full revolution
        self.motor_gate.step(5, config.gate_forward, config.motor_drive)
        step = 5

        # Count loop steps
        while True:
            self.motor_gate.step(1, config.gate_forward, Adafruit_MotorHAT.MICROSTEP)
            step += 1
            ldr = self.get_ldr_val()
            print("LDR: {}".format(ldr))
            if ldr > self.cal_brightness:
                break

            self.display_progress(step, config.num_steps_circle)

        if step < 20:
            raise ValueError('ERROR!!! TOO FEW STEPS DETECTED: {}'.format(step))

        # Success
        self.lighting.all_off()
        self.cal_led.off()
        # Absolutely no idea why this is off by a factor of 2...
        self.steps_per_symbol = (float(step) / float(config.num_symbols)) * 2.0
        print('Num steps: {}'.format(step))
        print('Steps per symbol: {:f}'.format(self.steps_per_symbol))
        self.current_symbol = 0
        self.release_motor(self.motor_gate)
        print('Full calibration complete')

    def quick_calibration(self):
        print('Performing Quick Calibration')
        self.lighting.all_off()
        self.move_home()

    def drive_test(self):
        print('Single Drive')
        self.motor_gate.step(200, config.gate_forward, Adafruit_MotorHAT.SINGLE)

        print('Double Drive')
        self.motor_gate.step(200, config.gate_forward, Adafruit_MotorHAT.DOUBLE)

        print('Interleave Drive')
        self.motor_gate.step(200, config.gate_forward, Adafruit_MotorHAT.INTERLEAVE)

        self.release_motor(self.motor_gate)

    # Move to the home position, with Earth symbol at the top
    def move_home(self):
        print('Moving to home')
        self.cal_led.on()

        # Initially move a few symbols 'backward' to see if we've got a small overrun,
        # this is the 'normal' situation if the gate has been used
        current_step = 0
        ldr_val = self.get_ldr_val()
        print('LDR: {}, Threshold: {}'.format(ldr_val, self.cal_brightness))

        print('Initial quick reverse scan')
        while self.get_ldr_val() < self.cal_brightness:
            self.motor_gate.step(1, config.gate_backward, Adafruit_MotorHAT.MICROSTEP)
            current_step += 1

            # Didn't find the home position, go back to where we were (more or less)
            # and continue the search
            if current_step > config.home_initial_reverse:
                self.motor_gate.step(int(config.home_initial_reverse - 2), config.gate_forward, config.motor_drive)
                break

        # If previous find worked, LDR will still be lit up and this loop won't execute
        # Otherwise scan the entire gate
        print('Full scan')
        current_step = 0
        while self.get_ldr_val() < self.cal_brightness:
            current_step += 1
            self.motor_gate.step(1, config.gate_forward, Adafruit_MotorHAT.MICROSTEP)
            self.display_progress(current_step, config.num_steps_circle)

        # Now in home position, turn off lighting and set current symbol to 'home'
        print('At home position, LDR value: {}'.format(self.get_ldr_val()))
        self.release_motor(self.motor_gate)
        self.lighting.all_off()
        self.cal_led.off()
        self.current_symbol = 0

    # Move to a specific symbol on the gate
    def move_to_symbol(self, index, direction):
        motor_direction = config.gate_forward
        delta = 0

        if direction == self.FORWARD:
            if index >= self.current_symbol:
                delta = index - self.current_symbol
            else:
                delta = (config.num_symbols - self.current_symbol) + index
        else:
            motor_direction = config.gate_backward
            if index <= self.current_symbol:
                delta = self.current_symbol - index
            else:
                delta = self.current_symbol + (config.num_symbols - index)

        num_steps = int(round(float(delta) * float(self.steps_per_symbol)))

        print('Index: {}, Direction: {}, Delta: {}, Steps: {}'.format(index, motor_direction, delta, num_steps))
        self.current_symbol = index;
        self.motor_gate.step(num_steps, motor_direction, config.motor_drive)
        self.release_motor(self.motor_gate)

    def lock_chevron(self, light=True):
        if light:
            self.lighting.light_chevron(config.top_chevron)

        self.motor_chevron.step(config.steps_chevron_lock, config.chevron_forward, config.motor_drive)
        self.release_motor(self.motor_chevron)

    def unlock_chevron(self, light=True):
        if light:
            self.lighting.darken_chevron(config.top_chevron)

        self.motor_chevron.step(config.steps_chevron_lock, config.chevron_backward, config.motor_drive)
        self.release_motor(self.motor_chevron)

    def is_at_home(self):
        self.cal_led.on()
        at_home = self.get_ldr_val() > self.cal_brightness
        self.cal_led.off()

        return at_home

    # Get the target brightness for the LDR based on real-life values
    def get_target_cal_brightness(self):
        self.cal_led.on()

        # Initial read at current position
        brightness = self.get_ldr_val()
        print('Read in {}'.format(brightness))

        # Gather brightness samples
        for i in xrange(config.cal_num_samples):
            self.display_progress(i, config.cal_num_samples)
            val = self.get_ldr_val()
            print('Read in {}'.format(brightness))

            brightness += val
            self.motor_gate.step(config.cal_num_samples, config.gate_forward, config.motor_drive)

        self.lighting.all_off()
        self.cal_led.off()
        self.release_motor(self.motor_gate)
        average = brightness / config.cal_num_samples + 1
        print("Average: {:f}".format(average))

        target_val = average + ((average / 100) * config.cal_percentage)
        print("Target val: {}".format(target_val))
        return target_val

    # Get the current LDR reading
    def get_ldr_val(self):
        return self.adc.read_adc(config.ldr_index)

    # Display progress of something
    def display_progress(self, step, max_count):
        print('Progress, step: {}, max: {}'.format(step, max_count))
        progress = float(step) / float(max_count)
        self.display_progress_percent(progress)

    # Display % of something
    def display_progress_percent(self, percent):
        if percent > 1:
            percent = 1

        print('Percent: {:f}'.format(percent))
        num_leds = int(round(percent * 9))
        print('Num LEDS: {}'.format(num_leds))
        self.lighting.all_off()
        for chevron in xrange(num_leds):
            self.lighting.light_chevron(chevron)

    # Adafruit haven't added a 'release' method to the library for steppers
    # So use the 'public everything' Python feature to do it here
    # The Arduino library DOES have a release method
    def release_motor(self, motor):
        motor.MC.setPin(motor.AIN1, 0)
        motor.MC.setPin(motor.AIN2, 0)
        motor.MC.setPin(motor.BIN1, 0)
        motor.MC.setPin(motor.BIN1, 0)
