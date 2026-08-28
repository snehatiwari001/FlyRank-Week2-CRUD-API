from fastapi import FastAPI, HTTPException, Body

app = FastAPI()


# In-memory list of tasks
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Complete FlyRank Week 2", "done": False}
]


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
    return tasks


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

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

    new_task = {
        "id": max(task["id"] for task in tasks) + 1,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task
@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, data: dict = Body(...)):
    for task in tasks:
        if task["id"] == task_id:

            if "title" in data:
                if not data["title"] or not data["title"].strip():
                    raise HTTPException(
                        status_code=400,
                        detail="Title cannot be empty"
                    )
                task["title"] = data["title"]

            if "done" in data:
                task["done"] = data["done"]

            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )