def test_check_if_user_in_group(test_database_path):
    from backend.database import checkIfUserInGroup

    assert checkIfUserInGroup("group-1", "John") is True
    assert checkIfUserInGroup("group-1", "Alice") is True
    assert checkIfUserInGroup("group-1", "Missing") is False
import pytest

def test_check_if_group_exists(test_database_path):
    from backend.database import checkIfGroupExists

    assert checkIfGroupExists("group-1") is True
    assert checkIfGroupExists("missing-group") is False

def test_check_if_admin(test_database_path):
    from backend.database import checkIfAdmin

    assert checkIfAdmin("group-1", "John") is True
    assert checkIfAdmin("group-1", "Alice") is False

    with pytest.raises(KeyError):
        checkIfAdmin("group-1", "joey")

    with pytest.raises(KeyError):
        checkIfAdmin("group-1", "hank")
 
def test_check_for_player(test_database_path):
    from backend.draft import Pick, Position, Team
    from backend.database import checkForPlayer

    assert checkForPlayer(Pick("Sample Player", Position.QB, Team.ARI)) is True
    assert checkForPlayer(Pick("Missing Player", Position.QB, Team.ARI)) is False
