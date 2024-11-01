from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, load_only

from db import database
from functions.create_test import create_result_f
from functions.db_operations import save_in_db, get_in_db
from models.answer import Answers
from models.question import Questions
from models.science import Sciences
from schemas.result import AddResult
from typing import List

tests_router = APIRouter(
    prefix="/test",
    tags=["Test operatsiyalari"]
)


@tests_router.post('/add_science')
def create(science_name: str, db: Session = Depends(database)):
    new_item = Sciences(
        name=science_name
    )
    save_in_db(db, new_item)
    raise HTTPException(200, 'success')


@tests_router.get('/get_science')
def get(db: Session = Depends(database)):
    return db.query(Sciences).all()


@tests_router.get('/get_tests')
async def get_test_f(science_id: int, db: Session = Depends(database)):
    await get_in_db(db, Sciences, science_id)
    questions = (db.query(Questions).options(load_only(Questions.text))
                 .filter(Questions.science_id == science_id).all())
    result1 = []
    for question in questions:
        answers = db.query(Answers).filter(Answers.question_id == question.id).all()
        result1.append({
            "question": question,
            "answers": [answer for answer in answers]
        })

    return {"data": result1}


@tests_router.post('/upload_test/{science_id}')
async def upload_txt(science_id: int, file: UploadFile = File(...), db: Session = Depends(database)):
    item = await create_result_f(db, science_id, file)
    return item


@tests_router.post('/add_result')
def result(forms: List[AddResult], db: Session = Depends(database)):
    total = 0
    common = 0

    for form in forms:
        get_in_db(db, Questions, form.question_id)
        get_in_db(db, Answers, form.answer_id)
        answer = db.query(Answers).filter(Answers.id == form.answer_id).first()
        total += 1
        if answer.status:
            common += 1
    return {"jami savollar soni": total,
            "to`g`ri javoblar soni": common}
