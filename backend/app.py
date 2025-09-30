from flask import Flask, request, jsonify
from Main import submitPick
import Player

app = Flask(__name__)

users = []
currUser = 'testusername'

@app.route("/userPick", methods=["POST"])
def userPick():
    global users

    data = request.json

    username = data.get('username')

    if currUser == username:
        pick = Player(data.get('playerName'), data.get('position'), data.get('team'))
        if (submitPick(username, pick)): return jsonify({"status": "success", "received": data}), 200
        else: return jsonify({"status": "fail", "received": data}), 200



if __name__ == "__main__": app.run(debug=True) 