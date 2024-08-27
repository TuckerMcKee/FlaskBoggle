from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        boggle_game = Boggle()

    def test_game_start(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div id="score">0</div>',html) 

    def test_guess(self):
        boggle_game = Boggle()
        with app.test_client() as client:
            res = client.post('/guess', data={'guess': 'xiaosfj'})
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200) #this is getting 400 status code
            self.assertIn('not-word',html)         

