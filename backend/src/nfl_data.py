import os, sqlite3
from dotenv import load_dotenv
import nflreadpy as nfl

load_dotenv()

def updatePlayersTable(year: int):
    rosters = nfl.load_rosters(year)
    
    player_data = rosters.select(["full_name", "position", "team"]).sort("team")
    
    # Connect to database
    conn = sqlite3.connect(os.getenv('DATABASE_LOCATION'))
    cursor = conn.cursor()
    
    output = []
    for row in player_data.iter_rows(named=True):
        output.append((row['full_name'], row['position'], row['team']))
    
    # Insert all players at once
    cursor.executemany("INSERT INTO players (name, position, team) VALUES (?, ?, ?)", output)
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(output)} players into database")

if __name__ == "__main__":
    updatePlayersTable(2025)