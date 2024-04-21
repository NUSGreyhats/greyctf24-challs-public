import os
from flask import Flask, render_template, session

app = Flask(__name__)
app.secret_key = "baby-web"
FLAG = "grey{0h_n0_mY_5up3r_53cr3t_4dm1n_fl4g}"


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


@app.route("/flag")
def flag():
    if session.get("is_admin"):
        return render_template("flag.html", flag=FLAG)
    return render_template("index.html", message="You are not admin")

@app.route("/rickroll")
def rickroll():
    return render_template("rickroll.html")


if __name__ == "__main__":
    app.run(debug=True)
