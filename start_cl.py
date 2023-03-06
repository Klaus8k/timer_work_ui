import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from datetime import datetime


class Window(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('timer for work')
        self.geometry('500x300')
        self.obj_list = []

        self.l1 = ttk.Label(self, text='about worktack').grid()
        self.subscribe = ttk.Entry(self)
        self.subscribe.grid()

        self.button_start = ttk.Button(self, text='start',
                             command=self.start_timer).grid()

        self.button_pause = ttk.Button(self, text='pause',
                             command='', default='disable').grid()
        
        self.button_stop = ttk.Button(self, text='stop', command=self.stop_timer).grid()

        self.current_text = StringVar()
        self.current_text.set('---------')
        self.current_task = ttk.Label(self, textvariable=self.current_text, foreground='red')
        self.current_task.grid()

        self.all_tasks_text = StringVar()
        # self.all_tasks_text.set('---------')
        self.all_tasks = ttk.Label(self, textvariable=self.all_tasks_text).grid()

    def start_timer(self):
        self.timer_obj = Timer()
        self.timer_obj.text = self.subscribe.get()
        self.obj_list.append(self.timer_obj)
        self.current_text.set(f"{self.timer_obj.text} - {self.timer_obj.start.strftime('%H:%M:%S')}")


    def stop_timer(self):
        self.timer_obj.stop = datetime.now()
        self.timer_obj.result_time = self.timer_obj.stop - self.timer_obj.start
        self.show_all()

    def show_all(self):
        str_timers = ''
        for i in self.obj_list:
            str_timers += f"{i.text} --- {str(i.result_time)}\n"
        self.all_tasks_text.set(str_timers)


class Timer():
    def __init__(self):
        self.text = ''
        self.start = datetime.now()



if __name__ == '__main__':
    root = Window()
    root.mainloop()
