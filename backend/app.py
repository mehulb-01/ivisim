from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from simulator import IVISimulator

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

simulator = IVISimulator()

@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/api/state")
def state():
    return jsonify(simulator.state())

@app.post("/api/action")
def action():
    data = request.get_json(silent=True) or {}
    command = str(data.get("command", "")).lower()

    if command not in {"play", "pause", "next", "stop"}:
        return jsonify({"error": "Invalid command"}), 400

    return jsonify(simulator.handle_command(command))

@app.post("/api/volume")
def volume():
    data = request.get_json(silent=True) or {}
    try:
        value = int(data.get("volume"))
    except (TypeError, ValueError):
        return jsonify({"error": "Volume must be an integer"}), 400

    value = max(0, min(100, value))
    return jsonify(simulator.set_volume(value))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
