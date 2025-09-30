from flask import Flask, request, jsonify
from Main import submitPick

app = Flask(__name__)

users = []
currUser = 'testusername'

@app.route("/userPick", methods=["POST"])
def userPick():
    global users

    data = request.json

    username = data.get('username')

    if currUser == username:   # assume user can only make valid picks
        pick = {'name': data.get('playerName'), 'position': data.get('position'), 'team': data.get('team')}
        submitPick(username, pick) 

    return jsonify({"status": "success", "received": data}), 200



if __name__ == "__main__": app.run(debug=True)