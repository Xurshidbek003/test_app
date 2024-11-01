from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean
from db import Base
from models.question import Questions


class Answers(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False)
    question_id = Column(Integer, nullable=False)

    question = relationship("Questions", foreign_keys=[question_id],
                            primaryjoin=lambda: Questions.id == Answers.question_id)
