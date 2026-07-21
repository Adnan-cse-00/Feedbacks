from flask import Blueprint, render_template

from app.models.forum import Forum

main = Blueprint("main", __name__)


@main.route("/")
def home():

    forums = Forum.query.order_by(
        Forum.created_at.desc()
    ).all()

    return render_template(
        "pages/home.html",
        forums=forums
    )


@main.route("/about")
def about():
    return render_template("pages/about.html")


@main.route("/contact")
def contact():
    return render_template("pages/contact.html")