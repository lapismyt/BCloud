from flask import Flask, request, redirect, render_template, session, jsonify
import json
import random
import os, sys
import pickle
from flaskext.markdown import Markdown
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
AUTHTOKEN = os.environ.get("BCLOUD_AUTHTOKEN")
print(f"Current authtoken: {AUTHTOKEN}")
here = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    return render_template("newpost.html")

@app.route("/publish", methods=["POST"])
def publish():
    if request.form["authtoken"] == os.environ.get("BCLOUD_AUTHTOKEN"):
        posts_db = json.load(open("data/posts.json"))
        post_id = str(random.randint(10000, 99999))
        post = {"header": request.form["header"], "body": request.form["body"], "id": post_id}
        print(post)
        posts_db[post_id] = post
        json.dump(posts_db, open("data/posts.json", "w"))
        if not ("posts" in session):
            session["posts"] = []
        session["posts"].append(post_id)
        return redirect(f"/posts/{post_id}")
    else:
        return "Неверный ключ", 403

@app.route("/posts/<post_id>")
def posts(post_id): 
    posts_db = json.load(open("data/posts.json"))
    if posts_db.get(post_id) is not None:
        post = posts_db.get(post_id)
        res = render_template("post.html", header=post["header"], body=post["body"])
        return res
    else:
        return "<h1>Not Found</h1>", 404

if __name__ == "__main__":
    if len(sys.argv) == 3:
        app.run(debug=False, host=sys.argv[1], port=sys.argv[2])
    else:
        app.run(debug=False)
