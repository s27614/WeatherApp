import unittest
from app import app


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_page(self):
        rv = self.app.get('/index')
        self.assertIn(b'Get Weather Conditions', rv.data)

    def test_valid_city_weather(self):
        rv = self.app.get('/weather?city=Warsaw')
        self.assertIn(b'Warsaw Weather', rv.data)

    def test_empty_city_weather(self):
        rv = self.app.get('/weather?city=')
        self.assertIn(b'Warsaw Weather', rv.data)  # Assuming it should return Warsaw weather when city is empty

    def test_invalid_city_weather(self):
        rv = self.app.get('/weather?city=InvalidCity')
        self.assertEqual(rv.status_code, 200)  # Assuming it returns 200 OK even for invalid city
        self.assertIn(b'City Not Found', rv.data)

if __name__ == '__main__':
    unittest.main()

