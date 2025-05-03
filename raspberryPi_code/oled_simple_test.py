from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)  

with canvas(device) as draw:
    draw.text((10, 40), "Hello World", fill="white")
    draw.text((10, 70), "from peppe8o.com!", fill="white")

sleep(10)