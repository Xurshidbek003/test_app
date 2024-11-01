from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from db import Base
from models.science import Sciences


class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    science_id = Column(Integer, nullable=False)

    science = relationship("Sciences", foreign_keys=[science_id],
                           primaryjoin=lambda: Sciences.id == Questions.science_id)
