from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host="postgres",
        user="postgres",
        password="rootpass",
        dbname="pessoas"
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
