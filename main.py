from flask import Flask, request, redirect, render_template, session, jsonify
import json
import random
import os, sys
import pickle

app = Flask(__name__)
app.secret_key = os.urandom(24)
AUTHTOKEN = os.environ.get("BCLOUD_AUTHTOKEN")
print(f"Current authtoken: {AUTHTOKEN}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    return render_template("newpost.html")

@app.route("/publish", methods=["POST"])
def publish():
    if request.form["authtoken"] == os.environ.get("BCLOUD_AUTHTOKEN"):
        posts_db = pickle.load(open("data/posts.pkl", "rb"))
        post_id = str(random.randint(10000, 99999))
        post = {"header": request.form["header"], "body": request.form["body"], "id": post_id}
        print(post)
        posts_db.add(post)
        pickle.dump(posts_db, open("data/posts.pkl", "wb"))
        if not ("posts" in session):
            session["posts"] = []
        session["posts"].append(post_id)
        return redirect(f"/posts/{post_id}")
    else:
        return "Неверный ключ", 403

@app.route("/posts/<post_id>")
def posts(post_id):
    posts_db = pickle.load(open("data/posts.pkl", "rb"))
    if posts_db.get(post_id) is not None:
        post = posts_db.get(post_id)
        return render_template("post.html", header=post["header"], body=post["body"])
    else:
        return "Not Found", 404

if __name__ == "__main__":
    if len(sys.argv) == 3:
        app.run(debug=False, host=sys.argv[1], port=sys.argv[2])
    else:
        app.run(debug=False)

@app.route("/admin/api/{token}/{do}", methods=["GET"])
def admin_features(token, do):
    tokens = json.load(open("data/api_tokens.json"))
    if token not in tokens:
        return 403
    else:
        return 403
