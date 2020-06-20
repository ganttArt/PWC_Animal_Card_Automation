import textwrap
from PIL import Image, ImageDraw, ImageFont

def resize_photograph(photo):
    base_width = 360
    width_percentage = base_width / photo.size[0]
    height = int(photo.size[1] * width_percentage)
    return photo.resize((base_width, height), Image.LANCZOS)


def text_generation(animal_description):
    img = Image.new('RGB', (600, 540), color=(255, 255, 255))
    font = ImageFont.truetype("assets/Arial.ttf", 30)

    lines = textwrap.wrap(animal_description, width=42)
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
        line_height = font.getsize(line)[1]
        draw.text(
            (0, y_text),
            line,
            font=font,
            fill=0
        )
        y_text += line_height

    return img


def generate_shelter_info(name, email, phone):
    # define text variable by the amount of information given
    if email and phone:
        text = email + '  ' + phone
    elif email and name:
        text = name + ': ' + email
    elif phone and name:
        text = name + ': ' + phone
    elif email:
        text = 'Shelter: ' + email
    elif phone:
        text = 'Shelter: ' + phone
    elif name:
        text = 'Contact ' + name + ' for more info.'
    else:
        text = 'Contact PawsWithCause for more info.'

    # define text image size
    if len(text) > 40:
        img = Image.new('RGB', (996, 40), color=(255, 255, 255))
    else:
        img = Image.new('RGB', (600, 40), color=(255, 255, 255))

    # draw text onto image
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("assets/Arial.ttf", 30)
    draw.text((0, 0), text, font=font, fill=0)

    return img


def create_card(image, shelter_name, email, phone, description):
    card = Image.new('RGB', (1050, 600), color=(255, 255, 255))

    image = resize_photograph(image)
    card.paste(image, (30, 30))

    text = text_generation(description)
    card.paste(text, (420, 24))

    shelter_info = generate_shelter_info(shelter_name, email, phone)
    if shelter_info.size[0] == 600:
        card.paste(shelter_info, (420, 432))
    else:
        card.paste(shelter_info, (30, 432))

    closing_text = Image.open('assets/closing_text.png')
    card.paste(closing_text, (30, 465))

    return card


def create_pdf(card):
    pdf = Image.new('RGB', (2550, 3300), color=(255, 255, 255))
    y_start = 150
    for _ in range(5):
        pdf.paste(card, (150, y_start))
        pdf.paste(card, (1275, y_start))
        y_start += 600
    return pdf
