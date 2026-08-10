from datetime import datetime, timedelta, timezone


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


def test_patch_existing_task_in_progress_to_todo_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "In progress task", "status": "InProgress"},
    )
    assert create_response.status_code == 201

    task_id = create_response.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert "Invalid status transition from InProgress to ToDo" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {task_id} not found"


def test_create_task_with_valid_due_date_returns_201_and_overdue_flag(client):
    today = datetime.now(timezone.utc).date()
    past = (today - timedelta(days=1)).isoformat()

    response = client.post(
        "/tasks",
        json={
            "title": "Task with due",
            "due_date": past,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] == past
    assert data["overdue"] is True


def test_create_task_without_due_date_returns_201_and_null_due_and_not_overdue(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task without due",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["due_date"] is None
    assert data["overdue"] is False


def test_create_task_with_invalid_due_date_returns_422_and_no_task_created(client):
    response = client.post(
        "/tasks",
        json={"title": "Bad due", "due_date": "not-a-date"},
    )
    assert response.status_code == 422

    # storage is reset per-test; ensure no task was created
    list_resp = client.get("/tasks")
    assert list_resp.status_code == 200
    assert list_resp.json() == []


def test_patch_add_change_and_clear_due_date(client):
    today = datetime.now(timezone.utc).date()
    tomorrow = (today + timedelta(days=1)).isoformat()
    yesterday = (today - timedelta(days=1)).isoformat()

    # create without due date
    create = client.post("/tasks", json={"title": "patch due test"})
    assert create.status_code == 201
    task = create.json()
    task_id = task["id"]

    # add due date
    add = client.patch(f"/tasks/{task_id}", json={"due_date": tomorrow})
    assert add.status_code == 200
    assert add.json()["due_date"] == tomorrow

    # change due date
    change = client.patch(f"/tasks/{task_id}", json={"due_date": yesterday})
    assert change.status_code == 200
    assert change.json()["due_date"] == yesterday

    # clear due date
    clear = client.patch(f"/tasks/{task_id}", json={"due_date": None})
    assert clear.status_code == 200
    assert clear.json()["due_date"] is None
    assert clear.json()["overdue"] is False


def test_overdue_rule_for_past_today_future_and_none(client):
    today = datetime.now(timezone.utc).date()
    past = (today - timedelta(days=1)).isoformat()
    today_s = today.isoformat()
    future = (today + timedelta(days=1)).isoformat()

    r1 = client.post("/tasks", json={"title": "past", "due_date": past})
    assert r1.status_code == 201
    r2 = client.post("/tasks", json={"title": "today", "due_date": today_s})
    assert r2.status_code == 201
    r3 = client.post("/tasks", json={"title": "future", "due_date": future})
    assert r3.status_code == 201
    r4 = client.post("/tasks", json={"title": "none"})
    assert r4.status_code == 201

    all_tasks = client.get("/tasks").json()
    by_title = {t["title"]: t for t in all_tasks}

    assert by_title["past"]["overdue"] is True
    assert by_title["today"]["overdue"] is False
    assert by_title["future"]["overdue"] is False
    assert by_title["none"]["overdue"] is False


def test_overdue_filtering_and_combination_with_status_and_priority(client):
    today = datetime.now(timezone.utc).date()
    past = (today - timedelta(days=1)).isoformat()
    future = (today + timedelta(days=1)).isoformat()

    # overdue, ToDo, High
    r1 = client.post("/tasks", json={"title": "A", "due_date": past, "status": "ToDo", "priority": "High"})
    assert r1.status_code == 201
    # not overdue, ToDo, Low
    r2 = client.post("/tasks", json={"title": "B", "due_date": future, "status": "ToDo", "priority": "Low"})
    assert r2.status_code == 201
    # not overdue, Done, High
    r3 = client.post("/tasks", json={"title": "C", "due_date": future, "status": "Done", "priority": "High"})
    assert r3.status_code == 201

    resp_overdue_true = client.get("/tasks", params={"overdue": "true"})
    assert resp_overdue_true.status_code == 200
    data_true = resp_overdue_true.json()
    assert all(t["overdue"] is True for t in data_true)
    assert any(t["title"] == "A" for t in data_true)

    resp_overdue_false = client.get("/tasks", params={"overdue": "false"})
    assert resp_overdue_false.status_code == 200
    data_false = resp_overdue_false.json()
    assert all(t["overdue"] is False for t in data_false)
    assert any(t["title"] == "B" for t in data_false)
    assert any(t["title"] == "C" for t in data_false)

    # omitted preserves normal list behavior (all tasks)
    resp_all = client.get("/tasks")
    assert resp_all.status_code == 200
    assert len(resp_all.json()) >= 3

    # overdue + status
    resp_combo = client.get("/tasks", params={"overdue": "true", "status": "ToDo"})
    assert resp_combo.status_code == 200
    combo_data = resp_combo.json()
    assert all(t["overdue"] is True and t["status"] == "ToDo" for t in combo_data)

    # overdue + priority
    resp_combo2 = client.get("/tasks", params={"overdue": "true", "priority": "High"})
    assert resp_combo2.status_code == 200
    combo2_data = resp_combo2.json()
    assert all(t["overdue"] is True and t["priority"] == "High" for t in combo2_data)


def test_add_comment_valid_returns_201_and_strips_whitespace(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "  first comment  "},
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["task_id"] == created_task["id"]
    assert data["text"] == "first comment"
    assert "created_at" in data


def test_add_comment_empty_text_returns_422_and_does_not_create_comment(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": ""},
    )

    assert response.status_code == 422

    comments_response = client.get(f"/tasks/{created_task['id']}/comments")
    assert comments_response.status_code == 200
    assert comments_response.json() == []


def test_add_comment_whitespace_text_returns_422_and_does_not_create_comment(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "   "},
    )

    assert response.status_code == 422

    comments_response = client.get(f"/tasks/{created_task['id']}/comments")
    assert comments_response.status_code == 200
    assert comments_response.json() == []


def test_list_comments_for_existing_task_without_comments_returns_200_and_empty_list(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}/comments")

    assert response.status_code == 200
    assert response.json() == []


def test_list_comments_returns_oldest_to_newest_and_only_for_requested_task(client):
    task_a = client.post("/tasks", json={"title": "Task A"}).json()
    task_b = client.post("/tasks", json={"title": "Task B"}).json()

    first = client.post(f"/tasks/{task_a['id']}/comments", json={"text": "first"})
    assert first.status_code == 201

    other_task = client.post(f"/tasks/{task_b['id']}/comments", json={"text": "other"})
    assert other_task.status_code == 201

    second = client.post(f"/tasks/{task_a['id']}/comments", json={"text": "second"})
    assert second.status_code == 201

    response = client.get(f"/tasks/{task_a['id']}/comments")
    assert response.status_code == 200
    data = response.json()

    assert [comment["text"] for comment in data] == ["first", "second"]
    assert all(comment["task_id"] == task_a["id"] for comment in data)


def test_delete_existing_comment_returns_204_and_comment_no_longer_listed(client, created_task):
    create_response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "to be deleted"},
    )
    assert create_response.status_code == 201
    comment_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{created_task['id']}/comments/{comment_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    comments_response = client.get(f"/tasks/{created_task['id']}/comments")
    assert comments_response.status_code == 200
    assert comments_response.json() == []


def test_list_comments_for_missing_task_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{task_id}/comments")

    assert response.status_code == 404


def test_add_comment_for_missing_task_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    response = client.post(f"/tasks/{task_id}/comments", json={"text": "hello"})

    assert response.status_code == 404


def test_delete_comment_for_missing_task_returns_404(client):
    task_id = "00000000-0000-0000-0000-000000000000"
    comment_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{task_id}/comments/{comment_id}")

    assert response.status_code == 404


def test_delete_missing_comment_for_existing_task_returns_404(client, created_task):
    comment_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{created_task['id']}/comments/{comment_id}")

    assert response.status_code == 404
