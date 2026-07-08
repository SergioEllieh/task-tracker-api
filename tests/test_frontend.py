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
