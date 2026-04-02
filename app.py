from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Recreating the core gym database structure
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, program TEXT)")
    cur.execute("INSERT OR IGNORE INTO clients (id, name, program) VALUES (1, 'Admin User', 'Elite Muscle Gain')")
    conn.commit()
    conn.close()    

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    # Ensure table exists every time we connect (safe for SQLite)
    conn.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY, name TEXT, program TEXT)")
    return conn

@app.route('/members')
def get_members():
    conn = get_db_connection() # Use the helper instead of raw connect
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "program": r[2]} for r in rows])

@app.route('/')
def home():
    return jsonify({"message": "Welcome to ACEest Fitness Web API"})

@app.route('/status')
def status():
    # REQUIRED for your Jenkins/GitHub Actions health checks
    return jsonify({"status": "Healthy", "version": "3.2.4"})

@app.route('/members')
def get_members():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "program": r[2]} for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)