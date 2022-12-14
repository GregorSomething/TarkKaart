import os.path
import pickle as p
import sys
import time
import tkinter

import utils


def save(storage, question_list: list[utils.Question]):
    storage.iQuestion_list = []
    for i, q in enumerate(question_list):
        sq = iQuestion()
        sq.set(is_correct=q.is_correct_arr,
               question=q.question_entry.get(),
               answer=q.answer_entry.get(),
               image=q.image_entry.get())
        if not q.updated_in_session:
            sq.is_correct.append(q.is_correct)
            q.updated_in_session = True
        else:
            sq.is_correct = sq.is_correct[:-1]
            sq.is_correct.append(q.is_correct)
        storage.iQuestion_list.append(sq)
    with open(storage.datafile, "wb") as f:
        p.dump(storage, f)


def load(storage, app) -> list[utils.Question]:
    if not os.path.exists(storage.datafile):
        print("Andmefail puudu!")
        return []
    with open(storage.datafile, "rb") as f:
        f_storage = p.load(f)
        storage.iQuestion_list = f_storage.iQuestion_list
        questions = []
        storage.iQuestion_list = sorted(storage.iQuestion_list, key=question_sort_value_provider)
        for q in storage.iQuestion_list:
            fq = utils.Question(app)
            fq.is_correct = False
            fq.is_correct_arr = q.is_correct
            fq.question_entry.insert(0, q.question)
            fq.answer_entry.insert(0, q.answer)
            fq.image_entry.insert(0, q.image)
            questions.append(fq)
        return questions


def question_sort_value_provider(q):
    """q - iQuestion"""
    summa = sum(map(lambda bl: 1 if bl else 0, q.is_correct))
    pikkus = len(q.is_correct)
    if pikkus == 0:
        return 0
    return summa / pikkus


def get_data_file_from_user():
    box = tkinter.messagebox.askquestion("TarkKaart | Start", "Ava eksisteeriv andmefail?")
    if box == "no":
        return "./save.dat"
    return tkinter.filedialog.askopenfilename(title="Ava andmefail", initialdir="./",
                                              filetypes=[("Andmefail", "*.dat")])


class Storage:
    def __init__(self, datafile):
        self.iQuestion_list: list = []
        self.datafile = datafile


class iQuestion:
    def __init__(self):
        self.is_correct: list[bool] = []
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
        if self.end_time <= time.time():
            tkinter.messagebox.showinfo(title="TarkKaart | Pomodoro",
                                        message=f"Oled õppinud {self.delay} minutit, võta viie minutine paus, et õppida efektiivsemalt.")
            self.reset()
            self.start()
