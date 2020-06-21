import os
import io
from datetime import datetime
from PIL import Image, UnidentifiedImageError
from flask import Flask, render_template, request, send_file
from card_generation_functions import create_card, create_pdf


APP = Flask(__name__)
# app.secret_key = b'\xd6\x13\x02\xd1-\xa6\x04\x8c!K478\xdfr^\xbd\x0b\xc62\xf7q\xe1\x98'
# app.secret_key = os.environ.get('SECRET_KEY').encode()


@APP.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        try:
            image = Image.open(request.files['file'])
        except UnidentifiedImageError as ex:
            print(ex)
            return render_template('main.jinja2', error='Image error: Please try again.')

        shelter_name = request.form['shelter_name']
        shelter_email = request.form['shelter_email']
        shelter_phone = request.form['shelter_phone']
        animal_description = request.form['description']

        card = create_card(image, shelter_name, shelter_email, shelter_phone, animal_description)
        pdf = create_pdf(card)

        output = io.BytesIO()
        pdf.convert('RGB').save(output, format='PDF')
        output.seek(0, 0)
        return send_file(output, mimetype='application/pdf', as_attachment=False)
    else:
        return render_template('main.jinja2')


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    APP.run(host='0.0.0.0', port=PORT, debug=True)
