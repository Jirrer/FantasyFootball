from Player import Player
from MiscFunctions import createPlayers
import smtplib, json, os
from collections import Counter
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

numberOfTeamsPerPlayer = 2
DraftPicks = {}
availablePlayers = createPlayers(numberOfTeamsPerPlayer)

def startDraft(usersInput):
    for user in usersInput: 
        DraftPicks[user.username] = []

def endDraft(draftUsers):
    for user in draftUsers:
        try: sendEmail(user.email, user)
        except smtplib.SMTPRecipientsRefused as e: print(e)

        sendEmail(os.getenv('DEFAULT_EMAIL'), user) # <--- sends a copy to my email

def submitPick(username, pick): 
    if not validPick(username, pick): return False

    DraftPicks[username].append(pick)
    
    global availablePlayers
    availablePlayers[pick] -= 1

    return True

def validPick(username, pick):
    userPicks = DraftPicks[username]

    if not playerIsAvailable(pick): return False
    if not userDoesNotHavePlayer(userPicks, pick): return False
    if not openPosition(userPicks, pick.position): return False

    return True

def playerIsAvailable(player):
    if availablePlayers[player] > 0: return True
    else: return False

def userDoesNotHavePlayer(userPlayers, pick):
    for player in userPlayers:
        if player == pick: return False

    return True

def openPosition(userPlayers, pickPosition):
    positionCounts = {'QB': 2, 'WR': 3, 'RB': 3, 'TE': 2, 'K': 1, 'DFS': 1}

    count = 0
    for player in userPlayers:
        if player.position == pickPosition: count += 1

    if count >= positionCounts[pickPosition]: return False
    else: return True

def getNonAvailablePlayers(username):
    nonAvailable = []
    
    for player in availablePlayers:
        if not validPick(username, player): nonAvailable.append(player)

    return json.dumps([p.__dict__ for p in nonAvailable])


def sendEmail(email, user):
    if len(email) <= 0: return

    scriptUserName = os.getenv("EMAIL_USERNAME")
    scriptPassword = os.getenv("EMAIL_PASSWORD")

    message = generateEmailMessage(user)

    msg = MIMEMultipart()
    msg["Subject"] = f"Fantasy Football Draft Report"
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