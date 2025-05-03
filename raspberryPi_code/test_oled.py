import time
import board
import digitalio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Create the I2C bus
i2c = board.I2C()

# Set up the OLED display
oled = SSD1306_I2C(128, 64, i2c)

# Create an image object to draw text
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a default font
font = ImageFont.load_default()

# Clear the display
oled.fill(0)
oled.show()

# Draw text on the image object
draw.text((0, 0), "Hello", font=font, fill=255)

# Display the image with the drawn text
oled.image(image)
oled.show()

# Keep the "Hello" message visible for 5 seconds
time.sleep(5)

# Clear the screen after the delay
oled.fill(0)
oled.show()
