import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db():
    return psycopg2.connect(DATABASE_URL)


def get_all_tasks():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT id, title, done FROM tasks ORDER BY id")
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return [dict(task) for task in tasks]


def get_task_by_id(task_id):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        "SELECT id, title, done FROM tasks WHERE id = %s",
        (task_id,)
    )
    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return dict(task) if task else None


def create_task(title):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING id, title, done
        """,
        (title, False)
    )

    task = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return dict(task)


def update_task(task_id, title=None, done=None):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if title is not None and done is not None:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s, done = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (title, done, task_id)
        )
    elif title is not None:
        cursor.execute(
            """
            UPDATE tasks
            SET title = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (title, task_id)
        )
    elif done is not None:
        cursor.execute(
            """
            UPDATE tasks
            SET done = %s
            WHERE id = %s
            RETURNING id, title, done
            """,
            (done, task_id)
        )
    else:
        cursor.execute(
            """
            SELECT id, title, done
            FROM tasks
            WHERE id = %s
            """,
            (task_id,)
        )

    task = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return dict(task) if task else None


def delete_task(task_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    cursor.close()
    conn.close()

    return deleted