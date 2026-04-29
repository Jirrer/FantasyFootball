import os, random, string

from flask import Flask, jsonify, request

app = Flask(__name__)

class Player:
    def __init__(self, key: str):
        self.key = key

    def __hash__(self):
        return hash(self.key)

class Draft:
    def __init__(self, key: str):
        self.key = key
        self.players: list[Player] = []
    
    def __hash__(self):
        return hash(self.key)
    
    def addPlayer(self, newPlayer: Player) -> bool:
        if len(self.players) <= 12:
            self.players.append(newPlayer)
            return True
        
        else:
            return False

drafts: list[Draft] = []


@app.route('/start-draft')
def startDraft():
    characters = string.ascii_letters + string.digits

    while (True):
        newDraftKey = ''.join(random.choices(characters, k=16))
        
        if newDraftKey in set(drafts): continue 

        drafts.append(Draft(newDraftKey))
        
        break

    return jsonify({"message": "Draft started", "key": newDraftKey}), 200

@app.route('/add-player', methods=["post"])
def addPlayer():
    data = request.json

    draftKey = data.get('draftKey')

    if not draftKey:
        return jsonify({"status": "fail", "reason": "Null draft key"}), 404
    
    foundDraft = False
    
    # To-Do: implement search algo
    for draft in drafts:
        if draft.key != draftKey: continue

        foundDraft = True

        characters = string.ascii_letters + string.digits

        while(True):
            newPlayerKey = ''.join(random.choices(characters, k=16))

            if newPlayerKey in set(draft.players): continue

            if not draft.addPlayer(Player(newPlayerKey)): 
                return jsonify({"status": "fail", "reason": "Draft is full"}), 404  

            break

    if foundDraft == False:
        return jsonify({"status": "fail", "reason": "Draft Key does not exist"}), 404 

    showDraftState()

    return jsonify({"message": "Player Added", "key": newPlayerKey}), 200


def showDraftState():
    for draft in drafts:
        print(draft.key)
        
        for p in draft.players:
            print(f"\t{p}")

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5001"))
    app.run(debug=True, host=host, port=port)