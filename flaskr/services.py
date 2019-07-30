import requests


def get_spaceship_data():
    """Gets from SWAPI the data from spaceships and returns in the asked form
    """
    page = 0
    content = []
    while True:
        page += 1
        page_content, is_there_next_page = _get_content_from_page(page)
        content.extend(page_content)
        if not is_there_next_page:
            break
    return _classify_spaceships_for_having_hyperdrive(content)


def _get_content_from_page(page_number):
    """Gets formatted content from a page and returns a json and a boolean
    informing if exists any other page
    """
    url = 'https://swapi.co/api/starships/'
    r = requests.get(url, params={'page': page_number})
    page_content = r.json()
    return _parse_page_content(page_content), bool(page_content['next'])


def _parse_page_content(page_content):
    return [
        # List of dicts with name and hyperdrive
        {'name': x['name'], 'hyperdrive': x.get('hyperdrive_rating', '')}
        for x in page_content['results']
    ]


def _classify_spaceships_for_having_hyperdrive(content):
    with_hyperdrive = filter(_is_hyperdrive_known, content)
    without_hyperdrive = [{'name': c['name']} for c in content if not _is_hyperdrive_known(c)]
    return {
        'starships': sorted(with_hyperdrive, key=_get_hyperdrive),
        'starships_unknown_hyperdrive': without_hyperdrive
    }


def _is_hyperdrive_known(starship):
    return starship['hyperdrive'] != 'unknown'


def _get_hyperdrive(starship):
    return starship['hyperdrive']
