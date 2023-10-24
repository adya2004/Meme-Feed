import  requests

API_URL = "https://api.memegen.link/templates/"


def generate_meme(template_id, top_text, bottom_text):
    top_text = str(top_text)
    bottom_text = str(bottom_text)
    API_URL = "https://api.memegen.link/templates/"
    params = {
    "style": [
        "string"
    ],
    "text": [
        top_text, bottom_text
    ],
    }
    ur = API_URL + str(template_id)

    response = requests.post(ur, data=params)
    data = response.json()
    meme_details = data
    return (data['url'])

def get_templates():
    API_URL = "https://api.memegen.link/templates"
    ids = []
    links = []
    response = requests.get(API_URL)
    data = response.json()
    #meme_details = data
    for temp in data:
        ids.append(temp['id'])
        links.append(temp['blank'])
    return (ids,links)