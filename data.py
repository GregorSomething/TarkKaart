import os.path
import pickle as p
import sys
import time
import tkinter

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


class Pomodoro:

    def __init__(self, delay: int):
        self.start_time = int(time.time() // 1)
        self.end_time = self.start_time + delay * 60
        self.delay = delay

    def reset(self):
        self.start_time = int(time.time() // 1)
        self.end_time = sys.maxsize

    def start(self):
        self.reset()
        self.end_time = self.start_time + self.delay * 60

    def check(self):
        print("aa", self.start_time, self.end_time, time.time())
        if self.end_time <= time.time():
            tkinter.messagebox.showinfo(title="TarkKaart | Pomodoro",
                                        message=f"Oled õppinud {self.delay} minutit, võta viie minutine paus, et õppida efektiivsemalt.")
            self.reset()
            self.start()
