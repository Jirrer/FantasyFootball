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

def test_start_draft(app_client):
    # Open Draft
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})

    empty_room_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "test"})
    assert empty_room_response.status_code == 403

    # Join Draft
    app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})

    missing_group_response = app_client.post("/start-draft", json={"draftKey": "", "userToken": "test"})
    assert missing_group_response.status_code == 404

    # Does not work while username is hardcoded
    # missing_user_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": ""})
    # assert missing_user_response.status_code == 404

    # Does not work while username is hardcoded
    # not_admin_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "test"})
    # assert not_admin_response.status_code == 403

    unknown_group_response = app_client.post("/start-draft", json={"draftKey": "group-2", "userToken": "test"})
    assert unknown_group_response.status_code == 404

    # Does not work while username is hardcoded
    # user_not_in_group_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "alice"})
    # assert user_not_in_group_response.status_code == 404

    good_response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "John"})
    assert good_response.status_code == 200

    already_started_draft = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "test"})
    assert already_started_draft.status_code == 403
