import os
import io
import requests
import json
from datetime import datetime
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from flask import Flask, render_template, request, send_file
from werkzeug.exceptions import BadRequestKeyError
from card_generation_functions import create_card, create_pdf


app = Flask(__name__)


def load_shelters():
    """
        Makes a request to pwc database to get all shelter information.
        Returns a dictionary where the Key = Shelter name, and Value = {'phone_number', 'email'}
    """
    shelters = {}
    response = requests.get('https://pwc-volunteers-backend.herokuapp.com/shelters')
    shelter_list = json.loads(response.text)

    for shelter in shelter_list:
        shelters[shelter['name']] = {'phone_number': shelter['phone_number'], 'email': shelter['email']}

    return shelters


@app.route('/', methods=['GET', 'POST'])
def animal_id_entry():
    if request.method == 'POST':
        try:
            animal_id = int(request.form['animal_id'])
            animal_info = requests.get(f'https://pwc-volunteers-backend.herokuapp.com/animals/card_generator/{animal_id}')
            if animal_info.text == '':
                return render_template('animal_id_entry.jinja2', error='Animal ID is not in PWC database')
        except ValueError as ex:
            print(ex)
            return render_template('animal_id_entry.jinja2', error='Animal ID must be a number')
        
        animal_info = json.loads(animal_info.text)

        shelter_name = animal_info['shelter']['name']
        shelter_email = animal_info['shelter']['email']
        shelter_phone = animal_info['shelter']['phone_number']
        animal_description = animal_info['description']
        
        image = requests.get(animal_info['photos'][0]['url'])
        image = Image.open(BytesIO(image.content))
        
        card = create_card(image, shelter_name, shelter_email, shelter_phone, animal_description)
        pdf = create_pdf(card)

        output = io.BytesIO()
        pdf.convert('RGB').save(output, format='PDF')
        output.seek(0, 0)
        return send_file(output, mimetype='application/pdf', as_attachment=False)
    else:
        return render_template('animal_id_entry.jinja2')


@app.route('/manual_entry', methods=['GET', 'POST'])
def manual_entry():
    SHELTERS = load_shelters()
    if request.method == 'POST':
        try:
            image = Image.open(request.files['file'])
            shelter_name = request.form['shelter']
        except UnidentifiedImageError as ex:
            print(ex)
            return render_template('manual_entry.jinja2', error='Image error: Please try again.', shelters=SHELTERS)
        except BadRequestKeyError as ex:
            print(ex)
            return render_template('manual_entry.jinja2', error='Please choose a shelter, and try again.', shelters=SHELTERS)

        shelter_email = SHELTERS[shelter_name]['email']
        shelter_phone = SHELTERS[shelter_name]['phone_number']
        animal_description = request.form['description']

        card = create_card(image, shelter_name, shelter_email, shelter_phone, animal_description)
        pdf = create_pdf(card)

        output = io.BytesIO()
        pdf.convert('RGB').save(output, format='PDF')
        output.seek(0, 0)
        return send_file(output, mimetype='application/pdf', as_attachment=False)
    else:
        print('get request')
        return render_template('manual_entry.jinja2', shelters=SHELTERS)


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=PORT, debug=True)    
