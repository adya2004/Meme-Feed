import  requests

API_URL = "https://api.memegen.link/templates/"


def generate_meme(template_id, top_text, bottom_text):
    '''This is a function which use template_id, top_text, bottom_text and create a meme using memegen api'''
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
    return (data['url'])

def get_templates():
    '''this function gives list which has dictionary of template_id and image url from memegen api to create memes'''
    API_URL = "https://api.memegen.link/templates"
    ids = []
    links = []
    response = requests.get(API_URL)
    data = response.json()
    for temp in data:
        ids.append(temp['id'])
        links.append(temp['blank'])
        
    lst = []

    for i, j in zip(ids, links):
        lst.append(
            {
                "id" : i,
                "url" : j
            }
        )
    #return a list which contains a dictionary
    return lst


