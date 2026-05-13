import os, random, string, enum, secrets
from . import database
from flask import Blueprint, jsonify, request

bp = Blueprint('draft', __name__)
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
        return self.name

    def __contains__(self, item):
        return item == self.name

class Draft:
    def __init__(self, key: str):
        self.key = key
        self.players: list[Player] = []
        self.round:int = 0
        self.playerOnTheClock:int = 0
        self.seenPlayers: dict[str:int] = {}
    
    def __hash__(self):
        return hash(self.key)
    
    def __repr__(self):
        return self.key
    
    def __eq__(self, value):
        return self.key == value
        
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

                if pick in self.seenPlayers and self.seenPlayers[pick] >= 2: return False

                if pick in player.team: return False #To-Do: fix

                if pick in self.seenPlayers: self.seenPlayers[pick] += 1

                else: self.seenPlayers[pick] = 1

                player.team.append(pick)

                return (self.nextPick())

        return False

drafts: dict[str, Draft] = {}

@bp.route('/open-draft', methods=["post"])
def openDraft():
    data = request.json

    groupKey = data.get('groupKey')
    userName = data.get('userName')

    if not groupKey:
        return jsonify({"status": "fail", "message": "NULL group"}), 404
    
    if not userName:
        return jsonify({"status": "fail", "message": "NULL username"}), 404
    
    if not database.checkIfGroupExists(groupKey):
        return jsonify({"status": "fail", "message": "Unknown group key"}), 404
    
    if not database.checkIfUserInGroup(groupKey, userName):
        return jsonify({"status": "fail", "message": "User not found in group"}), 404

    if not database.checkIfAdmin(groupKey, userName):
        return jsonify({"status": "fail", "message": "You must be an admin to open the draft"}), 403

    if drafts.get(groupKey):
        return jsonify({"status": "fail", "message": "draft is already open"}), 403
    
    drafts[groupKey] = Draft(groupKey)

    return jsonify({"status": "success"}), 200

@bp.route('/join-draft', methods=["post"])
def joinDraft():
    data = request.json

    groupKey = data.get('draftKey') #to-Do: change to group key
    userName = data.get('userName')

    if not groupKey:
        return jsonify({"status": "fail", "reason": "Null group key"}), 404
    
    if not userName:
        return jsonify({"status": "fail", "reason": "Null user name"}), 404
    
    if not database.checkIfGroupExists(groupKey):
        return jsonify({'status': "fail", 'message': "Group does not exist"}), 404
    
    if not database.checkIfUserInGroup(groupKey, userName):
        return jsonify({'status': "fail", 'message': "User not found in group"}), 404
    
    if not drafts.get(groupKey):
        return jsonify({'status': "fail", 'message': "could not find draft"}), 404
    
    if any(player.name == userName for player in drafts[groupKey].players):
        return jsonify({'status': "fail", 'message': "user already in this draft room"}), 200
    
    # To-Do: add a place here to let a user  rejoin and get new key
    
    token = generateUserToken(groupKey)

    if not drafts[groupKey].addPlayer(Player(token, userName)):
        return jsonify({'status': "fail", 'message': "Failed to add player for unknown reason"}), 500

    return jsonify({"message": "Player Joined",
                    "key": token,
                    "admin": database.checkIfAdmin(groupKey, getUsernameFromToken(groupKey, token)),
                    "started": drafts[groupKey].round > 0
                    }), 200

def generateUserToken(groupID: str) -> str:
    seenTokens = set([p.key for p in drafts[groupID].players])

    secret = secrets.token_urlsafe(32)

    while (seenTokens in seenTokens):
        secret = secrets.token_urlsafe(32)
    
    return secret
    
@bp.route("/start-draft", methods=["post"])
def startDraft():
    data = request.json

    groupKey = data.get('draftKey') #To-Do: change to groupKey
    userToken = data.get('userToken') 

    if not userToken:
        return jsonify({"status": "fail", "reason": "Null user token"}), 404

    if not groupKey:
        return jsonify({"status": "fail", "reason": "Null draft key"}), 404

    if not drafts.get(groupKey):
        return jsonify({"status": "fail", "reason": "Could not find group"}), 404

    username = getUsernameFromToken(groupKey, userToken)
    
    if not username:
        return jsonify({"status": "fail", "reason": "Null username"}), 404
    
    if not len(drafts[groupKey].players):
        return jsonify({"status": "fail", "reason": "Empty draft room"}), 403
    
    if not database.checkIfUserInGroup(groupKey, username): 
        return jsonify({"status": "fail", "reason": "User is not found in this draft"}), 404
    
    if not database.checkIfAdmin(groupKey, username): 
        return jsonify({"status": "Fail", 'message': 'you do not have the writes to start draft'}), 403

    if drafts[groupKey].round != 0:
        return jsonify({"status": "fail", "reason": "draft already started"}), 403
    
    drafts[groupKey].round = 1

    return jsonify({"status": "Success - draft started"}), 200

@bp.route("/add-pick", methods=["post"])
def addPick():
    data = request.json

    groupKey = data.get('draftKey') # to-do: change to group key
    userToken = data.get('token')
    playerName = data.get('playerName')
    playerTeam = data.get('playerTeam')
    playerPosition = data.get('playerPosition')

    if not userToken:
        return jsonify({"status": "fail", "message": "NULL user key"}), 404
    
    if not playerName:
        return jsonify({"status": "fail", "message": "NULL player name"}), 404
    
    if not playerTeam:
        return jsonify({"status": "fail", "message": "NULL player team"}), 404
    
    if not playerPosition:
        return jsonify({"status": "fail", "message": "NULL player position"}), 404
    
    if not groupKey:
        return jsonify({"status": "fail", "message": "NULL group key"}), 404

    if not drafts.get(groupKey):
        return jsonify({"status": "fail", "reason": "Unknown draft key"}), 404
    
    username = getUsernameFromToken(groupKey, userToken)

    if not username:
        return jsonify({"status": "fail", "message": "Unknown username"}), 404
    
    player = None
    for p in drafts[groupKey].players:
        if p.name == username:
            player = p
            break

    if not player:
        return jsonify({"status": "fail - could not find user"}), 404

    if drafts[groupKey].round == 0:
        return jsonify({"status": "fail - draft has not begun"}), 403

    pos = Position.__members__.get(playerPosition.upper())
    if not pos: return jsonify({"status": "fail - bad player position input"}), 403 

    team = Team.__members__.get(playerTeam.upper())
    if not team: return jsonify({"status": "fail - bad team input"}), 403 

    pick = Pick(playerName, Position(pos), Team(team))

    if not database.checkForPlayer(pick): return jsonify({"status": "fail - pick not in database"}), 404

    if drafts[groupKey].makePick(player, pick): return jsonify({"status": "Success - player added"}), 200 

    else:
        return jsonify({"status": "fail - could not make pick"}), 500 
    
def getUsernameFromToken(groupID:str, userToken: str):
    if not drafts.get(groupID):
        return None

    for player in drafts[groupID].players:
        print(player.key, userToken)
        if player.key == userToken:
            return player.name

    return None

def showDraftState():
    print("\n\n")

    for draftKey, draftInfo in drafts.items():
        print(f"draft - {draftKey} - Round({draftInfo.round})")
        
        for p in draftInfo.players:
            if draftInfo.players.index(p) == draftInfo.playerOnTheClock and draftInfo.round != 0:
                print(f"\tUser - {p} (On the clock)")

            else:
                print(f"\tUser - {p}")

            for x in p.team:
                print(f"\t\tPlayer - {x}")

    print("\n\n")

@bp.after_request
def log_state(response):
    showDraftState()
    return response
