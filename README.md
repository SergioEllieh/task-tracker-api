# Task Tracker API

A simple REST API for managing tasks, built with **Python**, **FastAPI**, and **Pydantic**, as a Module 1 learning project.

This project uses **local JSON file storage** for task persistence instead of a database, in order to keep the focus on learning REST API design, FastAPI, and request/response validation with Pydantic (see ADR-001).

## Project Status

This skeleton currently includes only the base application setup and a `/health` endpoint. CRUD endpoints for tasks will be added in a later step.

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic
- python-dotenv

## Project Structure