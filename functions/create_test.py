from fastapi import HTTPException

from functions.db_operations import save_in_db, get_in_db
from models.answer import Answers
from models.question import Questions
from models.science import Sciences


async def create_result_f(db, science_id, file):
    await get_in_db(db, Sciences, science_id)
    content = await file.read()
    content_str = content.decode("utf-8-sig")

    questions_data = content_str.strip().split("+++++")
    created_questions = []

    for question_data in questions_data:
        lines = question_data.strip().split("====")
        if len(lines) < 2:
            continue

        question_text = lines[0].strip()
        options = []
        correct_option_index = None

        for idx, line in enumerate(lines[1:], start=0):
            line = line.strip()
            if line.startswith("#"):
                option_text = line[1:].strip()
                correct_option_index = idx
            else:
                option_text = line
            options.append(option_text)

        if correct_option_index is None:
            raise HTTPException(status_code=400, detail=f"No correct option found for question: "
                                                        f"{question_text}")

        db_question = Questions(text=question_text, science_id=science_id)
        save_in_db(db, db_question)

        db_options = []
        for idx, option_text in enumerate(options):
            is_correct = (idx == correct_option_index)
            db_option = Answers(text=option_text, status=is_correct, question_id=db_question.id)
            save_in_db(db, db_option)
            db_options.append(db_option)

        created_questions.append({
            "id": db_question.id,
            "question_text": db_question.text,
            "options": [{"id": opt.id, "text": opt.text, "is_correct": opt.status} for opt in db_options]
        })

    return created_questions
