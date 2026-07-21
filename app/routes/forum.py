from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models.forum import Forum
from app.models.comment import Comment

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


@forum.route("/create-question", methods=["GET", "POST"])
@login_required
def create_question():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        question = Forum(
            user_id=current_user.id,
            forum_type="question",
            title=title,
            content=content,
            rating=None
        )

        db.session.add(question)
        db.session.commit()

        return redirect(url_for("main.home"))

    return render_template("pages/create_question.html")



@forum.route("/review/<int:review_id>", methods=["GET", "POST"])
def review_details(review_id):

    review = Forum.query.get_or_404(review_id)

    if request.method == "POST":

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        content = request.form["content"]

        comment = Comment(
            forum_id=review.id,
            user_id=current_user.id,
            content=content
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for("forum.review_details", review_id=review.id))

    comments = Comment.query.filter_by(
        forum_id=review.id
    ).order_by(
        Comment.created_at.asc()
    ).all()

    return render_template(
        "pages/review_details.html",
        review=review,
        comments=comments
    )


@forum.route("/question/<int:question_id>", methods=["GET", "POST"])
def question_details(question_id):

    question = Forum.query.get_or_404(question_id)

    if question.forum_type != "question":
        return "Question not found", 404

    if request.method == "POST":

        if not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

        content = request.form["content"]

        comment = Comment(
            forum_id=question.id,
            user_id=current_user.id,
            content=content
        )

        db.session.add(comment)
        db.session.commit()

        return redirect(
            url_for(
                "forum.question_details",
                question_id=question.id
            )
        )

    comments = Comment.query.filter_by(
        forum_id=question.id
    ).order_by(
        Comment.created_at.asc()
    ).all()

    return render_template(
        "pages/question_details.html",
        question=question,
        comments=comments
    )


@forum.route("/question/<int:question_id>/edit", methods=["GET", "POST"])
@login_required
def edit_question(question_id):

    question = Forum.query.get_or_404(question_id)

    if question.user_id != current_user.id:
        return "Unauthorized", 403

    if question.forum_type != "question":
        return "Question not found", 404

    if request.method == "POST":

        question.title = request.form["title"]
        question.content = request.form["content"]

        db.session.commit()

        return redirect(
            url_for(
                "forum.question_details",
                question_id=question.id
            )
        )

    return render_template(
        "pages/edit_question.html",
        question=question
    )


@forum.route("/question/<int:question_id>/delete", methods=["POST"])
@login_required
def delete_question(question_id):

    question = Forum.query.get_or_404(question_id)

    if question.user_id != current_user.id:
        return "Unauthorized", 403

    if question.forum_type != "question":
        return "Question not found", 404

    db.session.delete(question)
    db.session.commit()

    return redirect(url_for("main.home"))


@forum.route("/review/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):

    review = Forum.query.get_or_404(review_id)

    # Only the author can delete
    if review.user_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(review)
    db.session.commit()

    return redirect(url_for("main.home"))

@forum.route("/review/<int:review_id>/edit", methods=["GET", "POST"])
@login_required
def edit_review(review_id):

    review = Forum.query.get_or_404(review_id)

    # Only the author can edit
    if review.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == "POST":

        review.title = request.form["title"]
        review.rating = int(request.form["rating"])
        review.content = request.form["content"]

        db.session.commit()

        return redirect(
            url_for(
                "forum.review_details",
                review_id=review.id
            )
        )

    return render_template(
        "pages/edit_review.html",
        review=review
    )