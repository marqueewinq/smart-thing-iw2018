import json
import requests
import os
from flask import Flask, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from db import get_db, init_db
from utility import get_new_token, get_data_list

app = Flask(__name__)


@app.route("/")
def index():
    """Show all the posts, most recent first."""

    db = get_db()
    data_list = json.dumps(get_data_list())
    user_list = db.execute("SELECT id, token FROM user").fetchall()
    caller_url = os.environ.get("BASE_URL")
    return render_template(
        "index.html",
        data_list=data_list,
        user_list=user_list,
        caller_url=caller_url,
    )


@app.route("/api/get")
def api_get():
    return json.dumps(get_data_list())


@app.route("/api/register")
def api_register():
    token = get_new_token()
    db = get_db()
    db.execute("INSERT INTO user (token) VALUES (?)", (token,))
    db.commit()
    return (
        json.dumps({"success": True, "token": token}),
        200,
        {"ContentType": "application/json"},
    )


@app.route("/api/add", methods=["POST"])
def api_add():
    js = request.json
    if type(js) != dict or "token" not in js:
        return json.dumps(
            {"success": False, "detail": "No token provided"},
            401,
            {"ContentType": "application/json"},
        )
    token = js.get("token")
    db = get_db()
    all_tokens = [
        {"id": item[0], "token": item[1]}
        for item in db.execute("SELECT id, token from user", ()).fetchall()
    ]
    found = False
    for token_h in all_tokens:
        if token == token_h["token"]:
            found = True
            break

    if len(all_tokens) == 0 or not found:
        return json.dumps(
            {"success": False, "detail": "Token not found"},
            401,
            {"ContentType": "application/json"},
        )
    user = all_tokens[0]

    if "data" not in js:
        return json.dumps(
            {"success": False, "detail": "Data not found"},
            401,
            {"ContentType": "application/json"},
        )
    try:
        data = json.dumps(js["data"])
    except ValueError:
        return json.dumps(
            {"success": False, "detail": "Data can't be parsed into JSON"},
            401,
            {"ContentType": "application/json"},
        )

    db.execute("INSERT INTO post (author_id, data) values (?, ?)", (user["id"], data))
    db.commit()
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


if __name__ == "__main__":
    # we need app context to perform sql queries
    ctx = app.app_context()
    ctx.push()
    init_db()
    ctx.pop()  # end of context

    app.run(debug=True, host="0.0.0.0")
