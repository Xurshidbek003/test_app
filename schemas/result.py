from pydantic import BaseModel, Field


class AddResult(BaseModel):
    question_id: int = Field(..., gt=0)
    answer_id: int = Field(..., gt=0)
