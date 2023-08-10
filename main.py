from flask import Flask, request, redirect, render_template, session, jsonify, url_for, send_from_directory
import json
import random
import os, sys
import pickle
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)
AUTHTOKEN = os.environ.get("BCLOUD_AUTHTOKEN")
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(["txt", "png", "pdf", "jpg", "gif", "jpeg", "mp3", "mp4", "apk"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print(f"Current authtoken: {AUTHTOKEN}")
here = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if request.form["key"] == AUTHTOKEN:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))
        else:
            return "<h1>Access Denied</h1>", 403
    return render_template("upload_file.html")

@app.route("/uploaded_file/<filename>")
def uploaded_file(filename):
    return render_template("uploaded_file.html", filename=filename)

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        app.run(debug=False, host=sys.argv[1], port=sys.argv[2])
    else:
        app.run(debug=False)
