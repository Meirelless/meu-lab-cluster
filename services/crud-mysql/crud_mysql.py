from fastapi import FastAPI
import mysql.connector

app = FastAPI()

def get_conn():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="rootpass",
        database="pessoas"
    )

@app.get("/pessoas")
def list_pessoas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM pessoas")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return {"pessoas": result}
