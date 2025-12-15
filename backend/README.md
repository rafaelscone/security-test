# Todo List API

A simple REST API for managing todos built with FastAPI and SQLite.

## Features

- Create, read, update, and delete todos
- SQLite database with automatic initialization
- RESTful API endpoints
- Interactive API documentation

## Installation

1. Install dependencies:
```bash
python3.12 -m venv venv
source venv/bin
pip3 install -r requirements.txt
```

## Running the Application

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Get all todos
```
GET /todos
```

### Get a specific todo
```
GET /todos/{todo_id}
```

### Create a new todo
```
POST /todos
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

### Update a todo
```
PUT /todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true
}
```

### Delete a todo
```
DELETE /todos/{todo_id}
```

## Database

The application uses SQLite with a file named `todos.db`. The database and tables are automatically created when the application starts.
