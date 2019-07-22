import requests


def get_spaceship_data():
    page = 0
    url = 'https://swapi.co/api/starships/'
    content = []
    while True:
        page += 1
        r = requests.get(url, params={'page': page})
        page_content = r.json()
        content.extend([
            {'name': x['name'], 'hyperdrive': x['hyperdrive_rating']}
            for x in page_content['results']
        ])
        if not page_content['next']:
            break
    return content
