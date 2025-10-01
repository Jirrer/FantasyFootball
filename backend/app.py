from flask import Flask, request, jsonify
from Main import submitPick, startDraft
from Player import Player

app = Flask(__name__)

# To-Do: make code that can create the json well

numberOfPlayers = 2
users = []
currUserIndex = 0
TotalPicks = numberOfPlayers * 12
numPicks = 0

@app.route("/addUser", methods=["POST"])
def addUser():
    data = request.json
    username = data.get('username')

    users.append(username)

    if len(users) == numberOfPlayers: startDraft(users)

    return jsonify({"status": "success"})


@app.route("/userPick", methods=["POST"])
def userPick():
    global users
    global currUserIndex
    global TotalPicks
    global numPicks

    data = request.json

    username = data.get('username')

    if users[currUserIndex] == username:
        pick = Player(data.get('playerName'), data.get('position'), data.get('team'))
        if (submitPick(username, pick)): 
            if currUserIndex == (len(users) - 1): currUserIndex = 0
            else: currUserIndex += 1

            numPicks += 1

            if numPicks == TotalPicks: exit

            return jsonify({"status": "success", "received": data}), 200
        else: return jsonify({"status": "fail", "reason": "Invalid Pick"}), 200

    return jsonify({"status": "fail", "reason": "Not Players Turn"}), 200



if __name__ == "__main__": app.run(debug=True) 