from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    @classmethod
    def setUpClass(self):
        """Set up test variables."""
        self.boggle_game = Boggle()
        self.client = app.test_client()
        self.client.testing = True
        with self.client.session_transaction() as sess:
            sess['board'] = [['Z', 'U', 'J', 'Z', 'R'], 
                             ['I', 'P', 'W', 'O', 'D'], 
                             ['Z', 'W', 'R', 'H', 'G'], 
                             ['B', 'T', 'D', 'O', 'T'], 
                             ['C', 'Q', 'A', 'L', 'O']]
            sess['high_score'] = 0
            sess['num_games'] = 0
        self.board = sess['board']
        self.high_score = sess['high_score']
        self.num_games = sess['num_games']

    def test_game_start(self):
        """testing html for home route"""
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div id="score">0</div>',html) 

    def test_guess(self):
        """testing responses for guess route"""
        with self.client as client:
            res = client.post('/guess', json={'guess': 'xiaosfj'})
            json_obj = res.get_json()
            res2 = client.post('/guess', json={'guess': 'dot'})
            json_obj2 = res2.get_json()
            res3 = client.post('/guess', json={'guess': 'way'})
            json_obj3 = res3.get_json()
            self.assertEqual(res.status_code, 200) 
            self.assertEqual('not-word',json_obj['result'])
            self.assertEqual(res2.status_code, 200) 
            self.assertEqual('ok',json_obj2['result'])
            self.assertEqual(res3.status_code, 200) 
            self.assertEqual('not-on-board',json_obj3['result'])

    def test_score(self):
        """testing num_games and high_score variables updates for score route"""
        with self.client as client:
            res = client.post('/score',json={'score': 5})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(int(session['num_games']), 1)
            self.assertEqual(int(session['high_score']), 5)
            res2 = client.post('/score',json={'score': 6})
            self.assertEqual(res2.status_code, 200)
            self.assertEqual(int(session['num_games']), 2)
            self.assertEqual(int(session['high_score']), 6)

             

