from datetime import datetime
from pytz.reference import UTC

from sqlalchemy import Column, Integer, String, DateTime, Text

from app.database import Base

class CollectedDataMixin(object):
    """Mixin of all collected data"""

    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True, nullable=False)
    updated_at = Column(DateTime(), default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime(), nullable=False)

class Task(Base, CollectedDataMixin):
    """Task model"""

    __tablename__ = "task"

    title = Column(String(250), nullable=False)
    description = Column(Text())
    deadline_at = Column(DateTime(), nullable=False)
    finished_at = Column(DateTime())

    def __repr__(self):
        return "<Task %r>" % self.public_id

    def serialize(self, timezone=UTC) -> dict:
        """Serialize the object attributes values into a dictionary.
        Returns:
        dict: a dictionary containing the attributes values
        """

        data = {
            "public_id": self.public_id,
            "title": self.title,
            "description": self.description,
            "deadline_at": self.created_at.astimezone(timezone).isoformat(),
            "finished_at": self.created_at.astimezone(timezone).isoformat(),
            "updated_at": self.created_at.astimezone(timezone).isoformat(),
            "created_at": self.created_at.astimezone(timezone).isoformat(),
        }

        return data    