# Task API

A Django REST API for managing tasks with monitoring and logging capabilities.

## Features

- Create, read, and update tasks
- Get pending tasks
- Mark tasks as completed
- Prometheus metrics for monitoring
- Comprehensive logging

## Architecture

This application follows a standard Django REST Framework architecture:

- **Models**: Define the data structure for tasks
- **Views**: Handle HTTP requests and responses
- **Serializers**: Convert between JSON and Python objects
- **URLs**: Define the API endpoints

Additional components:

- **Prometheus Integration**: Provides metrics for monitoring
- **Logging**: Captures application events for debugging and auditing
- **PostgreSQL Database**: Stores task data (in Docker and production)
- **Docker**: Containerizes the application for consistent deployment

## Setup & Deployment

### Local Development

1. Clone the repository

   ```
   git clone https://github.com/tomasjelvez/task-api
   cd task-api
   ```

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Run migrations

   ```
   python manage.py migrate
   ```

4. Start the server
   ```
   python manage.py runserver
   ```

### Docker Setup

1. Build and start the containers

   ```
   docker-compose up -d --build
   ```

2. Run migrations

   ```
   docker-compose exec web python manage.py migrate
   ```

3. Create a superuser (optional)
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

### Deployment to Fly.io

1. Install the Fly CLI

   ```
   curl -L https://fly.io/install.sh | sh
   ```

2. Log in to Fly

   ```
   fly auth login
   ```

3. Launch the app (first time only)

   ```
   fly launch
   ```

4. Deploy updates
   ```
   fly deploy
   ```

## Testing

### Running Tests Locally

Run the test suite with:

```
python manage.py test
```

Or with Docker:

```
docker-compose exec web python manage.py test
```

### Manual Testing

You can test the API endpoints using tools like curl, Postman, or httpie:

```bash
# List all tasks
curl http://localhost:8000/tasks/

# Get a task by id
curl http://localhost:8000/tasks/1/
# Create a new task
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high", "status": "pending"}'

# Get a specific task
curl http://localhost:8000/tasks/1/

# Mark a task as completed
curl -X POST http://localhost:8000/tasks/1/complete/
```

## Production

### Manual Testing

You can test the API endpoints on the production environment using tools like curl, Postman, or httpie. Follow this documentation: https://documenter.getpostman.com/view/16608319/2sB2j4hBuR

## API Endpoints

- `GET /tasks/` - List all tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/{id}/` - Get a specific task
- `POST /tasks/{id}/complete/` - Mark a task as completed
- `GET /metrics/` - Prometheus metrics endpoint

## Trade-offs and Future Improvements

### Current Trade-offs

1. **Simple Authentication**: The API currently has no authentication, which simplifies development but isn't suitable for production.
2. **File-based Logging**: Logs are written to files, which works for development but isn't ideal for containerized environments.
3. **Basic Error Handling**: The error handling is minimal to keep the code simple.

### Future Improvements

With more time, I would:

1. **Add Authentication**: Implement JWT or OAuth2 authentication.
2. **Improve Logging**: Use a centralized logging service instead of file-based logging.
3. **Add Pagination**: Implement pagination for the task list endpoint.
4. **Add More Filters**: Allow filtering by priority, creation date, etc.
5. **Implement Rate Limiting**: Protect the API from abuse.
6. **Add More Tests**: Increase test coverage, especially for edge cases.

### Post Mortem

In this repo, there is a `DEPLOYMENT_FAILURE.md` file, wich aims to help for a generic case of a deployment failure on a live demo. Also, there is a `POSTMORTEM.md` file, wich outlines a specific case of that deployment failure, and how it was solved.
