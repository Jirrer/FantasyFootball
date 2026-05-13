def test_open_draft(app_client):
    missing_group_response = app_client.post("/open-draft", json={"groupKey": "", "userName": "Alice"})
    assert missing_group_response.status_code == 404

    missing_user_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": ""})
    assert missing_user_response.status_code == 404

    unknown_group_response = app_client.post("/open-draft", json={"groupKey": "group-2", "userName": "Alice"})
    assert unknown_group_response.status_code == 404

    unknown_player_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "invalid"})
    assert unknown_player_response.status_code == 404

    blocked_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "Alice"})
    assert blocked_response.status_code == 403

    good_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})
    assert good_response.status_code == 200

    duplicate_open_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})
    assert duplicate_open_response.status_code == 403

def test_join_draft(app_client):
    unstarted_draft_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "John"})
    assert unstarted_draft_response.status_code == 404

    # open Draft
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})

    missing_group_response = app_client.post("/join-draft", json={"draftKey": "", "userName": "Alice"})
    assert missing_group_response.status_code == 404

    missing_user_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": ""})
    assert missing_user_response.status_code == 404

    unknown_group_response = app_client.post("/join-draft", json={"draftKey": "group-2", "userName": "Alice"})
    assert unknown_group_response.status_code == 404

    unknown_user_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "invalid"})
    assert unknown_user_response.status_code == 404

    good_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})
    assert good_response.status_code == 200

    duplicate_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})
    assert duplicate_response.status_code == 200

def test_start_draft(app_client):
    # Open Draft
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})

    john_join_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "John"})
    john_token = john_join_response.get_json()["key"]

    empty_room_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "test"})
    assert empty_room_response.status_code == 404

    # Join Draft
    alice_join_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})
    alice_token = alice_join_response.get_json()["key"]

    missing_group_response = app_client.post("/start-draft", json={"draftKey": "", "userToken": "test"})
    assert missing_group_response.status_code == 404

    # Does not work while username is hardcoded
    missing_user_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": ""})
    assert missing_user_response.status_code == 404

    # Does not work while username is hardcoded
    not_admin_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": alice_token})
    assert not_admin_response.status_code == 403

    unknown_group_response = app_client.post("/start-draft", json={"draftKey": "group-2", "userToken": "test"})
    assert unknown_group_response.status_code == 404

    # Does not work while username is hardcoded
    user_not_in_group_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "alice"})
    assert user_not_in_group_response.status_code == 404

    good_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": john_token})
    assert good_response.status_code == 200

    already_started_draft = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": john_token})
    assert already_started_draft.status_code == 403

def test_add_pick(app_client):
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})
    
    john_join_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "John"})
    john_token = john_join_response.get_json()["key"]

    unstarted_draft_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert unstarted_draft_response.status_code == 403

    app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": john_token})

    missing_userkey_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": "",
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert missing_userkey_response.status_code == 404 
    
    missing_playernName_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert missing_playernName_response.status_code == 404

    missing_playerTeam_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "",
        "playerPosition": "QB"
    })
    assert missing_playerTeam_response.status_code == 404

    missing_playerPosition_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": ""
    })
    assert missing_playerPosition_response.status_code == 404

    missing_groupKey_response = app_client.post("/add-pick", json={
        "draftKey": "",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert missing_groupKey_response.status_code == 404

    unknown_group_response = app_client.post("/add-pick", json={
        "draftKey": "group-2",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert unknown_group_response.status_code == 404

    unknown_user_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": "Alice",
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert unknown_user_response.status_code == 404

    bad_playerPosition_input_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "BUF",
        "playerPosition": "invalid"
    })
    assert bad_playerPosition_input_response.status_code == 403

    bad_playerTeam_input_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Josh Allen",
        "playerTeam": "invalid",
        "playerPosition": "QB"
    })
    assert bad_playerTeam_input_response.status_code == 403

    input_not_in_database_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Real Looking Player",
        "playerTeam": "BUF",
        "playerPosition": "QB"
    })
    assert input_not_in_database_response.status_code == 404

    good_response = app_client.post("/add-pick", json={
        "draftKey": "group-1",
        "token": john_token,
        "playerName": "Sample Player",
        "playerTeam": "ARI",
        "playerPosition": "QB"
    })

    assert good_response.status_code == 200

def test_pull_user_players(app_client):
    pass