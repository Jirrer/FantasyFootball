from collections import Counter
import json
from Player import Player
from User import User
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

load_dotenv()

def createPlayers():
    players = Counter()
    with open('data/Players.json', 'r') as file:
        playerDict = json.load(file)
        for player in playerDict:
            p = Player(player["name"], player["position"], player["team"])
            players[p] += 2 
    return players

availablePlayers = createPlayers()
DraftPicks = {}

def startDraft(usersInput):
    for user in usersInput:
        DraftPicks[user.username] = []

def submitPick(username, pick): 
    userPicks = DraftPicks[username]

    if not playerIsAvailable(pick): return False
    if userHasPlayer(userPicks, pick): return False
    if not openPosition(userPicks, pick.position): return False

    DraftPicks[username].append(pick)
    
    global availablePlayers
    availablePlayers[pick] -= 1

    print(f"{username} drafts {pick}")

    return True

def playerIsAvailable(player):
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
        if player.position == pickPosition: currCount += 1

    if currCount >= count: return False
    else: return True

def endDraft(draftUsers):
    print("draft is done, sending emails")
    for user in draftUsers:
        sendEmail(user.email, user)
        sendEmail('jrirrer@gmail.com', user) # <--- sends a copy to my email

def sendEmail(email, user):
    scriptUserName = os.getenv("EMAIL_USERNAME")
    scriptPassword = os.getenv("EMAIL_PASSWORD")

    message = generateEmailMessage(user)

    msg = MIMEMultipart()
    msg["Subject"] = f"Screen Time Report"
    msg["To"] = email
    msg["From"] = scriptUserName

    msg.attach(MIMEText(message))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(scriptUserName, scriptPassword)
        server.send_message(msg)

def generateEmailMessage(user):
    playersByPosition = {'QB': [], 'WR': [], 'RB': [], 'TE': [], 'DFS': [], 'K': []}
    
    for player in DraftPicks[user.username]:
        playersByPosition[player.position].append(player) 

    message = f"""{user.username} made the following picks:
        Quarterbacks
            {playersByPosition['QB'][0].name} - {playersByPosition['QB'][0].team}
            {playersByPosition['QB'][1].name} - {playersByPosition['QB'][1].team}

        Wide Recievers
            {playersByPosition['WR'][0].name} - {playersByPosition['WR'][0].team} 
            {playersByPosition['WR'][1].name} - {playersByPosition['WR'][1].team} 
            {playersByPosition['WR'][2].name} - {playersByPosition['WR'][2].team} 

        Running Backs
            {playersByPosition['RB'][0].name} - {playersByPosition['RB'][0].team}
            {playersByPosition['RB'][1].name} - {playersByPosition['RB'][1].team}
            {playersByPosition['RB'][2].name} - {playersByPosition['RB'][2].team}

        Tight End
            {playersByPosition['TE'][0].name} - {playersByPosition['TE'][0].team}
            {playersByPosition['TE'][1].name} - {playersByPosition['TE'][1].team}

        Defense & Special Teams
            {playersByPosition['DFS'][0].name} - {playersByPosition['DFS'][0].team}

        Kicker
            {playersByPosition['K'][0].name} - {playersByPosition['K'][0].team}
    """

    return message