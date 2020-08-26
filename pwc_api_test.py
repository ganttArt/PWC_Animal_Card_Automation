import requests
import json
from PIL import Image
from io import BytesIO

def main():
    response = requests.get('https://pwc-volunteers-backend.herokuapp.com/animals/card_generator/1')
    dictionary = json.loads(response.text)
    print(dictionary['photos'][0]['file_path'])

    response = requests.get('https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48743544/1/?bust=1597119230')
    # print(response.text)
    im = Image.open(BytesIO(response.content))
    im.show()
'''
{"id":1,
 "description":"You can fill out an adoption application online on our official website.Interested in adopting? See our adoption proccess.\nSadie is a lovely adult malamute that wants to be your one and only! She has been well cared for and loved; however, has to find a new home due to an incident with another dog. Other than needing to be an only pet and careful around other dogs, she really has no other issues. She walks well on leash and knows a number of commands - and even follows them quite well on leash and about half the time when not on leash. (The other half of the time off leash she wants to convince us she just didn't hear the commands...oh malamutes!) On walks, she does well with the 'wait' command, though will pull to get to another dog, so needs someone strong enough to keep her from doing that. She enjoys pulling carts, which is good, as she needs exercise to lose a little extra 'fluff'. This friendly girl loves people and has spent time with older children that she did very well with. Sadie enjoys attention and getting pets and belly rubs. She likes to play with toys and will bring a toy over to encourage playtime. Interested in sponsoring? See our sponsorship information.",
 "name":"Sadie",
 "photos":[{"id":1,"file_path":"/Users/joshuaphelps/desktop/pawsdb/48743544_0.jpg","url":"https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48743544/1/?bust=1597119230"},
           {"id":2,"file_path":"/Users/joshuaphelps/desktop/pawsdb/48743544_1.jpg","url":"https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48743544/2/?bust=1597119227"},
           {"id":3,"file_path":"/Users/joshuaphelps/desktop/pawsdb/48743544_2.jpg","url":"https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48743544/3/?bust=1597119232"},
           {"id":205,"file_path":null,"url":"https://drive.google.com/uc?export=view\u0026id=1hVp_SGXOJMV8gPt2SFAhqCkYD1Fx6lIi"}],

 "shelter":{"id":29,
            "external_id":"WA47",
            "name":"WAMAL (Washington Alaska Malamute Adoption League)",
            "address":{"zip":"98201","city":"Spokane","state":"WA","street_address":"1108 W. 2nd Ave, PMB #243"},
            "phone_number":"425-610-6257",
            "email":"wamal@wamal.com",
            "created_at":"2020-08-11T02:41:36.280Z",
            "updated_at":"2020-08-11T02:41:36.280Z"
           }
}
'''
if __name__ == "__main__":
    main()