import time
import board
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Initialize the I2C bus
i2c = board.I2C()

# Set up the OLED display (128x64 resolution) with I2C address 0x3C
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Create an image object to draw text
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load the default font
font = ImageFont.load_default()

# Clear the display
oled.fill(0)
oled.show()

# Draw text on the image object (display "Hello")
draw.text((0, 0), "Hello", font=font, fill=255)

# Display the image with the drawn text
oled.image(image)
oled.show()

# Keep the "Hello" message visible for 5 seconds
time.sleep(5)

# Clear the screen after the delay
oled.fill(0)
oled.show()
