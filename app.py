from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)

# In-memory data stores
members = {}
classes = {}
trainers = {}
bookings = {}

_member_id_counter = 1
_class_id_counter = 1
_trainer_id_counter = 1
_booking_id_counter = 1


# ──────────────────────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "app": "ACEest Fitness & Gym",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


# ──────────────────────────────────────────────────────────────
# Members
# ──────────────────────────────────────────────────────────────
@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(list(members.values())), 200


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = members.get(member_id)
    if not member:
        abort(404)
    return jsonify(member), 200


@app.route("/members", methods=["POST"])
def add_member():
    global _member_id_counter
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400

    member = {
        "id": _member_id_counter,
        "name": data["name"],
        "email": data["email"],
        "membership_type": data.get("membership_type", "basic"),
        "join_date": datetime.utcnow().isoformat()
    }
    members[_member_id_counter] = member
    _member_id_counter += 1
    return jsonify(member), 201


@app.route("/members/<int:member_id>", methods=["PUT"])
def update_member(member_id):
    member = members.get(member_id)
    if not member:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    member.update({k: v for k, v in data.items() if k in ("name", "email", "membership_type")})
    return jsonify(member), 200


@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    if member_id not in members:
        abort(404)
    del members[member_id]
    return jsonify({"message": "Member deleted"}), 200


# ──────────────────────────────────────────────────────────────
# Fitness Classes
# ──────────────────────────────────────────────────────────────
@app.route("/classes", methods=["GET"])
def get_classes():
    return jsonify(list(classes.values())), 200


@app.route("/classes/<int:class_id>", methods=["GET"])
def get_class(class_id):
    fitness_class = classes.get(class_id)
    if not fitness_class:
        abort(404)
    return jsonify(fitness_class), 200


@app.route("/classes", methods=["POST"])
def add_class():
    global _class_id_counter
    data = request.get_json()
    if not data or "name" not in data or "schedule" not in data:
        return jsonify({"error": "name and schedule are required"}), 400

    fitness_class = {
        "id": _class_id_counter,
        "name": data["name"],
        "schedule": data["schedule"],
        "trainer_id": data.get("trainer_id"),
        "capacity": data.get("capacity", 20),
        "enrolled": 0
    }
    classes[_class_id_counter] = fitness_class
    _class_id_counter += 1
    return jsonify(fitness_class), 201


# ──────────────────────────────────────────────────────────────
# Trainers
# ──────────────────────────────────────────────────────────────
@app.route("/trainers", methods=["GET"])
def get_trainers():
    return jsonify(list(trainers.values())), 200


@app.route("/trainers", methods=["POST"])
def add_trainer():
    global _trainer_id_counter
    data = request.get_json()
    if not data or "name" not in data or "specialization" not in data:
        return jsonify({"error": "name and specialization are required"}), 400

    trainer = {
        "id": _trainer_id_counter,
        "name": data["name"],
        "specialization": data["specialization"],
        "experience_years": data.get("experience_years", 0)
    }
    trainers[_trainer_id_counter] = trainer
    _trainer_id_counter += 1
    return jsonify(trainer), 201


# ──────────────────────────────────────────────────────────────
# Bookings
# ──────────────────────────────────────────────────────────────
@app.route("/bookings", methods=["GET"])
def get_bookings():
    return jsonify(list(bookings.values())), 200


@app.route("/bookings", methods=["POST"])
def create_booking():
    global _booking_id_counter
    data = request.get_json()
    if not data or "member_id" not in data or "class_id" not in data:
        return jsonify({"error": "member_id and class_id are required"}), 400

    member_id = data["member_id"]
    class_id = data["class_id"]

    if member_id not in members:
        return jsonify({"error": "Member not found"}), 404
    if class_id not in classes:
        return jsonify({"error": "Class not found"}), 404

    fitness_class = classes[class_id]
    if fitness_class["enrolled"] >= fitness_class["capacity"]:
        return jsonify({"error": "Class is fully booked"}), 409

    booking = {
        "id": _booking_id_counter,
        "member_id": member_id,
        "class_id": class_id,
        "booked_at": datetime.utcnow().isoformat(),
        "status": "confirmed"
    }
    bookings[_booking_id_counter] = booking
    fitness_class["enrolled"] += 1
    _booking_id_counter += 1
    return jsonify(booking), 201


@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    booking = bookings.get(booking_id)
    if not booking:
        abort(404)
    class_id = booking["class_id"]
    if class_id in classes:
        classes[class_id]["enrolled"] = max(0, classes[class_id]["enrolled"] - 1)
    del bookings[booking_id]
    return jsonify({"message": "Booking cancelled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
