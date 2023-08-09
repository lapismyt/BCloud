from flask import Flask, request, redirect, render_template
import json
import random
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Это облако принадлежит <a href=\"https://t.me/LapisMYT\">LapisMYT</a>"

@app.route("/newpost", methods=["GET", "POST"])
def newpost():
    return """
    <title>BCloud - New Post</title>
    <h1>Новый пост</h1>
    <form class="pform" action="/publish" method="POST">
    <textarea name="header" placeholder="Заголовок" cols="40"></textarea>
    <br/><br/>
    <textarea name="body" placeholder="Текст" cols="40" rows="30"></textarea>
    <br/><br/>
    <textarea type="password" name="authtoken" placeholder="Ключ" cols="40"></textarea>
    <br/><br/>
    <input type="submit" value="Опубликовать">
    </form>
    <style>* {font-size: 30; padding: 10px;} h1 {font-size: 50;}</style>
    """

@app.route("/publish", methods=["POST"])
def publish():
    if request.form["authtoken"] == os.environ.get("BCLOUD_AUTHTOKEN"):
        posts_db = json.load(open("posts.json"))
        post_id = str(random.randint(10000, 99999))
        post = {"header": request.form["header"], "body": request.form["body"], "id": post_id}
        print(post)
        posts_db[post_id] = post
        json.dump(posts_db, open("posts.json", "w"), ensure_ascii=True)
        return redirect(f"/posts/{post_id}")
    else:
        return "Неверный ключ", 403

@app.route("/posts/<post_id>")
def posts(post_id):
    posts_db = json.load(open("posts.json"))
    if post_id in posts_db.keys():
        post = posts_db[post_id]
        return render_template("post.html", header=post["header"], body=post["body"])
    else:
        return "Not Found", 404

if __name__ == "__main__":
    app.run()
