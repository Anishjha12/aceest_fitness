from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ACEest System Online"}), 200

@app.route('/generate_program/<client_name>', methods=['POST'])
def generate_program(client_name):
    programs = ["Fat Loss", "Muscle Gain", "Beginner"]
    selected = random.choice(programs)
    # Logic to update DB would go here
    return jsonify({"client": client_name, "assigned_program": selected})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)