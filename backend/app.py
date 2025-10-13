from flask import Flask, request, jsonify
from Main import DraftPicks, submitPick, startDraft, endDraft, getNonAvailablePlayers
from Player import Player
from User import User

app = Flask(__name__)

# To-Do: need to handle end of the draft

numberOfPlayers = 1
users = []
currUserIndex = 0
TotalPicks = numberOfPlayers * 12
draftStatus = False
draftBoard = []

@app.route('/getDraftStatus')
def getDraftStatus():
    if draftStatus: return jsonify({"status": 'Running'}), 200
    else: return jsonify({"status": "not-running"}), 200

@app.route("/addUser", methods=["POST"])
def addUser():
    data = request.json

    username = data.get('username')
    email = data.get('email')

    users.append(User(username, email))

    if len(users) == numberOfPlayers: 
        global draftStatus
        draftStatus = True
        startDraft(users)

    return jsonify({"status": "success"})


@app.route("/userPick", methods=["POST"])
def userPick():
    global users
    global currUserIndex
    global TotalPicks
    global draftStatus

    data = request.json

    username = data.get('username')

    if users[currUserIndex].username == username:
        pick = Player(data.get('playerName'), data.get('position'), data.get('team'))
        if (submitPick(username, pick)): 
            if currUserIndex == (len(users) - 1): currUserIndex = 0
            else: currUserIndex += 1

            draftBoard.append((username, (f"{pick.name} | {pick.position} | {pick.team}")))

            if len(draftBoard) == TotalPicks: 
                draftStatus = False
                endDraft(users)

            return jsonify({"status": "success", "received": data}), 200
        else: return jsonify({"status": "fail", "reason": "Invalid Pick"}), 200

    return jsonify({"status": "fail", "reason": "Not Players Turn"}), 200

@app.route('/pullDraftResults')
def sendDraftResults():
    return jsonify({'picks': draftBoard}), 200

@app.route('/pullUserTeam', methods=["POST"])
def sendUserTeam():
    data = request.json
    username = data.get('username')

    user_picks = DraftPicks.get(username, [])

    picks_serializable = [
        {"name": p.name, "position": p.position, "team": p.team} for p in user_picks
    ]

    return jsonify({'picks': picks_serializable}), 200

@app.route('/getAvailablePlayers', methods=["POST"])
def sendAvailablePlayers():
    data = request.json
    username = data.get("username")
    print("test")

    nonAvailablePlayers = getNonAvailablePlayers(username)
    
    return jsonify({"NonAvailablePlayers": nonAvailablePlayers}), 200



if __name__ == "__main__": app.run(debug=True) 