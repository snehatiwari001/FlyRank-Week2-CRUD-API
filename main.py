from fastapi import FastAPI, HTTPException, Body

import repository

app = FastAPI()


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
    return repository.get_all_tasks()


@app.get("/tasks/{task_id}", summary="Get a task by ID")
def get_task(task_id: int):
    task = repository.get_task_by_id(task_id)

    if task:
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

    return repository.create_task(title)


@app.put("/tasks/{task_id}", summary="Update a task")
def update_task(task_id: int, data: dict = Body(...)):
    task = repository.get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    if "title" in data:
        if not data["title"] or not data["title"].strip():
            raise HTTPException(
                status_code=400,
                detail="Title cannot be empty"
            )

    updated_task = repository.update_task(
        task_id,
        title=data.get("title"),
        done=data.get("done")
    )

    return updated_task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    deleted = repository.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return