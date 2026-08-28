from fastapi import FastAPI, HTTPException, Body

app = FastAPI()


# In-memory list of tasks
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Complete FlyRank Week 2", "done": False}
]


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201)
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