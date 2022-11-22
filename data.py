import os.path
import pickle as p

import utils


def save(storage, question_list: list[utils.Question]):
    for i, q in enumerate(question_list):
        sq = iQuestion()
        sq.set(is_correct=q.is_correct,
               question=q.question_entry.get(),
               answer=q.answer_entry.get(),
               image=q.image_entry.get())
        try:
            storage.iQuestion_list[i] = sq
        except IndexError:
            storage.iQuestion_list.append(sq)
    with open("save.dat", "wb") as f:
        p.dump(storage, f)


def load(storage, app) -> list[utils.Question]:
    if not os.path.exists("save.dat"):
        print("Andmefail puudu!")
        return []
    with open("save.dat", "rb") as f:
        f_storage = p.load(f)
        storage.iQuestion_list = f_storage.iQuestion_list
        questions = []
        for q in f_storage.iQuestion_list:
            fq = utils.Question(app)
            fq.is_correct = q.is_correct
            fq.question_entry.insert(0, q.question)
            fq.answer_entry.insert(0, q.answer)
            fq.image_entry.insert(0, q.image)
            questions.append(fq)
        return questions


class Storage:
    def __init__(self):
        self.iQuestion_list: list = []


class iQuestion:
    def __init__(self):
        self.is_correct = False
        self.question = ""
        self.answer = ""
        self.image = ""

    def set(self, is_correct=None, question=None, answer=None, image=None):
        if is_correct is not None:
            self.is_correct = is_correct
        if question is not None:
            self.question = question
        if answer is not None:
            self.answer = answer
        if image is not None:
            self.image = image
