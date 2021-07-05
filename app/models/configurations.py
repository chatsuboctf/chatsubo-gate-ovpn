from datetime import datetime, timedelta

from flask import current_app
from sqlalchemy import func

import app.context


class Configurations(app.context.db.Model):
    __tablename__ = "configurations"

    id = app.context.db.Column(
        app.context.db.String(36),
        primary_key=True,
    )

    username = app.context.db.Column(
        app.context.db.Text,
        nullable=False,
        unique=True
    )

    config = app.context.db.Column(
        app.context.db.Text,
        nullable=False,
        unique=True
    )

    created_at = app.context.db.Column(
        app.context.db.DateTime,
        index=False,
        server_default=func.now()
    )

    def is_expired(self):
        now = datetime.now()
        if now - timedelta(minutes=current_app.config.get("expiration", 0)) <= self.created_at <= now:
            # within "access_expiration" timeframe
            return False

        return True

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "config": self.config,
            "downloaded_at": self.downloaded_at,
        }

    def __repr__(self):
        return f"<Configurations ({self.username})>"

