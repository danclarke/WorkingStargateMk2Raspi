#!/usr/bin/env python

from Daemon import Daemon
from LightingControl import LightingControl
from StargateControl import StargateControl
from DialProgram import DialProgram
from StargateAudio import StargateAudio
from StargateLogic import StargateLogic
from WebServer import StargateHttpHandler
from BaseHTTPServer import HTTPServer
import threading
import sys

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
logic = StargateLogic(audio, light_control, stargate_control, dial_program)

# Run this FIRST to get the chevron lighting order
# lightControl.cycle_chevrons()

# Run this SECOND to get the best drive method
# stargateControl.drive_test()

# Run this THIRD to get core calibration settings
# stargateControl.full_calibration()

# Run this NORMALLY to home the gate at start up
stargate_control.quick_calibration()

# Run this to TEST the dial sequence
# dialProgram.dial([26, 6, 14, 31, 11, 29, 0])

# Background running in Daemon


class StargateDaemon(Daemon):
    def run(self):
        while True:
            # Web control
            print('Running web server...')
            StargateHttpHandler.logic = logic
            httpd = HTTPServer(('', 80), StargateHttpHandler)

            httpd_thread = threading.Thread(name="HTTP", target=httpd.serve_forever)
            httpd_thread.setDaemon(True)
            httpd_thread.start()

            # Infinite loop doing stuff
            print('Running logic...')
            logic.loop()


if __name__ == "__main__":
        daemon = StargateDaemon('/tmp/daemon-stargate.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
