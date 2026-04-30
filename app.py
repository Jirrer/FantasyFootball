import os, random, string, enum
import database
from flask import Flask, jsonify, request

app = Flask(__name__)

class Team(enum.Enum):
    ARI = "Arizona Cardinals"
    ATL = "Atlanta Falcons"
    BAL = "Baltimore Ravens"
    BUF = "Buffalo Bills"
    CAR = "Carolina Panthers"
    CHI = "Chicago Bears"
    CIN = "Cincinnati Bengals"
    CLE = "Cleveland Browns"
    DAL = "Dallas Cowboys"
    DEN = "Denver Broncos"
    DET = "Detroit Lions"
    GB = "Green Bay Packers"
    HOU = "Houston Texans"
    IND = "Indianapolis Colts"
    JAX = "Jacksonville Jaguars"
    KC = "Kansas City Chiefs"
    LAC = "Los Angeles Chargers"
    LAR = "Los Angeles Rams"
    LV = "Las Vegas Raiders"
    MIA = "Miami Dolphins"
    MIN = "Minnesota Vikings"
    NE = "New England Patriots"
    NO = "New Orleans Saints"
    NYG = "New York Giants"
    NYJ = "New York Jets"
    PHI = "Philadelphia Eagles"
    PIT = "Pittsburgh Steelers"
    SEA = "Seattle Seahawks"
    SF = "San Francisco 49ers"
    TB = "Tampa Bay Buccaneers"
    TEN = "Tennessee Titans"
    WSH = "Washington Commanders"

class Position(enum.Enum):
    QB = 3
    WR = 5
    RB = 5
    TE = 2
    K = 2
    DFS = 2
    FLEX = 1 

class Pick:
    def __init__(self, name:str, position:Position, team:Team):
        self.name = name
        self.position = position
        self.team = team

    def __repr__(self):
        return (f"{self.name} | {self.position.name} | {self.team.name}")
        
class Player:
    def __init__(self, key: str, name: str):
        self.key = key
        self.team: list[Pick] = []
        self.name = name

    def __hash__(self):
        return hash(self.key)
    
    def __repr__(self):
        return f"{self.name} - {self.key}"

class Draft:
    def __init__(self, key: str):
        self.key = key
        self.players: list[Player] = []
        self.round:int = 0
        self.playerOnTheClock:int = 0
    
    def __hash__(self):
        return hash(self.key)
    
    def addPlayer(self, newPlayer: Player) -> bool:
        if len(self.players) <= 12 and self.round == 0:
            self.players.append(newPlayer)
            return True
        
        else:
            return False
        
    def nextPick(self) -> bool:
        self.playerOnTheClock += 1

        if self.playerOnTheClock == len(self.players):
            self.playerOnTheClock = 0
            self.players.reverse()
            self.round += 1

        if self.round > 12:
            return False
        
        return True

    def makePick(self, newPlayer:Player, pick:Pick) -> bool:
        for player in self.players:
            if player.key == newPlayer.key:
                if self.playerOnTheClock != self.players.index(player): return False
                if len([p.position for p in player.team if p.position == pick.position]) >= pick.position.value: return False

                player.team.append(pick)

                return (self.nextPick())

        return False

drafts: list[Draft] = []

@app.route('/create-draft')
def createDraft():
    characters = string.ascii_letters + string.digits

    while (True):
        # newDraftKey = ''.join(random.choices(characters, k=16))
        newDraftKey = "devDraftKey"
        
        if newDraftKey in set(drafts): continue 

        drafts.append(Draft(newDraftKey))
        
        break

    return jsonify({"message": "Draft started", "key": newDraftKey}), 200

@app.route('/add-player', methods=["post"])
def addPlayer():
    data = request.json

    draftKey = data.get('draftKey')
    userName = data.get('userName')

    if not draftKey or not userName:
        return jsonify({"status": "fail", "reason": "Null draft key or user name"}), 404
    
    foundDraft = False
    
    # To-Do: implement search algo
    for draft in drafts:
        if draft.key != draftKey: continue

        foundDraft = True

        characters = string.ascii_letters + string.digits

        while(True):
            # newPlayerKey = ''.join(random.choices(characters, k=16))
            newPlayerKey = "devPlayerKey"

            if newPlayerKey in set(draft.players): continue

            if not draft.addPlayer(Player(newPlayerKey, userName)): 
                return jsonify({"status": "fail", "reason": "Draft is full or has started"}), 404  

            break

    if foundDraft == False:
        return jsonify({"status": "fail", "reason": "Draft Key does not exist"}), 404 

    return jsonify({"message": "Player Added", "key": newPlayerKey}), 200

@app.route("/start-draft", methods=["post"])
def startDraft():
    data = request.json

    draftKey = data.get('draftKey')

    if not draftKey:
        return jsonify({"status": "fail", "reason": "Null draft key"}), 404
    
    for draft in drafts:
        if draft.key != draftKey: continue

        if not len(draft.players):
            return jsonify({"status": "fail - empty draft"}), 403

        if draft.round == 0:
            draft.round = 1

            return jsonify({"status": "Success - draft started"}), 200 
        
    return jsonify({"status": "fail"}), 403 

@app.route("/add-pick", methods=["post"])
def addPick():
    data = request.json

    draftKey = data.get('draftKey')
    userKey = data.get('userKey')
    playerName = data.get('playerName')
    playerTeam = data.get('playerTeam')
    playerPosition = data.get('playerPosition')

    if not userKey or not playerName or not playerTeam or not playerPosition or not draftKey:
        return jsonify({"status": "fail - bad input"}), 403

    for draft in drafts:
        if draft.key == draftKey:
            if draft.round == 0:
                return jsonify({"status": "fail - draft has not begun"}), 404

            for player in draft.players:
                if player.key == userKey:
                    pos = Position.__members__.get(playerPosition.upper())
                    if not pos: return jsonify({"status": "fail - bad player position input"}), 403 

                    team = Team.__members__.get(playerTeam.upper())
                    if not team: return jsonify({"status": "fail - bad team input"}), 403 

                    pick = Pick(playerName, Position(pos), Team(team))

                    if not database.checkForPlayer(pick): return jsonify({"status": "fail - pick not in database"}), 404

                    if draft.makePick(player, pick): return jsonify({"status": "Success - player added"}), 200 

                    else:
                        return jsonify({"status": "fail - could not make pick"}), 404 

    return jsonify({"status": "fail - could not find draft"}), 404

def showDraftState():
    print("\n\n")

    for draft in drafts:
        print(f"draft - {draft.key} - Round({draft.round})")
        
        for p in draft.players:
            if draft.players.index(p) == draft.playerOnTheClock and draft.round != 0:
                print(f"\tUser - {p} (On the clock)")

            else:
                print(f"\tUser - {p}")


            for x in p.team:
                print(f"\t\tPlayer - {x}")

    print("\n\n")

@app.after_request
def log_state(response):
    showDraftState()
    return response

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5001"))
    app.run(debug=True, host=host, port=port)