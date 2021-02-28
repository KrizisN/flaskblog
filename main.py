from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Article {self.id}"


@app.route("/")
def home_view():
    posts = Article.query.order_by(Article.date).all()
    return render_template("home.html", posts=posts)


@app.route("/add-post", methods=["POST", "GET"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except:
            return "Ошибка"
        return render_template("home.html")
    else:
        return render_template("add_post.html")


@app.route("/post/<int:id>")
def detail_post(id):
    post = Article.query.get(id)
    return render_template("detail_post.html", post=post)


@app.route("/post/<int:id>/del")
def delete_post(id):
    post = Article.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка"
    return render_template("home.html", post=post)


@app.route("/post/<int:id>/update", methods=["POST", "GET"])
def update_post(id):
    post = Article.query.get(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.intro = request.form["intro"]
        post.text = request.form["text"]
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка"
    else:
        return render_template("update_post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
