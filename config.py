from Adafruit_MotorHAT_Motors import Adafruit_MotorHAT

# Configuration for Stargate

# Chevron pins, from bottom-left to bottom-right.
# Index 0 will be bottom-left, 4 will be the top, 8 will be the bottom-right
#
# To work out the chevon pin numbers, create a table, then run ChevonLighting.cycle_chevrons (see in main.py)
#
# 17: 8
# 27: 4
# 22: 6
# 5: 7
# 6: 5
# 13: 3
# 26: 0
# 12: 1
# 16: 2
#
# Enter the LED that lights up after the pin number, in the above example the first LED that lit up
# was the last LED in the gate, '8'. Then te top '4'. And so on.
#
# Once the table is populated, enter the values into the pin array below, following LED order:
# pins_chevron = [17, 27, 22, 5, 6, 13, 26, 12, 16] # Pin order
pins_chevron = [26, 12, 16, 13, 27, 6, 22, 5, 17] # Actual order, COMMENT OUT when figuring out the order

# Pin for the ramp LED
pin_gantry = 24

# Pin for the calibration LED
pin_cal_led = 20

# Pin for the CS of MCP3008 ADC chip
pin_adc_cs = 8

# Motor number 'Mx' for gate
motor_gate = 2

# Motor number 'Mx' for chevron
motor_chevron = 1

# RPM for the motors
motor_rpm = 100

# Drive method for motors
motor_drive = Adafruit_MotorHAT.MICROSTEP

# 'Forward' direction for stargate
gate_forward = Adafruit_MotorHAT.FORWARD

# 'Backward' direction for stargate
gate_backward = Adafruit_MotorHAT.BACKWARD

# 'Forward' direction for chevron
chevron_forward = Adafruit_MotorHAT.FORWARD

# 'Backward' direction for chevron
chevron_backward = Adafruit_MotorHAT.BACKWARD

# Expected minimum value from LDR when in the home position
cal_brightness = 800

# How much brighter the calibration LED is to the LDR vs. baseline as a percentage
cal_percentage = 150

# Number of steps of the motor per full symbol movement
cal_steps_per_symbol = 15.46153846153846 * 2  # x2 because reasons

# Steps for the top chevron lock
steps_chevron_lock = 9

# Number of steps for a full rotation of the gate
num_steps_circle = 603

# Settings you shouldn't need to change

spi_port = 0
spi_device = 0
ldr_index = 0           # Index of the LDR in the ADC chip
cal_num_samples = 10    # Number of LDR samples to get background lighting levels
cal_num_steps = 50      # Number of steps to move gate per sample
home_initial_reverse = cal_steps_per_symbol * 2  # Number of steps to move backwards when performing an initial home
audio_delay_time = 0.2  # Time between playback request, and actual playback

num_symbols = 39
num_chevrons = 9
top_chevron = 4

chevron_light_order = [5, 6, 7, 1, 2, 3, 0, 8]  # Order Chevrons will light up when dialing
chevron_engage_time = 1.5 - audio_delay_time  # Amount of time in seconds that the chevron will remain locked
