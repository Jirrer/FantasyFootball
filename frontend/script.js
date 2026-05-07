const API_URL = "http://127.0.0.1:5001"

showPage('join_create');

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.style.display = 'none';
    });

    document.getElementById(pageId).style.display = 'block';
}

function showDraftPage(pageId) {
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
            showDraftPage('draftBoard');
        }

        const data = await response.json();

        showPage('draftPage');
    } catch (error) {       
        console.error(`Error joining draft - ${error}`);
        
    }
}