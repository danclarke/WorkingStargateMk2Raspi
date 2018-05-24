# Working Stargate Mk2 Control Code with Raspberry Pi

Control code for [Glitch's Working Stargate Mk2](https://www.thingiverse.com/thing:1603423) via a web browser.

**Warning:** Do not attempt this build if you don't have a rudimentary understanding of electronics and Linux. This build involves surface-mount soldering, updating of Python files, and basic configuration of Linux via command line. There is no GUI.

## Requirements
- Raspberry Pi 3
- [Adafruit Motor Hat](https://www.adafruit.com/product/2348)
- [Adafruit I2S 3W Breakout](https://www.adafruit.com/product/3006)
- [Custom PCB](https://easyeda.com/boogleoogle/Stargate-HAT) with associated components
- 2.5" Speaker
- 12V DC Adapter
- Everything else required by the standard build from Glitch, unless replaced above

### Motor HAT
The HAT will be stacked directly on top of the Rasperry Pi, with the custom PCB on top. This means pass-through stacking headers will need to be used on the HAT. I used [C35165](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20P_C35165.html) from LCSC.

### Custom PCB

The [custom PCB](https://easyeda.com/boogleoogle/Stargate-HAT) has all connections and required components marked in the silkscreen. The following components are required to be soldered directly to the PCB:

 - 11x BC847 SOT23 [C8547](https://lcsc.com/product-detail/Transistors-NPN-PNP_BC847A-1E_C8574.html)
 - 10x 470ohm 0805 Resistor [C114747](https://lcsc.com/product-detail/Chip-Resistor-Surface-Mount_470R-471-5_C114747.html)
 - 2x 10k ohm 0805 Resistor [C84376](https://lcsc.com/product-detail/Chip-Resistor-Surface-Mount_10KR-1002-1_C84376.html)
 - 1x [LM2596S Buck Converter Breakout](https://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=140_171&products_id=3202)
 - 1x [MCP3008](https://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=140_166&products_id=2274)
 - Optional 1x [16-pin DIL Socket](https://www.bitsbox.co.uk/index.php?main_page=product_info&cPath=255_256&products_id=1933)
 - 1x 5mm 2-pin terminal [C3703](https://lcsc.com/product-detail/Terminal-Blocks_WJ127-5-0-2P_C3703.html)
 - 1x 2.54mm 7-pin female header [C124418](https://lcsc.com/product-detail/Female-Header_Shenzhen-Cancome-Female-header-1-7P-2-54mm-Straight-line_C124418.html)
 - 1x 2.54mm 2x20 female header [C50982](https://lcsc.com/product-detail/Female-Header_2-54mm-2-20PFemale-header_C50982.html)

The board will be at the top of the stack, so you can use standard female header/socket. Power is provided by this board, no need to connect power to the Raspberry Pi directly.

#### Pinouts

| Pin | Item |
| :---: | :---: |
| GPIO17 | Chevron 1 |
| GPIO27 | Chevron 2 |
| GPIO22 | Chevron 3 |
| GPIO5 | Chevron 4 |
| GPIO6 | Chevron 5 |
| GPIO13 | Chevron 6 |
| GPIO26 | Chevron 7 |
| GPIO12 | Chevron 8 |
| GPIO16 | Chevron 9 |
| GPIO24 | Ramp LEDs |
| GPIO20| Calibration LED |
| GPIO19 | Audio LRCLK |
| GPIO18 | Audio BCLK |
| GPIO21 | Audio DIN |
| GPIO8 | MCP3008 CS |
| GPIO10 | MOSI |
| GPIO9 | MISO |
| GPIO11 | SCLK |

Chevron ordering does not matter since it will be corrected in software.

#### Connections

Prior to soldering anything, connect the LM2596S Buck Converter to 12V power and adjust the potentiometer until 5.1v is at the output terminals. Next set up the Raspberry Pi for SSH so that the Pi can be configured without direct physical access. Once this is done you can continue.

Solder the LM2596S Buck Converter directly onto the PCB using any wire to hand such as the offcuts from LEDs. Use the 12V-2 headers to run 12V lines to the 12V input of the Motor HAT. Power is provided via the LM2596S, so do not connect USB power directly to the Raspberry Pi. When soldering the LM2596S, ensure the bottom part (Output) is flush with the PCB. Due to some of the through-hole components the entire board can't be flush, but it's important the lower part is. The top part (Input) can stand slightly proud since there's more space between it and the ramp.

For connections to the LEDs and LDR I used LED strip JST connectors.

The Raspberry Pi itself fits, at a very slightly skewed angle, to the two left-most screw holes in the base. From there, all of the boards can stack on top.

### LEDs
The chevron LEDs are all powered via 12V, with ground going to the custom PCB. Resistors are already on the board. The calibration LED is also powered via 12V, with ground to the board. **The LDR must be powered via 3.3v, not 12v**.

Finally the Ramp / Gantry LEDs can be wired in series on each side, with no resistor. The 12v divided by the 4 LEDs results in 3V to each LED. This should nicely dim the white LEDs resulting in a well-lit but not overwhelmingly bright ramp. Ground should go to the custom PCB. This is also significantly easier to wire up than a resistor and power line to each individual LED. If your LEDs can't be lit with 3v, you'll need to customise your wiring and potentially add in some resistors.

I used 1206 surface mount LEDs from [Bright Components](http://bright-components.co.uk/), however any LED of the right colour will work. For example [C110588](https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_LED-26-21-UYC-S530-A3-TR8_C110588.html) and [C71796](https://lcsc.com/product-detail/Light-Emitting-Diodes-LED_white1206-Non-warm-tones-of-white_C71796.html) from LCSC will probably work fine too. The 1206 form factor is much easier to solder than the 0604s used in Glitch's original instructions and fit fine.

Be very careful of the pads on the LEDs, they're very easy to rip off in this application. Ensure all wires have strain relief to prevent a pad from being accidentally ripped off. I used small dots of hotmelt glue to hold wires in place. Be very careful with hotmelt and PLA since it will soften and even melt the PLA.

### Rasperry Pi Setup

First install a fresh copy of Raspbian Lite, configure the Pi for SSH and continue configuration via an SSH terminal. Remote SSH access is important so that the Pi can be updated / changed without having to disassemble the ramp.

Set a static IP by running:

`sudo nano /etc/dhcpcd.conf`

Follow the instructions in the file to set a static IP. For me I used the following configuration:

```
interface wlan0
static ip_address=192.168.0.34/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1 8.8.8.8
```

Next get the required packages:

```
sudo apt update
sudo apt install python python-pip python-gpiozero build-essential git python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
```

Next install the required Python packages:

`sudo pip install Adafruit-MCP3008 pygame gpiozero`

Update the I2C speed of the Raspberry Pi to 400Khz (400000): http://www.mindsensors.com/blog/how-to/change-i2c-speed-with-raspberry-pi

Finally, follow Adafruit's instructions for the I2S Breakout: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage

Create a folder for the Stargate in the home directory:

`mkdir stargate`

Copy all of the Python files here.

### Code Setup

Open main.py and comment out `stargate_control.quick_calibration()`, and the entire Web Control section. Uncomment `light_control.cycle_chevrons()`.

Open config.py and follow the instructions for figuring out the chevron lighting order. Update the array with the results.

To run the program execute `sudo python main.py` in the stargate directory.

After you've executed the full calibration, update config.py with the values found. The calibration values all start with **cal_**.

When you've gone through all steps and updated config.py to your liking, you can uncomment the web control section. Go to http://192.168.0.34 to control your Stargate.

If you're happy with how the Stargate works, you can now set the program to auto-run:

### Auto-Run

You can use [Daemon tools](https://samliu.github.io/2017/01/10/daemontools-cheatsheet.html) to ensure the Python program runs at boot.

First ensure the Python program isn't running, then execute following commands:

```
sudo apt install daemontools daemontools-run
sudo mkdir /etc/service/stargate
sudo nano /etc/service/stargate/run
```

In Nano enter the following text:

```
#!/bin/bash
cd /home/pi/stargate
exec /usr/bin/python main.py
```

Save the file, then execute the following:

`sudo chmod u+x /etc/service/stargate/run`

The Python program should immediately start running. You can now control the Stargate via web browser as soon as the Raspberry Pi boots.
