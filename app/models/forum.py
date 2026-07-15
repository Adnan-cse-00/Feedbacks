from datetime import datetime
from app import db

class Forum(db.Model):
    __tablename__ = "forums"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    forum_type = db.Column(db.String(20), nullable=False)   # review or question

    title = db.Column(db.String(255), nullable=False)

    content = db.Column(db.Text, nullable=False)

    rating = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    comments = db.relationship(
    "Comment",
    backref="forum",
    lazy=True,
    cascade="all, delete-orphan"
    )