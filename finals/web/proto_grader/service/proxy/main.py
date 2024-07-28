from flask import Flask, request
import os
import json
import base64
import subprocess

app = Flask(__name__)
cur_dir = os.path.dirname(__file__)

index_html = open(os.path.join(cur_dir, "index.html")).read()


@app.route("/", methods=["GET"])
def index():
    return index_html


@app.route("/grade", methods=["POST"])
def receive_grade():
    data = request.get_json()
    data = json.dumps(data).encode()

    try:
        out = subprocess.check_output(
            [
                "node",
                os.path.join(cur_dir, "../backend/index.js"),
                base64.b64encode(data),
            ]
        ).decode()
        if int(out) < 3:
            print("solve", data)
            return json.load(open(os.path.join(cur_dir, "../config.json")))["flag"]
        else:
            print(out)
            return "Wrong answer!"
    except Exception:
        return "Process crashed or didn't return an integer"
