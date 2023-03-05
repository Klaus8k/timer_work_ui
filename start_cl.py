import tkinter as tk
from tkinter import ttk
from tkinter import StringVar


class Window(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('name')
        self.geometry('500x300')
        self.obj_list = []

        self.e1 = ttk.Entry(self)
        self.e1.grid()

        self.b1 = ttk.Button(self, text='write e1 to lst',
                             command=self.writ_e1).grid()

        self.b2 = ttk.Button(self, text='all objs',
                             command=self.all_obj).grid()

        self.l1_text = StringVar()
        self.l1_text.set('---------')
        self.l1 = ttk.Label(self, textvariable=self.l1_text)
        self.l1.grid()

    def writ_e1(self):
        a = Timer()
        a.text = self.e1.get()
        self.obj_list.append(a)
        self.l1_text.set(a.text)

    def all_obj(self):

        b = ''
        for _ in self.obj_list: b += _.text + '\n'
        print(b)
        self.l1_text.set(b)


class Timer():
    def __init__(self):
        self.info = {}
        self.text = ''


if __name__ == '__main__':
    root = Window()
    root.mainloop()
