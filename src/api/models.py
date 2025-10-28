import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


"""Database models for the application.

Contains the User model and the RevokedToken model used for JWT revocation.
"""


class User(db.Model):
    """A user account."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)

    def serialize(self):
        """Return a JSON-serializable representation (without password)."""
        return {"id": self.id, "email": self.email}


class RevokedToken(db.Model):
    """A revoked JWT identifier (jti) stored to invalidate tokens on logout."""

    __tablename__ = "revoked_token"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow
    )
