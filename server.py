from flask import Flask, request, jsonify
import time

app = Flask(__name__)

players = {}


@app.route("/join", methods=["POST"])
def join():

    data = request.json
    pid = data["id"]

    if pid not in players:

        players[pid] = {
            "x": 500,
            "y": 100,
            "vx": 0,
            "vy": 0,
            "facing_right": True,
            "atk": False,
            "image": data["image"],
            "last_seen": time.time()
        }

    return jsonify({
        "players": players,
        "start": len(players) >= 2
    })


@app.route("/update", methods=["POST"])
def update():

    data = request.json
    pid = data["id"]

    if pid in players:

        players[pid]["x"] = data["x"]
        players[pid]["y"] = data["y"]

        players[pid]["facing_right"] = data["facing_right"]
        players[pid]["atk"] = data["atk"]
        players[pid]["vx"] = data["vx"]
        players[pid]["vy"] = data["vy"]
        players[pid]["last_seen"] = time.time()

    # Remove disconnected players
    now = time.time()

    for other_pid in list(players):

        if now - players[other_pid]["last_seen"] > 5:

            del players[other_pid]

    return jsonify(players)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
