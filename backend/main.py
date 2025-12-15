from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import init_database, get_db

app = FastAPI(title="Todo List API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

aws = {
    "region": "eu-central-1",
    "access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
}

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_database()

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Todo List API", "docs": "/docs"}

@app.get("/todos", response_model=list[Todo])
async def get_todos():
    """Get all todos."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get a specific todo by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return dict(row)

@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    """Create a new todo."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, description) VALUES (?, ?)",
            (todo.title, todo.description)
        )
        conn.commit()
        todo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return dict(row)

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoUpdate):
    """Update an existing todo."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        update_fields = []
        params = []

        if todo.title is not None:
            update_fields.append("title = ?")
            params.append(todo.title)
        if todo.description is not None:
            update_fields.append("description = ?")
            params.append(todo.description)
        if todo.completed is not None:
            update_fields.append("completed = ?")
            params.append(todo.completed)

        if update_fields:
            params.append(todo_id)
            query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()

        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return dict(row)

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    """Delete a todo."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
