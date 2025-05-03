import time
import board
import digitalio
from adafruit_ssd1306 import SSD1306_I2C
from adafruit_display_shapes.rect import Rect
import adafruit_displayio

# Create the I2C bus
i2c = board.I2C()

# Set up the OLED display
oled = SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.fill(0)
oled.show()

# Create text to display
oled.text("Hello", 0, 0)  # "Hello" at the top-left corner (x=0, y=0)
oled.show()

# Add a delay to keep the message visible
time.sleep(5)  # Display "Hello" for 5 seconds
