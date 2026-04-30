import csv
import sqlite3

allowed_positions = ["WR", "RB", "QB", "TE", "K"]
selected_teams = ["Lions", "Bills", "Jets", "Dolphins"]

database_connection = sqlite3.connect("..\\FantasyFootball_Backend\\FantasyFootball.db")

def main():
    clearDB()
    
    global selected_teams
    for team in selected_teams:
        importTeam(team)

def clearDB():
    global database_connection
    cursor = database_connection.cursor()

    cursor.execute("DELETE FROM players")

    database_connection.commit()
        
def importTeam(team):
    with open(f'teams\\{team}.csv') as file:
        reader = csv.reader(file)
        
        global allowed_positions
        selectedPlayers = []
        for row in reader:
            if row[3] in allowed_positions: selectedPlayers.append(row)

    updateDb(selectedPlayers, team)

def updateDb(playersList, teamName):
    global database_connection
    cursor = database_connection.cursor()
    
    cursor.execute(f"""
        INSERT OR IGNORE INTO players (name, position, team)
        values ("{teamName}","DFS","{teamName}")
        """)

    for player in playersList:
        playerName = player[1]
        playerPosition = player[3]

        cursor.execute(f"""
        INSERT OR IGNORE INTO players (name, position, team)
        values ("{playerName}","{playerPosition}","{teamName}")
        """)
        
        print(f"added - {playerName, playerPosition, teamName}")

    database_connection.commit()
    database_connection.close()

if __name__ == "__main__": main()