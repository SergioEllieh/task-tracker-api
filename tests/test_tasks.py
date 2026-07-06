def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "My Task",
            "description": "A description",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alice",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert data["description"] == "A description"
    assert data["status"] == "ToDo"
    assert data["priority"] == "High"
    assert data["assignee"] == "alice"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"description": "no title"})
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "priority": "Urgent"})
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "unknown_field": "nope"})
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "ToDo task"})
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Another high", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(task["priority"] == "High" for task in data)


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "updated title"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated title"
    assert data["description"] == created_task["description"]
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]
    assert data["assignee"] == created_task["assignee"]
    assert data["id"] == created_task["id"]


def test_patch_not_found_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{task_id}", json={"title": "nope"})
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"
