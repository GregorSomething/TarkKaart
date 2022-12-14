from PIL import Image, ImageTk
from tkinter import Button, Checkbutton, Frame, Label
from tkinter.messagebox import showerror
from tkinterdnd2.TkinterDnD import Tk

import data
from utils import *


class TarkKaart:
    questions = []

    def add_question(self):
        """Loo küsimus ja uuenda küsimuste listi"""
        question = Question(self)
        self.questions.append(question)
        self.question_scrollframe.update()
        self.question_scrollframe.canvas.yview_moveto(1)

    def add_questions(self, questions):
        self.questions.extend(questions)
        self.question_scrollframe.update()
        self.question_scrollframe.canvas.yview_moveto(1)

    def start_slideshow(self):
        """Tee flash kaartide raam nähtavaks ja kontrolli kas on küsimusi"""
        self.question_index = 0
        # Salvesta küsimused
        data.save(self.storage, self.questions)
        # ----
        self.pomodoro.reset()
        self.pomodoro.start()
        self.slideshow_frame.tkraise()
        if len(self.questions) > 0:
            self.update_slideshow()
            self.toggle_checkbox()
            self.question_button.configure(text=self.questions[0].question_entry.get())

    def update_slideshow(self):
        """Uuenda ekraani järgmise küsimuse informatsiooniga, kui järgmine küsimus eksisteerib"""
        self.question_button.configure(text=self.questions[self.question_index].question_entry.get())
        if self.questions[self.question_index].is_revealed:
            self.answer_label.configure(text=self.questions[self.question_index].answer_entry.get())
            self.draw_image()
        else:
            self.answer_label.configure(text='')
            self.image_label.image = None

    def draw_image(self):
        """Ava pilt ja salvesta"""
        filename = self.questions[self.question_index].image_entry.get()
        if filename != '':
            try:
                open_image = Image.open(filename)
                open_image = open_image.resize(
                    (self.answer_label.winfo_width() - 5, self.answer_label.winfo_height() - 5))
                image_file = ImageTk.PhotoImage(open_image)
                self.image_label.image = image_file
                self.image_label.configure(image=image_file, height=open_image.height, width=open_image.width)
            except FileNotFoundError:
                showerror('Invalid File Path',
                          'The file path for this image is invalid. Please choose a valid file path.')

    def reveal_answer(self):
        """Näita flash kaardi vastust"""
        if len(self.questions) > 0:
            if self.questions[self.question_index].is_revealed:
                self.questions[self.question_index].is_revealed = False
                self.update_slideshow()
            else:
                self.questions[self.question_index].is_revealed = True
                self.answer_label.configure(text=self.questions[self.question_index].answer_entry.get())
                self.draw_image()

    def previous_question(self):
        """Eelmine küsimus"""
        self.pomodoro.check()
        if self.question_index > 0:
            self.question_index -= 1
            self.update_slideshow()
            self.toggle_checkbox()
        # Salvesta küsimused
        data.save(self.storage, self.questions)
        # ----

    def next_question(self):
        """Järgmine küsimus"""
        self.pomodoro.check()
        if self.question_index + 1 < len(self.questions):
            self.question_index += 1
            self.update_slideshow()
            self.toggle_checkbox()
        # Salvesta küsimused
        data.save(self.storage, self.questions)
        # ----

    def mark_question(self):
        """Kas vastasid õieti või valesti checkbox"""
        if len(self.questions) > 0:
            self.questions[self.question_index].is_correct = not self.questions[self.question_index].is_correct

    def toggle_checkbox(self):
        """Jäta meelde kas vastati õieti või valesti"""
        if self.questions[self.question_index].is_correct:
            self.checkbox.select()
        else:
            self.checkbox.deselect()

    def run(self):
        """Widgetid ja main loop."""
        self.root = Tk()
        self.root.title('TarkKaart')
        self.root.geometry('1920x1080')

        # Frame
        self.container = Frame(self.root, bg=FRAME_BG)
        self.home_frame = Frame(self.container, bg=FRAME_BG)
        self.edit_frame = Frame(self.container, bg=FRAME_BG)
        self.button_frame = Frame(self.edit_frame, bg=FRAME_BG)
        self.question_frame = Frame(self.edit_frame, bg=FRAME_BG)
        self.slideshow_frame = Frame(self.container, bg=FRAME_BG)
        self.left_frame = Frame(self.slideshow_frame, bg=FRAME_BG)
        self.mid_frame = Frame(self.slideshow_frame, bg=FRAME_BG)
        self.right_frame = Frame(self.slideshow_frame, bg=FRAME_BG)
        self.answer_frame = Frame(self.mid_frame, bg=FRAME_BG)

        # Labels
        self.title_label = Label(self.home_frame, bg=FRAME_BG, font=HEADER_FONT, text='TarkKaart')
        self.edit_label = Label(self.edit_frame, bg=FRAME_BG, font=HEADER_FONT, text='Andmed')
        self.answer_label = Label(self.answer_frame, bg=FRAME_BG, font=LARGE_FONT, wraplength=650, height=7, width=20)
        self.image_label = Label(self.answer_frame, bg=FRAME_BG)

        # Buttons
        self.title_slideshow_button = Button(self.home_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                             bd=2, relief='solid', font=LARGE_FONT, text='Alusta',
                                             command=self.start_slideshow, width=15)
        self.edit_button = Button(self.home_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG, bd=2,
                                  relief='solid', font=LARGE_FONT, text='Sisesta andmed',
                                  command=self.edit_frame.tkraise, width=15)
        self.settings_button = Button(self.home_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG, bd=2,
                                      relief='solid', font=LARGE_FONT, text='Sätted', width=15)
        self.home_button_1 = Button(self.edit_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                    font=SMALL_FONT, text='<< Tagasi', command=self.home_frame.tkraise)
        self.home_button_2 = Button(self.slideshow_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                    font=SMALL_FONT, text='<< Tagasi', command=self.home_frame.tkraise)
        self.edit_add_button = Button(self.button_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                      font=SMALL_FONT, text='+ Lisa küsimus', command=self.add_question)
        self.edit_slideshow_button = Button(self.button_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                            font=SMALL_FONT, text='Alusta', command=self.start_slideshow)
        self.question_button = Button(self.mid_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                      font=LARGE_FONT, wraplength=1500, command=self.reveal_answer)
        self.previous_button = Button(self.left_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                      font=SMALL_FONT, text='<< Eelmine', command=self.previous_question)
        self.next_button = Button(self.right_frame, activebackground=ACTIVE_BG, activeforeground=ACTIVE_FG,
                                  font=SMALL_FONT, text='Järgmine >>', command=self.next_question)

        # Checkbutton
        self.checkbox = Checkbutton(self.mid_frame, activebackground=FRAME_BG, bg=FRAME_BG, font=SMALL_FONT,
                                    text='Vastasid õieti?', command=self.mark_question)

        # Widgetid ekraanile
        self.container.pack(expand=True, fill='both')
        self.home_frame.grid(row=0, column=0, sticky='nsew')
        self.title_label.grid(row=0, column=0, pady=25, sticky='nsew')
        self.title_slideshow_button.grid(row=1, column=0, pady=10)
        self.edit_button.grid(row=2, column=0, pady=10)
        self.settings_button.grid(row=5, column=0, pady=10)
        self.edit_frame.grid(row=0, column=0, sticky='nsew')
        self.slideshow_frame.grid(row=0, column=0, sticky='nsew')
        self.home_button_1.place(relx=0.01, rely=0.01)
        self.home_button_2.place(relx=0.01, rely=0.01)
        self.edit_label.pack(anchor='c', pady=25)
        self.button_frame.pack()
        self.question_frame.pack(expand=True, fill='both', pady=5)
        self.edit_add_button.pack(side='left', anchor='c', padx=5, pady=5)
        self.edit_slideshow_button.pack(side='left', anchor='c', padx=5, pady=5)
        self.question_scrollframe = ScrollFrame(self.question_frame)
        self.question_button.pack(side='top', anchor='n', expand=True, fill='both', padx=10, pady=5)
        self.left_frame.pack(side='left', padx=5)
        self.mid_frame.pack(side='left', expand=True, fill='both', padx=5, pady=50)
        self.answer_frame.pack(pady=50)
        self.right_frame.pack(side='left', padx=5)
        self.previous_button.pack()
        self.next_button.pack()
        self.answer_label.pack(side='left', anchor='c', padx=20, pady=5, expand=True, fill='both')
        self.image_label.pack(side='right', anchor='c', padx=20, pady=5, expand=True, fill='both')
        self.checkbox.pack(side='top', anchor='c')

        # Widgetid centered
        self.container.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.edit_frame.grid_columnconfigure(0, weight=1)
        self.slideshow_frame.grid_columnconfigure(0, weight=1)

        # Andme asjad
        self.storage = data.Storage()
        self.add_questions(data.load(self.storage, self))

        # Pomodoro, arg1 on aeg mille tagant sõnum tuleb
        self.pomodoro = data.Pomodoro(20)

        # Põhiraam nähtavale ja mainloop
        self.home_frame.tkraise()
        self.root.mainloop()


if __name__ == '__main__':
    app = TarkKaart()
    app.run()
