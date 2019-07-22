import requests


def get_spaceship_data():
    page = 0
    content = []
    while True:
        page += 1
        page_content, is_there_next_page = _get_content_from_page(page)
        content.extend(page_content)
        if not is_there_next_page:
            break
    return content


def _get_content_from_page(page_number):
    url = 'https://swapi.co/api/starships/'
    r = requests.get(url, params={'page': page_number})
    page_content = r.json()
    return _parse_page_content(page_content), bool(page_content['next'])


def _parse_page_content(page_content):
    """Returns the needed content from the given page"""
    return [
        # List of dicts with name and hyperdrive
        {'name': x['name'], 'hyperdrive': x['hyperdrive_rating']}
        for x in page_content['results']
    ]
