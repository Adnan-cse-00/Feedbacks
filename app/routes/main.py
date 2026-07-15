from flask import Blueprint, render_template

from app.models.forum import Forum

main = Blueprint("main", __name__)


@main.route("/")
def home():

    reviews = Forum.query.filter_by(
        forum_type="review"
    ).order_by(
        Forum.created_at.desc()
    ).all()

    return render_template(
        "pages/home.html",
        reviews=reviews
    )


@main.route("/about")
def about():
    return render_template("pages/about.html")


@main.route("/contact")
def contact():
    return render_template("pages/contact.html")