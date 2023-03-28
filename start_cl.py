import tkinter as tk
from datetime import datetime
from tkinter import IntVar, StringVar, ttk


class Window(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # self.title("timer for work")
        # self.geometry("500x300")
        self.obj_list = []

        self.l1 = ttk.Label(text="about worktack").grid(row=0, column=0)

        self.text = ttk.Entry()
        self.text.grid(row=1, column=0)

        self.button_start = ttk.Button(
            text="start", command=self.start_timer
        ).grid(row=2, column=0)

        self.button_pause = ttk.Button(
            text="pause", command="", default="disable"
        ).grid(row=2,column=1)

        self.button_stop = ttk.Button(
            text="stop", command=self.stop_timer)
        self.button_stop.grid(row=2,column=2)

        self.current_text = StringVar()
        self.current_text.set("---------")
        self.current_task = ttk.Label(
            self, textvariable=self.current_text, foreground="red"
        )
        self.current_task.grid()

        self.all_tasks_text = StringVar()
        # self.all_tasks_text.set('---------')
        self.all_tasks = ttk.Label(
            self, textvariable=self.all_tasks_text).grid()

        self.a = 0
        self.counter = StringVar()
        self.counter.set("-------------------")
        self.count_lab = ttk.Label(self, textvariable=str(self.counter)).grid()

    def count(self):
        self.counter.set(self.delta_time(self.timer_obj.start))
        self.after(1000, self.count)

    @staticmethod
    def delta_time(start):
        delta_time = datetime.now() - start
        return delta_time

    def start_timer(self):
        self.timer_obj = Timer()
        self.timer_obj.text = self.text.get()
        self.obj_list.append(self.timer_obj)
        self.current_text.set(
            f"Задание {self.timer_obj.text}, старт: {self.timer_obj.start.strftime('%H:%M')}"
        )
        self.count()
        self.button_stop.config(state='disable')
        print(self.button_stop)

    def stop_timer(self):
        self.timer_obj.result_time = self.delta_time(self.timer_obj.start)
        self.show_all()

    def show_all(self):
        str_timers = ""
        for i in self.obj_list:
            str_timers += f"{i.text} --- {str(i.result_time)}\n"
        self.all_tasks_text.set(str_timers)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Temperature Converter')
        self.geometry('300x70')
        self.resizable(False, False)


class Timer:
    def __init__(self):
        self.text = ""
        self.start = datetime.now()


if __name__ == "__main__":
    app = App()
    Window(app)
    app.mainloop()
