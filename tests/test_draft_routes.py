def test_open_draft_and_join_draft(app_client):
    response = app_client.post(
        "/open-draft",
        json={"groupKey": "group-1", "userName": "John"},
    )
    assert response.status_code == 200

    response = app_client.post(
        "/join-draft",
        json={"draftKey": "group-1", "userName": "Alice"},
    )
    assert response.status_code == 200
    assert response.get_json()["key"] == "test"


def test_start_draft_requires_admin(app_client):
    app_client.post(
        "/open-draft",
        json={"groupKey": "group-1", "userName": "John"},
    )
    app_client.post(
        "/join-draft",
        json={"draftKey": "group-1", "userName": "Alice"},
    )

    response = app_client.post(
        "/start-draft",
        json={"draftKey": "group-1", "userToken": "test"},
    )
    assert response.status_code == 200
