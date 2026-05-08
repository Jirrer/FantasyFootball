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
    
def checkIfGroupExists(groupKey: str) -> bool:
    database_location = os.getenv('DATABASE_LOCATION')

    if not database_location:
        return False
    
    with sqlite3.connect(database_location) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM groups WHERE key = ?",
            (groupKey,),
        )
        return cursor.fetchone() is not None

def checkIfAdmin(groupKey, username) -> bool:
    database_location = os.getenv('DATABASE_LOCATION')

    if not database_location:
        return False
    
    with sqlite3.connect(database_location) as connection:
        cursor = connection.cursor()

        membership = cursor.execute('''
            SELECT m.role
            FROM user_group_membership m
            JOIN groups g ON g.id = m.groupID
            JOIN users  u ON u.id = m.userID
            WHERE g.key    = ?
            AND   u.username = ?
        ''', (groupKey, username)).fetchone()

        if not membership:
            raise KeyError

        match membership[0]:
            case 'admin': return True
            case 'user': return False
            case _: raise KeyError()
