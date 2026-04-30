import sqlite3, os
from dotenv import load_dotenv
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import Pick

load_dotenv()

def checkForPlayer(pick: "Pick"):
    if pick is None:
        return False

    database_location = os.getenv('DATABASE_LOCATION')
    if not database_location:
        return False

    with sqlite3.connect(database_location) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT name, position, team FROM Players WHERE name = ? AND position = ? AND team = ?",
            (pick.name, pick.position.name.upper(), pick.team.name.upper()),
        )
        return cursor.fetchone() is not None
