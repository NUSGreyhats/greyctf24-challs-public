import os
from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = "baby-web"
FLAG = os.getenv("FLAG", r"grey{fake_flag}")


@app.route("/", methods=["GET"])
def index():
    # Set session if not found
    if "is_admin" not in session:
        session["is_admin"] = False
    return render_template("index.html")


@app.route("/admin")
def admin():
    # Check if the user is admin through cookies
    return render_template("admin.html", flag=FLAG, is_admin=session.get("is_admin"))

### Some other hidden code ###


if __name__ == "__main__":
    app.run(debug=True)
