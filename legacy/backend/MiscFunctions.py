from collections import Counter
from Player import Player
import json

def createPlayers(countPerPlayer: int):
    players = Counter()

    with open('data/Players.json', 'r') as file:
        playerDict = json.load(file)

        for player in playerDict:
            p = Player(player["name"], player["position"], player["team"])
            players[p] += countPerPlayer 

    return players