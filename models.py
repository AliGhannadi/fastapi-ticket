from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
class Tickets(Base):
    __tablename__ = 'Tickets'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    