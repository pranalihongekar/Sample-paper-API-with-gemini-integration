from pydantic import BaseModel
from typing import List, Dict

class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: str
    params: Dict[str, str] = {}

class Section(BaseModel):
    marks_per_question: int
    type: str
    questions: List[Question]

class PaperParams(BaseModel):
    board: str
    grade: int
    subject: str

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: PaperParams
    tags: List[str]
    chapters: List[str]
    sections: List[Section]
