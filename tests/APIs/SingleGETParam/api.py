from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 9, "name": "Bob"},
    {"id": 30, "name": "Charlie"},
    {"id": 1000, "name": "David"},
]


@app.route("/api/v1/users", methods=["GET"])
def get_user():
    user_id = request.args.get("id", type=int)

    if user_id is None:
        return jsonify({"error": "Missing 'id' parameter"}), 400

    user = next((user for user in users if user["id"] == user_id), None)

    if user:
        return jsonify(user)
    else:
        return jsonify({"error": f"User with id {user_id} not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
