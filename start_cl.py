import tkinter as tk
from tkinter import ttk


class Window(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('name')
        self.geometry('500x300')
        self.obj_list = []

        self.l1 = ttk.Label(self, text='text l1')
        self.l1.grid(column=0,row=0)

        self.b1 = ttk.Button(self, text='b1 test', command=self.obj_start)
        self.b1.grid()

        self.b2 = ttk.Button(self, text='object * 4', command=self.check)
        self.b2.grid()

        self.e1 = ttk.Entry(self)
        self.e1.grid()

    def obj_start(self):
        a = Timer()
        self.obj_list.append(a)

    def check(self):
        self.l1['text'] = self.obj_list


class Timer():
    def __init__(self):
        self.info = {}
        self.check_num = 5











if __name__ == '__main__':
    root = Window()
    root.mainloop()
