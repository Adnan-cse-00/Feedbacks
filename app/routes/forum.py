from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models.forum import Forum

forum = Blueprint("forum", __name__)


@forum.route("/create-review", methods=["GET", "POST"])
@login_required
def create_review():

    if request.method == "POST":

        title = request.form["title"]
        rating = int(request.form["rating"])
        content = request.form["content"]

        review = Forum(
            user_id=current_user.id,
            forum_type="review",
            title=title,
            content=content,
            rating=rating
        )

        db.session.add(review)
        db.session.commit()

        return redirect(url_for("main.home"))

    return render_template("pages/create_review.html")

@forum.route("/review/<int:review_id>")
def review_details(review_id):

    review = Forum.query.get_or_404(review_id)

    return render_template(
        "pages/review_details.html",
        review=review
    )