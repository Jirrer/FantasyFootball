let teamsArray = ["Player 1", "Player 2", "Player 3", "player 4", "player 5", "player 6"]

function updateTopBar() {
    let container = document.getElementById("topBar_teams");

    container.innerHTML = teamsArray
        .slice(0, teamsArray.length)
        .map(topBarTeam => `<div id="topBarTeam">${topBarTeam}</div>`)
        .join(""); 
}

updateTopBar();