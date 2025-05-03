# Task API

A Django REST API for managing tasks.

## Features

- Create, read, update, and delete tasks
- Filter tasks by status
- Mark tasks as completed

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start the server: `python manage.py runserver`

## API Endpoints

- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/{id}/` - Get a specific task
- `POST /tasks/{id}/complete/` - Mark a task as completed
