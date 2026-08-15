def test_frontend_index_page_is_served(client):
    response = client.get("/frontend/index.html")
    assert response.status_code == 200
    assert "Task Tracker Kanban" in response.text


def test_frontend_board_supports_loading_empty_and_error_states(client):
    response = client.get("/frontend/index.html")
    assert response.status_code == 200
    assert "boardState = \"loading\"" in response.text
    assert "boardState = \"empty\"" in response.text
    assert "boardState = \"error\"" in response.text
    assert "Retry" in response.text


def test_frontend_edit_modal_omits_unchanged_status(client):
    # The backend rejects same-status transitions with 422, so the edit modal
    # must not send `status` when the user did not change it.
    response = client.get("/frontend/index.html")
    assert response.status_code == 200
    assert "originalTaskStatus" in response.text
    assert "status !== originalTaskStatus" in response.text
