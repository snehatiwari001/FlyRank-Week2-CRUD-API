from fastapi import FastAPI, HTTPException, Body
import sqlite3

app = FastAPI()

DATABASE = "tasks.db"


# Connect to database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create table and insert example tasks if database is empty
def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]

    if count == 0:
        conn.executemany(
            "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
            [
                (1, "Learn FastAPI", False),
                (2, "Build a CRUD API", False),
                (3, "Complete FlyRank Week 2", False)
            ]
        )

    conn.commit()
    conn.close()


# Initialize database when application starts
init_db()


@app.get("/", summary="API information")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", summary="Check API health")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def get_tasks():
    conn = get_db()

    tasks = conn.execute(
        "SELECT id, title, done FROM tasks"
    ).fetchall()

    conn.close()

    return [dict(task) for task in tasks]


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    conn = get_db()

    task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if task:
        return dict(task)

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(data: dict = Body(...)):
    title = data.get("title")

    if not title or not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    conn = get_db()

    new_id = conn.execute(
        "SELECT COALESCE(MAX(id), 0) + 1 FROM tasks"
    ).fetchone()[0]

    conn.execute(
        "INSERT INTO tasks (id, title, done) VALUES (?, ?, ?)",
        (new_id, title, False)
    )

    conn.commit()

    task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (new_id,)
    ).fetchone()

    conn.close()

    return dict(task)


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, data: dict = Body(...)):
    conn = get_db()

    task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if not task:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    if "title" in data:
        if not data["title"] or not data["title"].strip():
            conn.close()
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )

        conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (data["title"], task_id)
        )

    if "done" in data:
        conn.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (data["done"], task_id)
        )

    conn.commit()

    updated_task = conn.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    return dict(updated_task)


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    conn = get_db()

    task = conn.execute(
        "SELECT id FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if not task:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return