from flask import Flask, request, jsonify
from Main import submitPick, startDraft, endDraft
from Player import Player
from User import User

app = Flask(__name__)

# To-Do: make code that can create the json well

numberOfPlayers = 1
users = []
currUserIndex = 0
TotalPicks = numberOfPlayers * 12
numPicks = 0
draftStatus = False

@app.route('/getDraftStatus')
def getDraftStatus():
    if draftStatus: return jsonify({"status": 'Running'}), 200
    else: return jsonify({"status": "not-running"}), 200



@app.route("/addUser", methods=["POST"])
def addUser():
    data = request.json

    username = data.get('username')
    email = data.get('email')

    print(username)
    print(email)


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
    global numPicks
    global draftStatus

    data = request.json

    username = data.get('username')

    if users[currUserIndex].username == username:
        pick = Player(data.get('playerName'), data.get('position'), data.get('team'))
        if (submitPick(username, pick)): 
            if currUserIndex == (len(users) - 1): currUserIndex = 0
            else: currUserIndex += 1

            numPicks += 1

            if numPicks == TotalPicks: 
                draftStatus = False
                endDraft(users)

            return jsonify({"status": "success", "received": data}), 200
        else: return jsonify({"status": "fail", "reason": "Invalid Pick"}), 200

    return jsonify({"status": "fail", "reason": "Not Players Turn"}), 200



if __name__ == "__main__": app.run(debug=True) 