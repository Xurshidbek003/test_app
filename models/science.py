from sqlalchemy import Column, Integer, String
from db import Base


class Sciences(Base):
    __tablename__ = "sciences"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
