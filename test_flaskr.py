import json
from unittest import TestCase, mock


from flaskr import app, services


def setup_client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    return client


def patch_get_with_multiple_pages(*args, **kwargs):
    get = mock.Mock()
    with_next = {'next': 'some_link', 'results': []}
    without_next = {'next': None, 'results': []}
    get.return_value.json.side_effect = [with_next, without_next]
    return mock.patch('flaskr.services.requests.get', get)


def patch_get_with_real_response(*args, **kwargs):
    get = mock.Mock()
    with open('fixtures/page.json') as f:
        get.return_value.json.return_value = json.loads(f.read())
    return mock.patch('flaskr.services.requests.get', get)


class HyperdriveTestCase(TestCase):

    def setUp(self):
        self.client = setup_client()

    def _load_json(self, response):
        return json.loads(response.data.decode('utf8'))

    def test_spaceships_returns_json(self):
        # Only checks if the answer is loadable
        self._load_json(self.client.get('/'))

    def test_load_spaceships_calls_requests(self):
        with patch_get_with_multiple_pages() as get:
            services.get_spaceship_data()
            get.assert_called_with(
                'https://swapi.co/api/starships/',
                params=mock.ANY
            )

    def test_load_spaceships_iterates_over_pages(self):
        with patch_get_with_multiple_pages() as get:
            services.get_spaceship_data()
            self.assertEqual(get.call_count, 2)

    def test_load_spaceships_gets_data(self):
        with patch_get_with_real_response():
            r = services.get_spaceship_data()
            self.assertListEqual(
                r,
                [{'name': 'Naboo star skiff', 'hyperdrive': '0.5'}]
            )
