from tkinter import Button, Canvas, Entry, Frame, Label, Scrollbar
from tkinter.filedialog import askopenfilename
from tkinterdnd2 import DND_FILES


# Värvid, fondid
FRAME_BG = 'lightgrey'
ACTIVE_BG = 'black'
ACTIVE_FG = 'white'
HEADER_FONT = 'Calibri', 64, 'bold', 'underline'
LARGE_FONT = 'Calibri', 48
SMALL_FONT = 'Calibri', 24
SMALL_FONT_BOLD = 'Calibri', 24, 'bold'


def drop_file(event, entry):
        """
        Drag and drop

        event : Tkinter Event object that provides a file path string
        entry : Tkinter Entry object in which to insert the file path string
        """
        entry.delete(0, 'end')
        entry.insert(0, event.data)


class Question:
    def __init__(self, gui):
        """
        Widgetid mis tuleb luua kui andmeid sisestatakse

        """
        # Jätame meelde kas küsimusele vastata õieti
        self.is_correct = False
        self.is_revealed = False

        # Defineerime parent scrollframe'i ja raami borderi
        self.gui = gui
        self.scrollframe = gui.question_scrollframe
        self.frame = Frame(self.scrollframe, bd='1', relief='solid')

        # Labels
        self.question_label = Label(self.frame, font=SMALL_FONT, text='Küsimus:')
        self.answer_label = Label(self.frame, font=SMALL_FONT, text='Vastus:')
        self.image_label = Label(self.frame, font=SMALL_FONT, text='Pilt:')

        # Entries
        self.question_entry = Entry(self.frame, font=SMALL_FONT)
        self.answer_entry = Entry(self.frame, font=SMALL_FONT)
        self.image_entry = Entry(self.frame, font=SMALL_FONT)
        
        # Nupud
        self.choose_button = Button(self.frame, bd=3, font=SMALL_FONT, text='Vali pilt...', command=self.select_image)
        self.remove_button = Button(self.frame, bd=3, font=SMALL_FONT_BOLD, text='X', command=self.remove, width=4)

        # Widgetid ekraanile
        self.frame.pack(side='top', fill='x')
        self.question_label.pack(side='left', padx=5)
        self.question_entry.pack(side='left', padx=5)
        self.answer_label.pack(side='left', padx=5)
        self.answer_entry.pack(side='left', padx=5)
        self.image_label.pack(side='left', padx=5)
        self.image_entry.pack(side='left', padx=5)
        self.choose_button.pack(side='left', padx=5)
        self.remove_button.pack(side='left', padx=5)

        # Drag ja drop failidele
        self.image_entry.drop_target_register(DND_FILES)
        self.image_entry.dnd_bind('<<Drop>>', lambda event: drop_file(event, self.image_entry))
    
    
    def select_image(self):
        #"Vali pilt" nupu funktsioon

        filename = askopenfilename(filetypes=[('PNG Files', '*.png'), ('JPG Files', '*.jpg')])
        if filename != '':
            self.image_entry.delete(0, 'end')
            self.image_entry.insert(0, filename)
            self.image_entry.xview_moveto(1)


    def remove(self):
        #Küsimuse eemaldamise (X) nupp.

        self.frame.destroy()
        self.scrollframe.update()
        self.gui.questions.remove(self)


class ScrollFrame(Frame):
    def __init__(self, frame):
        #Skrollitav frame widget
        self.scrollbar = Scrollbar(frame, width=24, bg=FRAME_BG)
        self.scrollbar.pack(side='right', fill='y', expand=False)

        self.canvas = Canvas(frame, yscrollcommand=self.scrollbar.set, bg=FRAME_BG)
        self.canvas.pack(side='bottom', fill='both', expand=True, padx=5, pady=5)

        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.bind('<Configure>', self.fill_canvas)
        self.canvas.bind('<Destroy>', lambda _: self.canvas.unbind_all('<MouseWheel>'))
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        
        Frame.__init__(self, frame, bd=2, relief='solid', bg=FRAME_BG)
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor='nw')


    def on_mousewheel(self, event):
        """
        Hiirenupuga saab skrollida

        event : Tkinter MouseWheel event
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')


    def fill_canvas(self, event):
        """
        Kohanda canvas laiust

        event : Tkinter Configure event
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)


    def update(self):
        self.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(self.windows_item))
