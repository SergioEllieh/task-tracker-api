# Task Tracker API

A REST API and simple frontend for managing tasks, built with **Python**, **FastAPI**, **Pydantic**, and a lightweight web interface.

The project was developed throughout the AI-Assisted Coding course and extended during the Mid-Course Project.

## Mid-Course Features

The two selected features for the Mid-Course Project are:

1. **Due Dates + Overdue Filter**

   * Tasks can have an optional due date.
   * Due dates can be added and updated.
   * Overdue tasks can be identified and filtered.
   * Due dates are displayed in the frontend.

2. **Task Comments**

   * Comments can be added to tasks.
   * Blank or whitespace-only comments are rejected.
   * Comments can be listed for an individual task.
   * Comments can be deleted.
   * Missing tasks and comments return appropriate 404 responses.

## Tech Stack

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* Pytest
* HTML
* CSS
* JavaScript

## Run the Backend

Open a terminal in the project root.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Open the Frontend

First, make sure the backend is running.

Then open the frontend file located at:

```text
frontend/index.html
```

You can open `index.html` directly in your browser.

If your project serves the frontend through FastAPI, use the frontend URL configured by the application instead.

## Run the Tests

Make sure the virtual environment is activated and the dependencies are installed.

From the project root, run:

```bash
pytest
```

For more detailed test output:

```bash
pytest -v
```

All existing tests and Mid-Course Project feature tests should pass before submission.

## Mid-Course Documentation

The required Mid-Course Project documentation is located in:

```text
docs/midcourse/
```

The folder contains:

* `user-stories.md`
* `mini-adr.md`
* `prompt-log.md`
* `verification.md`
* `reflection.md`

## Development Branch

The Mid-Course Project submission branch is:

```text
mid-course-project
```

## Final Verification

Before submitting the project, run:

```bash
pytest -v
```

Confirm that there are **zero failing tests**.

Also verify manually that:

* Tasks can be created and edited.
* Due dates can be added and updated.
* Overdue tasks are detected correctly.
* The overdue filter works.
* Comments can be added to tasks.
* Blank comments are rejected.
* Comments can be listed and deleted.
* The frontend loads and remains usable.
