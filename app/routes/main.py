from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("pages/home.html")


@main.route("/about")
def about():
    return render_template("pages/about.html")


@main.route("/contact")
def contact():
    return render_template("pages/contact.html")