from flask import Flask, request, render_template
import os
import json
import re
from util import get_challenge_author

app = Flask(__name__)
cur_dir = os.path.dirname(__file__)

token = open(os.path.join(cur_dir, "token.txt")).read()

def get_votes():
    return json.load(open("./votes.json"))

def set_votes(votes):
    return json.dump(votes, open("./votes.json", "w"))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", votes=get_votes())

@app.route("/flag", methods=["GET"])
def flag():
    get_token = request.args.get("token", default="")
    if not re.match(r"^[a-f0-9]{32}$", get_token):
        return "Invalid token!"
    if get_token == token:
        return open("./flag.txt")
    return "Invalid token!"

@app.route("/form_response", methods=["POST"])
def form_response():
    post_token = request.form.get("token")
    if token != post_token:
        return "Invalid token!"
    
    team_name = request.args.get("teamname")
    if not team_name:
        return "No flag for you!"
    
    challenge_file_id = request.args.get("challenge_file_id")
    if not challenge_file_id:
        return "Huhhh???"
    
    difficulty = request.form.get("difficulty")
    try:
        difficulty = int(difficulty)
    except:
        return "???"
    
    if difficulty == 5:
        return "It is impossible!"
    
    best_chal = request.form.get("best_chal")
    print(team_name, challenge_file_id, difficulty, best_chal)


    best_chal_author = get_challenge_author(challenge_file_id, best_chal)

    author_votes = get_votes()
    if not best_chal_author or best_chal_author not in author_votes:
        return "Author not exist???"
    
    # Yay
    author_votes[best_chal_author] += 1
    set_votes(author_votes)
    print("Updated votes for", best_chal_author)
    return "Success!"