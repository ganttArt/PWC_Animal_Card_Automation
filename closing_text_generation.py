'''
- Generates the closing text for the card 
- Saves image of text, overwriting previous closing_text.png in the assets folder.

To run from command line:
python3 closing_text_generation.py

Requirements:
PIL/Pillow
Python3
'''

from PIL import Image, ImageDraw, ImageFont


def closing_text():
    pwc_card_info = [
        "Love this portrait? Make a donation through PawsWithCause and it's yours!",
        "T: 206-801-0220 PawsWithCause.org / Proceeds benefit shelter animals.",
        "Join us at the Everett Mall to help paint shelter animals: No experience needed."
    ]
    img = Image.new('RGB', (996, 105), color=(255, 255, 255))
    font = ImageFont.truetype("assets/Arial.ttf", 27)
    draw = ImageDraw.Draw(img)
    y_text = 0
    
    for line in pwc_card_info:
        line_height = font.getsize(line)[1]
        draw.text(
            (0, y_text),
            line,
            font=font,
            fill=(19, 50, 245)
        )
        y_text += line_height
    img.save('assets/closing_text.png')

if __name__ == "__main__":
    closing_text()