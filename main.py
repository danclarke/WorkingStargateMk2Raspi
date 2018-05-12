from LightingControl import LightingControl
from StargateControl import StargateControl
from DialProgram import DialProgram
from StargateAudio import StargateAudio
from WebServer import StargateHttpHandler
from BaseHTTPServer import HTTPServer

#
# Working Stargate Mk2 by Glitch, code by Dan Clarke
# Adafruit motor library changes by hendrikmaus, pootle and shrkey
# These changes have a *substantial* impact on the Adafruit motor drive, allowing for high-speed microstep driving
# Raspberry Pi I2C speed must be 400000 (400Khz):
# http://www.mindsensors.com/blog/how-to/change-i2c-speed-with-raspberry-pi

# Packages needed:
# gpiozero, pygame, Adafruit_MCP3008
#

#
# *** DON'T FORGET TO EDIT CONFIG.PY ***
#

# Stargate components
audio = StargateAudio()
light_control = LightingControl()
stargate_control = StargateControl(light_control)
dial_program = DialProgram(stargate_control, light_control, audio)

# Run this FIRST to get the chevron lighting order
# lightControl.cycle_chevrons()

# Run this SECOND to get the best drive method
# stargateControl.drive_test()

# Run this THIRD to get core calibration settings
# stargateControl.full_calibration()

# Run this NORMALLY to home the gate at start up
stargate_control.quick_calibration()

# Web control

# Assign dependencies to handler, globally
StargateHttpHandler.dial_program = dial_program

print('Running web server...')
httpd = HTTPServer(('', 80), StargateHttpHandler)
httpd.serve_forever()

#dialProgram.dial([26, 6, 14, 31, 11, 29, 0])
