const API_URL = "http://127.0.0.1:5001"

if (!sessionStorage.getItem('page')) {
  sessionStorage.setItem('page','join_create');
}

function showPage() {
    const pageId = sessionStorage.getItem('page');

    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });

    document.getElementById(pageId).style.display = 'block';
}

function showDraftPage() {
    const pageId = sessionStorage.getItem('draftPage');

    document.querySelectorAll('.draftPage').forEach(page => {
        page.style.display = 'none';
    });

    document.getElementById(pageId).style.display = 'block';
}

async function createDraft(userName) {
    try {
        const response = await fetch(`${API_URL}/create-draft`);

        if (!response.ok) {
            throw new Error(response.status);
        }

        const data = await response.json();
        
        joinDraft(data.key, userName);
    } catch (error) {
        console.error(`Error creating draft - ${error}`)
    }
}

async function joinDraft(draftKey, userName) {
    try {
        const response = await fetch(`${API_URL}/join-draft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userName: userName, draftKey: draftKey})
        });

        if (!response.ok) {
            if (response.status == 404) {
                document.getElementById('joinResults').innerHTML = "Could not find draft";
            }

            throw new Error(response.status);
        } else {
            document.getElementById('joinResults').innerHTML = "Joined draft";
        }

        const data = await response.json();
        sessionStorage.setItem('draftKey', draftKey);
        sessionStorage.setItem('userName', userName);
        sessionStorage.setItem('playerKey', data.key); // backend returns "key"

        sessionStorage.setItem('page', 'waitingRoom')

        showPage();

        sessionStorage.setItem('draftPage', 'draftBoard');

        showDraftPage();
    } catch (error) {       
        console.error(`Error joining draft - ${error}`);
        
    }
}

function goToMyPlayers() {
    sessionStorage.setItem('draftPage', 'userPlayers');
    showDraftPage();
}

function goToDraftBoard() {
    sessionStorage.setItem('draftPage', 'draftBoard');
    showDraftPage();

}

function goToPicks() {
    sessionStorage.setItem('draftPage', 'picksBoard');
    showDraftPage();

}

async function sendPick(playerTeam, playerPosition, playerName) {
    const draftKey = sessionStorage.getItem('draftKey');
    const userKey = sessionStorage.getItem('playerKey');

    try {
        const response = await fetch(`${API_URL}/add-pick`, {
            method: 'POST',
            headers: {"Content-Type": 'application/json'},
            body: JSON.stringify({
                draftKey: draftKey,
                userKey: userKey,
                playerName: playerName,
                playerTeam: playerTeam,
                playerPosition: playerPosition,
            })
        });

        const data = await response.json()

        console.log(data);



    } catch (error) {
        console.error(error);
    }
}




showPage();

const savedPage = sessionStorage.getItem('page');
if (savedPage) {
  showPage();
  if (sessionStorage.getItem('draftKey')) showDraftPage();
}