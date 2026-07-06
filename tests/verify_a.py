"""Verification script for app.models."""

from datetime import datetime, timezone

from pydantic import ValidationError

from app.models import (
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)


def expect_fail(label: str, fn) -> None:
    try:
        fn()
    except ValidationError:
        print(f"{label}: PASS")
    else:
        raise AssertionError(label)


def expect_ok(label: str, fn) -> None:
    fn()
    print(f"{label}: PASS")


def verify_models() -> None:
    # 1 Whitespace title rejected
    expect_fail("#1 Whitespace title rejected", lambda: TaskCreate(title="   "))

    # 2 Empty title rejected
    expect_fail("#2 Empty title rejected", lambda: TaskCreate(title=""))

    # 3 Title over 200 chars rejected
    expect_fail("#3 Title over 200 chars rejected", lambda: TaskCreate(title="x" * 201))

    # 4 Valid title accepted, defaults applied
    def valid_title_with_defaults() -> None:
        task = TaskCreate(title="Valid title")
        assert task.title == "Valid title"
        assert task.status == TaskStatus.TODO
        assert task.priority == TaskPriority.MEDIUM
        assert task.description == ""
        assert task.assignee is None

    expect_ok("#4 Valid title accepted, defaults applied", valid_title_with_defaults)

    # 5 extra='forbid' - unknown field rejected on TaskCreate
    expect_fail(
        "#5 extra='forbid' - unknown field rejected on TaskCreate",
        lambda: TaskCreate(title="Valid title", unknown_field="nope"),
    )

    # 6 id NOT settable via TaskUpdate
    expect_fail("#6 id NOT settable via TaskUpdate", lambda: TaskUpdate(id="fake-id"))

    # 7 created_at NOT settable via TaskUpdate
    expect_fail(
        "#7 created_at NOT settable via TaskUpdate",
        lambda: TaskUpdate(created_at=datetime.now(timezone.utc)),
    )

    # 8 Invalid enum value rejected
    expect_fail(
        "#8 Invalid enum value rejected",
        lambda: TaskCreate(title="Valid title", status="NotAStatus"),
    )


def main() -> None:
    verify_models()
    print("All checks passed.")


if __name__ == "__main__":
    main()