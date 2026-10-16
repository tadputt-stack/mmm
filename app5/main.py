import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI(title="app5-movies-store")

DB_NAME = r"C:\Users\ICT69\Downloads\sever-side-app\app5\movies.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_table_name(conn):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%movies%';"
    )
    row = cursor.fetchone()
    return f'"{row[0]}"' if row else '"movies"'


@app.get("/")
def read_root():
    return {"message": "Welcome to Movies Store API"}



@app.get("/movies")
def get_all_movies():
    conn = get_db_connection()
    table = get_table_name(conn)
    movies = conn.execute(f"SELECT * FROM {table}").fetchall()
    conn.close()
    return [dict(movie) for movie in movies]



@app.get("/movies/{identifier}")
def get_movie_by_id_or_title(identifier: str):  
    conn = get_db_connection()
    table = get_table_name(conn)

    
    if identifier.isdigit():
        movie = conn.execute(
            f"SELECT * FROM {table} WHERE id = ?", (int(identifier),)
        ).fetchone()
    else:
        
        movie = conn.execute(
            f"SELECT * FROM {table} WHERE title LIKE ?", (f"%{identifier}%",)
        ).fetchone()

    conn.close()

    if movie is None:
        raise HTTPException(
            status_code=404, detail=f"Movie '{identifier}' not found"
        )

    return dict(movie)