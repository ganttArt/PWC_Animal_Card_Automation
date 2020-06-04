import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont

#text on image
#afterwards figuring out how to get the image from google photos

SPREADSHEET = 'assets/PWC-Spreadsheet.csv'
PWC_CARD_INFO = [
    "Love this portrait? Make a donation through PawsWithCause and it's yours!",
    "T: 206-801-0220 PawsWithCause.org / All proceeds benefit shelter animals.",
    "Join us at the Everett Mall to help paint shelter animals: No experience needed."
]

def closing_text():
    img = Image.new('RGB', (332, 35), color=(255, 255, 255))
    font = ImageFont.truetype("assets/Arial.ttf", 9)
    draw = ImageDraw.Draw(img)
    y_text = 0
    
    for line in PWC_CARD_INFO:
        line_width, line_height = font.getsize(line)
        draw.text(
            (0, y_text),
            line,
            font=font,
            fill=(19, 50, 245)
        )
        y_text += line_height
    img.save()


def resize_photograph(photo):
    base_width = 120
    width_percentage = base_width / photo.size[0]
    height = int(photo.size[1] * width_percentage)
    return photo.resize((base_width, height), Image.LANCZOS)


def text_generation(animal_description):
    img = Image.new('RGB', (200, 180), color=(255, 255, 255))
    font = ImageFont.truetype("assets/Arial.ttf", 10)
    
    lines = textwrap.wrap(animal_description, width=40)
    if len(lines) > 12:
        line_number = 11
        while line_number > 0:
            if '.' in lines[line_number]:
                split = lines[line_number].split('.')
                lines[line_number] = split[0] + '.'
                break
            elif ';' in lines[line_number]:
                split = lines[line_number].split(';')
                lines[line_number] = split[0] + ';'
                break
            elif '!' in lines[line_number]:
                split = lines[line_number].split('!')
                lines[line_number] = split[0] + '!'
                break
            line_number -= 1
        lines = lines[:line_number + 1]

    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(
            (0, y_text),
            line,
            font=font,
            fill=0
        )
        y_text += line_height

    return img


def create_card(animal_info):
    #need to scale this up to 1050w x 600h. x3 larger
    card = Image.new('RGB', (350, 200), color=(255, 255, 255))

    photograph = Image.open(f'photos/{animal_info[0]}.jpg')
    photograph = resize_photograph(photograph)
    card.paste(photograph, (10, 10))

    text = text_generation(animal_info[2])
    card.paste(text, (140, 8))

    closing_text = Image.open('assets/closing_statement.png')
    card.paste(closing_text, (10, 155))

    return card


def create_pdf(card):
    pdf = Image.new('RGB', (2550, 3300), color=(255, 255, 255))
    y_start = 300
    for _ in range(5):
        pdf.paste(card, (150, y_start))
        pdf.paste(card, (1275 , y_start))
        y_start += 600
    return pdf


def main(spreadsheet):
    with open(spreadsheet) as csvfile:
        animals_spreadsheet = csv.reader(csvfile)

        for animal in animals_spreadsheet:
            card = create_card(animal)
            pdf = create_pdf(card)
            pdf.show()
            # pdf.save(f'{animal[0]}.pdf')


if __name__ == "__main__":
    main(SPREADSHEET)
    # text_generation()
    # closing_text()
