from Main import DraftPicks, submitPick, startDraft, endDraft, getNonAvailablePlayers
from flask import Flask, request, jsonify
from Player import Player
from User import User

app = Flask(__name__)

# To-Do: need to handle end of the draft
# To-Do: add a way to know whos turn it is

numberOfPlayers = 3
users = []
currUserIndex = 0
TotalPicks = numberOfPlayers * 12
draftIsRunning = False
draftBoard = []

@app.route('/getDraftStatus')
def getDraftStatus():
    if draftIsRunning: return jsonify({"status": 'Running'}), 200
    else: return jsonify({"status": "not-running"}), 200

@app.route("/addUser", methods=["POST"])
def addUser():
    data = request.json

    username, email = data.get('username'), data.get('email')

    users.append(User(username, email))

    if len(users) == numberOfPlayers: 
        global draftIsRunning
        draftIsRunning = True

        startDraft(users)

    return jsonify({"status": "success"}), 200


@app.route("/userPick", methods=["POST"])
def userPick():
    data = request.json

    username = data.get('username')

    if not users[currUserIndex].username == username: 
        return jsonify({"status": "fail", "reason": "Not Players Turn"}), 200
    
    pick = Player(data.get('playerName'), data.get('position'), data.get('team'))

    if not (submitPick(username, pick)): 
        return jsonify({"status": "fail", "reason": "Invalid Pick"}), 200
    
    draftBoard.append((username, (f"{pick.name} | {pick.position} | {pick.team}")))

    if len(draftBoard) == TotalPicks: 
        global draftIsRunning
        draftIsRunning = False

        endDraft(users)

    movePlayerIndex()
    return jsonify({"status": "success", "received": data}), 200

def movePlayerIndex():
    global currUserIndex

    if currUserIndex == (len(users) - 1): currUserIndex = 0
    else: currUserIndex += 1


@app.route('/pullDraftResults')
def sendDraftResults():
    return jsonify({'picks': draftBoard}), 200

@app.route('/pullUserTeam', methods=["POST"])
def sendUserTeam():
    data = request.json
    username = data.get('username')

    picks = DraftPicks.get(username, [])

    serializablePicks = [
        {"name": p.name, "position": p.position, "team": p.team} for p in picks
    ]

    return jsonify({'picks': serializablePicks}), 200

@app.route('/getAvailablePlayers', methods=["POST"])
def sendAvailablePlayers():
    data = request.json
    username = data.get("username")

    nonAvailablePlayers = getNonAvailablePlayers(username)
    
    return jsonify({"NonAvailablePlayers": nonAvailablePlayers}), 200

if __name__ == "__main__": app.run(debug=True) 