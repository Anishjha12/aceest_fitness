from flask import Flask, jsonify, request # type: ignore
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, program TEXT, status TEXT)")
    # Add a default member for testing
    cur.execute("INSERT OR IGNORE INTO clients (name, program, status) VALUES ('Admin', 'Muscle Gain', 'Active')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym API", "system": "Online"})

@app.route('/status')
def status():
    return jsonify({"status": "Healthy", "database": "Connected", "version": "3.2.4"})

@app.route('/members', methods=['GET'])
def get_members():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    members = [{"id": r[0], "name": r[1], "program": r[2]} for r in cur.fetchall()]
    conn.close()
    return jsonify(members)

if __name__ == "__main__":
    init_db()
    # Must use 0.0.0.0 for Docker compatibility
    app.run(host='0.0.0.0', port=5000)