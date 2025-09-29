import json
from Player import Player
from collections import Counter

def createPlayers():
    players = Counter()

    with open('data/Players.json', 'r') as file:
        playerDict = json.load(file)

        for player in playerDict:
            players[Player(player["name"], player["position"], player["team"])] += 2

    return players

DraftPicks = {'testusername': [], 'Test': [], 'test2': []} # need to create empty arrays when game gets started
availablePlayers = createPlayers()


def submitPick(username, pick):
    userPicks = DraftPicks[username]

    if not playerIsAvailable(pick): return False
    if userHasPlayer(userPicks, pick): return False
    if not openPosition(userPicks, pick.position): return False

    DraftPicks[username].append(pick)
    
    global availablePlayers
    availablePlayers[pick] -= 1

    return True

def playerIsAvailable(player):
    global availablePlayers

    if availablePlayers[player] > 0: return True
    else: return False

def userHasPlayer(userPlayers, pick):
    for player in userPlayers:
        if player == pick: return True

    return False
    

def openPosition(userPlayers, pickPosition):
    if pickPosition == 'QB': count = 2
    elif pickPosition == 'WR': count = 3
    elif pickPosition == 'RB': count = 3
    elif pickPosition == 'TE': count = 2
    elif pickPosition == 'K': count = 1
    elif pickPosition == 'DFS': count = 1
    else: return "Error"

    currCount = 0
    for player in userPlayers:
        if player['position'] == pickPosition: currCount += 1

    if currCount >= count: return False
    else: return True

    

    
print(submitPick('testusername', Player("Josh Allen", "QB", "Bills")))
print(submitPick('Test', Player("Josh Allen", "QB", "Bills")))
print(submitPick('test2', Player("Josh Allen", "QB", "Bills")))

print(DraftPicks)