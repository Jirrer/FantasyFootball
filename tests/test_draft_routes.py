def test_open_draft(app_client):
    good_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})
    assert good_response.status_code == 200

    blocked_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "Alice"})
    assert blocked_response.status_code == 403

    unknown_group_response = app_client.post("/open-draft", json={"groupKey": "group-2", "userName": "Alice"})
    assert unknown_group_response.status_code == 404

    unknown_player_response = app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "invalid"})
    assert unknown_player_response.status_code == 404

def test_join_draft(app_client):
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})

    good_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})
    assert good_response.status_code == 200

    unknown_group_response = app_client.post("/join-draft", json={"draftKey": "group-2", "userName": "Alice"})
    assert unknown_group_response.status_code == 404

    unknown_user_response = app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "invalid"})
    assert unknown_user_response.status_code == 404

def test_start_draft(app_client):
    app_client.post("/open-draft", json={"groupKey": "group-1", "userName": "John"})
    app_client.post("/join-draft", json={"draftKey": "group-1", "userName": "Alice"})
    response = app_client.post("/start-draft", json={"draftKey": "group-1", "userToken": "test"})
    assert response.status_code == 200
