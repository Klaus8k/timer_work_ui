import tkinter as tk
from datetime import datetime
from tkinter import IntVar, StringVar, ttk
import json


def saver(timers_list: list):
    with open('timers.txt', mode='a') as file:
        str_to_file = ''
        for _ in timers_list:
            str_to_file += f'Задание: {_.text}, время: {_.result_time}\n'

            file.write(str_to_file)


class Window(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.obj_list = []

        self.l1 = ttk.Label(text="Worktack")
        self.l1.grid(
            row=0, column=0, columnspan=5)

        self.ent_text = ttk.Entry(width=50)
        self.ent_text.grid(row=1, column=0, columnspan=5, sticky=('EW'))

        self.btn_start = ttk.Button(
            text="start", command=self.start_timer
        )
        self.btn_start.grid(row=2, column=0, columnspan=2, sticky="EW")

        self.btn_pause = ttk.Button(
            text="pause", command="", state='disable'
        )
        self.btn_pause.grid(row=2, column=2)

        self.btn_stop = ttk.Button(
            text="stop", command=self.stop_timer, state='disable')
        self.btn_stop.grid(row=2, column=3, columnspan=2,  sticky="EW")

        self.current_text = StringVar()
        self.current_text.set("---------")
        self.current_task = ttk.Label(
            textvariable=self.current_text, foreground="red"
        )
        self.current_task.grid(row=3, column=0, columnspan=3)

        self.all_tasks_text = StringVar()
        # self.all_tasks_text.set('---------')
        self.all_tasks = ttk.Label(
            textvariable=self.all_tasks_text)
        self.all_tasks.grid(row=4, column=0, columnspan=4)

        self.counter = StringVar()
        self.counter.set("---")
        self.count_lab = ttk.Label(textvariable=str(self.counter), font='bold')
        self.count_lab.grid(row=3, column=4, columnspan=4)

    def count(self):
        current_time = self.delta_time(self.timer_obj.start)
        self.counter.set(current_time)
        self.timer_obj.result_time = current_time
        self.after(100, self.count)

    @staticmethod
    def delta_time(start):
        delta_time = str(datetime.now() - start)
        return delta_time.split('.')[0]

    def start_timer(self):
        self.timer_obj = Timer()
        self.timer_obj.text = self.ent_text.get()
        self.obj_list.append(self.timer_obj)
        self.current_text.set(
            f"Задание {self.timer_obj.text}, старт: {self.timer_obj.start.strftime('%H:%M')}"
        )
        self.count()
        self.btn_stop.config(state='normal')
        self.btn_pause.config(state='normal')
        self.btn_start.config(state='disable')

    def stop_timer(self):
        self.btn_stop.config(state='disable')
        self.btn_pause.config(state='disable')
        self.btn_start.config(state='normal')
        self.show_all()
        self.count_lab.config(state='disable')
        saver(self.obj_list)

    def show_all(self):
        str_timers = ""
        for i in self.obj_list:
            str_timers += f"{i.text} --- {str(i.result_time)}\n"
        self.all_tasks_text.set(str_timers)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Work timer')
        self.geometry('500x500')
        # self.resizable(False, False)


class Timer:
    def __init__(self):
        self.text = ""
        self.start = datetime.now()


if __name__ == "__main__":
    app = App()
    Window(app)
    app.mainloop()
