\# FlyRank Week 2 — CRUD API



A simple \*\*Task CRUD API\*\* built with \*\*Python and FastAPI\*\* as part of the FlyRank Week 2 assignment.



The API manages an in-memory list of tasks and supports the four CRUD operations:



\* \*\*Create\*\* — `POST /tasks`

\* \*\*Read\*\* — `GET /tasks` and `GET /tasks/{task\_id}`

\* \*\*Update\*\* — `PUT /tasks/{task\_id}`

\* \*\*Delete\*\* — `DELETE /tasks/{task\_id}`



Data is stored only in memory, so tasks are reset when the server restarts.



\## Tech Stack



\* Python 3.10+

\* FastAPI

\* Uvicorn

\* Swagger UI / OpenAPI



\## Installation and Run



\### 1. Activate the virtual environment



On Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 2. Install dependencies



```powershell

pip install fastapi uvicorn

```



\### 3. Start the server



```powershell

uvicorn main:app --reload

```



The API will be available at:



```text

http://127.0.0.1:8000

```



\## Swagger UI



FastAPI automatically provides interactive API documentation at:



```text

http://127.0.0.1:8000/docs

```



Swagger UI can be used to test the complete CRUD cycle without curl.



\## API Endpoints



| Method | Endpoint           | Description       | Success |

| ------ | ------------------ | ----------------- | ------- |

| GET    | `/`                | API information   | 200     |

| GET    | `/health`          | Check API health  | 200     |

| GET    | `/tasks`           | List all tasks    | 200     |

| GET    | `/tasks/{task\_id}` | Get a task by ID  | 200     |

| POST   | `/tasks`           | Create a new task | 201     |

| PUT    | `/tasks/{task\_id}` | Update a task     | 200     |

| DELETE | `/tasks/{task\_id}` | Delete a task     | 204     |



\### Error Responses



| Status | Meaning                       |

| ------ | ----------------------------- |

| 400    | Invalid or missing task title |

| 404    | Task ID not found             |



\## Example Task



```json

{

&#x20; "id": 1,

&#x20; "title": "Learn FastAPI",

&#x20; "done": false

}

```



\## Example curl Test



\### Get all tasks



```bash

curl -i http://127.0.0.1:8000/tasks

```



Example response:



```text

HTTP/1.1 200 OK

content-type: application/json



\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "title": "Learn FastAPI",

&#x20;   "done": false

&#x20; },

&#x20; {

&#x20;   "id": 2,

&#x20;   "title": "Build a CRUD API",

&#x20;   "done": false

&#x20; },

&#x20; {

&#x20;   "id": 3,

&#x20;   "title": "Complete FlyRank Week 2",

&#x20;   "done": false

&#x20; }

]

```



\## CRUD Flow



The API supports the complete CRUD lifecycle:



```text

POST /tasks

&#x20;    ↓

GET /tasks/{task\_id}

&#x20;    ↓

PUT /tasks/{task\_id}

&#x20;    ↓

DELETE /tasks/{task\_id}

```



The complete CRUD cycle was also tested through Swagger UI.



\## Project Structure



```text

FlyRank-Week2-CRUD-API/

├── main.py

├── .gitignore

├── README.md

└── venv/

```



> The `venv/` directory is local to the development environment and is not committed to GitHub.



\## Status



✅ Stage 0 — Hello server

✅ Stage 1 — Root and health endpoints

✅ Stage 2 — Read endpoints with 404

✅ Stage 3 — Create task with validation

✅ Stage 4 — Update and delete task

✅ Stage 5 — Swagger UI

✅ Stage 6 — GitHub publication and documentation

\## Swagger UI Screenshot



!\[Swagger UI](swagger.png)



