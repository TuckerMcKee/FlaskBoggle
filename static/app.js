const $guess = $('#guess');
const $guess_Btn = $('#guess-btn');
const $results = $('#results');
const $score = $('#score');
const $time = $('#time');
const $high_Score = $('#high-score');
const $game_Num = $('#game-num');

const wordsFound = [];

$(document).ready(timeHandler);

$guess_Btn.on('click', guessSubmitHandler);

function timeHandler() {
    let count = 60; 
    let stopTime = setInterval(async function() {
        count = count - 1;
        $time.text(count);
        if (count === 0) {
            clearInterval(stopTime);
            $guess_Btn.attr("disabled", "disabled");
            let response = await scoreUpdate($score.text())
            $high_Score.text(response.high_score)
            $game_Num.text(response.num_games)
        }
    }, 1000)
}

async function scoreUpdate(score) {
    const response = await axios({
        url: '/score',
        method: "POST",
        params: {score: score}
      });  
    return response.data;
}

async function guessSubmitHandler(e) {
    e.preventDefault();
    let guess = $guess.val();
    if (wordsFound.indexOf(guess) !== -1){
        $results.text('You already found that word');
        return;
    }
    let currScore = parseInt($score.text());
    let response = await sendGuess(guess);
    $results.text(response.result);
    if (response.result === 'ok'){
        $score.text(currScore + guess.length);
        wordsFound.push(guess);
    }
} 

async function sendGuess(guess) {
    const response = await axios({
        url: '/guess',
        method: "POST",
        params:{guess: guess}
      });
    return response.data;
}