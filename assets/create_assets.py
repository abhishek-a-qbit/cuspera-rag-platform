"""
Create placeholder assets for the application
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create a simple logo
def create_logo():
    # Create a new image with transparent background
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a gradient circle as logo
    for i in range(100, 0, -1):
        color = (102, 126, 234, 255)  # Blue color
        draw.ellipse([100-i, 100-i, 100+i, 100+i], fill=color)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "6s"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (200 - text_width) // 2
    y = (200 - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    img.save('logo.png')
    print("Logo created: logo.png")

# Create a simple background pattern
def create_background():
    # Create a gradient background
    img = Image.new('RGB', (1920, 1080), (0, 0, 0))
    pixels = img.load()
    
    for y in range(img.height):
        for x in range(img.width):
            # Create a gradient
            r = int(102 + (118 - 102) * (x / img.width))
            g = int(126 + (75 - 126) * (x / img.width))
            b = int(234 + (162 - 234) * (x / img.width))
            pixels[x, y] = (r, g, b)
    
    # Add some subtle patterns
    draw = ImageDraw.Draw(img)
    for i in range(0, img.width, 100):
        for j in range(0, img.height, 100):
            draw.ellipse([i, j, i+50, j+50], outline=(255, 255, 255, 20), width=2)
    
    img.save('background.png')
    print("Background created: background.png")

if __name__ == "__main__":
    create_logo()
    create_background()
