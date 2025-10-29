from datetime import datetime, timezone

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
    __tablename__ = "revoked_token"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), unique=True, nullable=False)
    # Use timezone-aware UTC timestamps to avoid DeprecationWarning and
    # to be explicit about timezone handling across environments.
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
