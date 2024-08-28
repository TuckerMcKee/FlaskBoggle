from boggle import Boggle
from flask import Flask, render_template, request, jsonify, session
boggle_game = Boggle()

app = Flask(__name__)
app.config["SECRET_KEY"] = 'secret_key'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def game_start():
    """initializes session variables, creates game board"""
    session['board'] = boggle_game.make_board()
    session['high_score'] = 0
    session['num_games'] = 0
    return render_template('board.html',board=session['board'])

@app.route('/guess', methods = ["POST"])
def guess_checker():
    """checks user guess, returns results"""
    guess = request.json.get('guess')
    result = boggle_game.check_valid_word(session['board'], guess)
    return jsonify({"result" : result})

@app.route('/score', methods = ["POST"])
def high_score():
    """when game is finished, updates high score and game number"""
    score = request.json.get('score')
    if int(score) > int(session['high_score']):
        session['high_score'] = score
    session['num_games'] += 1
    return jsonify({'num_games':session['num_games'],'high_score' : session['high_score']})
    



