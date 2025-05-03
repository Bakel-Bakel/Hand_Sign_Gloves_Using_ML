import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# OLED setup (128x64)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
oled.fill(0)
oled.show()

# Create image buffer
image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)

# Load the default font
font = ImageFont.load_default()

# Draw the text "Hello" at the top-left corner
draw.text((0, 0), "We are BME of 25", font=font, fill=255)

# Display the image with the drawn text
oled.image(image)
oled.show()

# Keep the "Hello" message visible for 5 seconds
time.sleep(5)

# Clear the display after the delay
oled.fill(0)
oled.show()
