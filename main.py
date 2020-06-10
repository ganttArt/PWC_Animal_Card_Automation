import os
import csv
import textwrap
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request

app = Flask(__name__)

def closing_text():
    pwc_card_info = [
        "Love this portrait? Make a donation through PawsWithCause and it's yours!",
        "T: 206-801-0220 PawsWithCause.org / All proceeds benefit shelter animals.",
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
    img.save('closing_statment.png')


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
    card = Image.new('RGB', (1050, 600), color=(255, 255, 255))

    photograph = Image.open(f'photos/{animal_info[0]}.jpg')
    photograph = resize_photograph(photograph)
    card.paste(photograph, (30, 30))

    text = text_generation(animal_info[2])
    card.paste(text, (420, 24))

    closing_text = Image.open('assets/closing_statement.png')
    card.paste(closing_text, (30, 465))

    return card


def create_pdf(card):
    pdf = Image.new('RGB', (2550, 3300), color=(255, 255, 255))
    y_start = 150
    for _ in range(5):
        pdf.paste(card, (150, y_start))
        pdf.paste(card, (1275 , y_start))
        y_start += 600
    return pdf


# def main(spreadsheet):
#     with open(spreadsheet) as csvfile:
#         animals_spreadsheet = csv.reader(csvfile)

#         for animal in animals_spreadsheet:
#             card = create_card(animal)
#             pdf = create_pdf(card)
#             pdf.show()
#             pdf.save(f'{animal[0]}.pdf')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return render_template('generated_pdf.jinja2')
    else:
        return render_template('main.jinja2')


@app.route('/generated_card/')
def generated_pdf():
    return render_template('generated_pdf.jinja2')



if __name__ == "__main__":
    # main('assets/PWC-Spreadsheet.csv')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)