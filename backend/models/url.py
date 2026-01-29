from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database.base import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    clicks = Column(Integer, default=0)
    created_ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    