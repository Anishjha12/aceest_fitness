from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

# ---------- DATABASE HELPER ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Users Table
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, role TEXT)")
    # Clients Table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            program TEXT,
            membership_status TEXT
        )
    """)
    # Add default data for tests
    conn.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'Admin')")
    conn.execute("INSERT OR IGNORE INTO clients (name, program, membership_status) VALUES ('Test User', 'Muscle Gain', 'Active')")
    conn.commit()
    conn.close()

# ---------- WEB ROUTES (API) ----------

@app.route('/')
def home():
    return jsonify({"message": "ACEest Fitness API Online", "version": "3.2.4"})

@app.route('/status')
def status():
    """Health check endpoint for Jenkins/GitHub Actions"""
    return jsonify({"status": "Healthy", "database": "Connected"})

@app.route('/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    members = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return jsonify([dict(row) for row in members])

if __name__ == "__main__":
    init_db()
    # Use 0.0.0.0 for Docker compatibility
    app.run(host='0.0.0.0', port=5000)