import sqlite3

def query_database(query: str) -> str:
    try:
        conn = sqlite3.connect("enterprise.db")
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return str(rows)

    except Exception as e:
        return f"Database Error: {e}"