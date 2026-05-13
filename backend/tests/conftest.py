import os
import sqlite3
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"


def _build_test_database(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        with SCHEMA_PATH.open("r", encoding="utf-8") as schema_file:
            schema_sql = schema_file.read().replace("CREATE TABLE sqlite_sequence(name,seq);\n", "")
            connection.executescript(schema_sql)

        connection.executemany(
            "INSERT INTO groups (key, password, drafted) VALUES (?, ?, ?)",
            [("group-1", "secret", 0)],
        )
        connection.executemany(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            [
                ("John", "password", "john@example.com"),
                ("Alice", "password", "alice@example.com"),
                ("joey", "password", "joey@example.com"),
                ("hank", "password", "hank@example.com"),
            ],
        )
        connection.executemany(
            "INSERT INTO user_group_membership (groupID, userID, role) VALUES (?, ?, ?)",
            [(1, 1, "admin"), (1, 2, "user"), (1, 3, ""), (1, 4, "badRole")],
        )
        connection.executemany(
            "INSERT INTO Players (name, position, team) VALUES (?, ?, ?)",
            [("Sample Player", "QB", "ARI")],
        )
        connection.executemany(
            "INSERT INTO Picks (userGroupID, season, pickID) VALUES (?, ?, ?)",
            [(1, 2026, 1)],
        )
        connection.commit()


@pytest.fixture()
def test_database_path(tmp_path, monkeypatch):
    database_path = tmp_path / "test_fantasy_football.db"
    _build_test_database(database_path)
    monkeypatch.setenv("DATABASE_LOCATION", str(database_path))
    return database_path


@pytest.fixture()
def app_client(test_database_path):
    import src.draft as draft_module
    from app import app as flask_app

    draft_module.drafts.clear()
    flask_app.config.update(TESTING=True)

    with flask_app.test_client() as client:
        yield client

    draft_module.drafts.clear()
