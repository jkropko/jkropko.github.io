const scoreBoard = {
  _round: 0,
  _home: 0,
  _away: 0,
  range: [0, 99],
  set home(val) {
    this._home = val;
    document.querySelector('#team1').textContent = this._home;
  },
  set away(val) {
    this._away = val;
    document.querySelector('#team2').textContent = this._away;
  },
  set round(val) {
    this._round = val;
    document.querySelector('#roundnum').textContent = this._round;
  },
  checkRangeAndUpdate(value, operator, step) {
    // destructure max and min
    const [min, max] = this.range;
    // set getter to underscore value for accessing object
    const getter = `_${value}`;
    if(operator === '+' && (this[getter] + step) - 1 < max) {
      // if operator is add and the incrementation wont exceede max increment by step
      this[value] = this[getter] + step;
    }
    if(operator === '-' && (this[getter] - step) + 1 > min) {
      // if operator is sub and the decrementation wont go below min deincrement by step
     this[value] = this[getter] - step;
    }
  },
  homeplus:   ['home', '+', 1],
  homeminus:  ['home', '-', 1],
  awayplus:   ['away', '+', 1],
  awayminus:  ['away', '-', 1],
  roundplus:  ['round', '+', 1],
  roundminus: ['round', '-', 1]
}

function init() {
  const container = document.querySelector('.scorecontainer');
  container.addEventListener('click', function(e) {
    // run function with params that match the buttons id
    scoreBoard.checkRangeAndUpdate.apply(scoreBoard, scoreBoard[e.target.id]);
  });
}

init();

// OLD CODE

// var round = 0, homeScore = 0, awayScore = 0;

// $('document').ready(function() {
//   $('#homeplus').click(function() { 
//     if (homeScore < 100) {
//       homeScore += 1;
//       $('#team1').text(homeScore);
//     }
//   });
//   $('#homeminus').click(function() {
//     if (homeScore > 0) {
//       homeScore -= 1;
//       $('#team1').text(homeScore);
//     }
//   });
//   $('#roundminus').click(function() {
//     if (round > 0) {
//       round -= 1;
//       $('#roundnum').text(round);
//     }
//   });
//   $('#roundplus').click(function() { 
//     if (round < 1000) {
//       round += 5;
//       $('#roundnum').text(round);
//     }
//   });
//   $('#awayplus').click(function() { 
//     if (awayScore < 100) {
//       awayScore += 1;
//       $('#team2').text(awayScore);
//     }
//   });
//   $('#awayminus').click(function() {
//     if (awayScore > 0) {
//       awayScore -= 1;
//       $('#team2').text(awayScore);
//     }
//   });
// });
