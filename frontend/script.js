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

async function openDraft(groupKey, username) {
    try {
        const response = await fetch(`${API_URL}/open-draft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({userName: username, groupKey: groupKey})
        });

        if (!response.ok) {
            throw new Error(response.status);
        } else {
            console.log("draft open");
        }

        
        
    } catch (error) {
        console.error(`Error opening draft - ${error}`)
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
        
        const data = await response.json();

        if (!response.ok) {
            document.getElementById('joinResults').innerHTML = data.message;

        } else {
            sessionStorage.setItem('draftKey', draftKey);
            sessionStorage.setItem('userName', userName);
            sessionStorage.setItem('playerKey', data.key); 

            sessionStorage.setItem('page', 'waitingRoom')
            
            showPage();  
                      
        }

        // create a way to go from waiting room to draft page
        
        
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

    console.log(playerTeam)

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

async function startDraft() {
    const groupKey = sessionStorage.getItem('draftKey');
    const userToken = sessionStorage.getItem('userKey');

    try {
        const response = await fetch (`${API_URL}/start-draft`, {
            method: 'POST',
            headers: {"Content-Type": 'application/json'},
            body: JSON.stringify({
                draftKey: groupKey,
                userToken: userToken,
            })
        });


        if (response.ok) {
            sessionStorage.setItem('page', 'draftPage')
            showPage();

            sessionStorage.setItem('draftPage', 'draftBoard');
            showDraftPage();


        } else {
            console.error(response);
        }



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