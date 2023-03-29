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
        self.timer_obj = None
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

        self.btn_pause = ttk.Button(text="pause", command=self.pause)
        self.btn_pause.grid(row=2, column=2)

        self.btn_stop = ttk.Button(
            text="stop", command=self.stop_timer)
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
        print(self.timer_obj.start_end_list, self.timer_obj.is_paused)
        if (len(self.timer_obj.start_end_list) % 2) != 0:
            time = self.delta_time(self.timer_obj.start_end_list[-1]) + #Предыдущее время, которое уже прошло
            self.counter.set(time)
            self.after(1000, self.count)
        else:
            self.counter.set(self.timer_obj.result_time())


    @staticmethod
    def delta_time(start):
        delta_time = datetime.now() - start
        return delta_time

    def start_timer(self):
        if self.timer_obj == None:
            self.timer_obj = Timer()
            self.timer_obj.text = self.ent_text.get()
            self.obj_list.append(self.timer_obj)
            self.current_text.set(f'{self.timer_obj.text}, {self.timer_obj.start_time}')
            self.count()
        else:
            self.timer_obj.start_end_list.append(datetime.now())
            self.count()


    def pause(self):
        if self.timer_obj.is_paused:
            self.timer_obj.switch_pause()
            self.start_timer()

        else:
            self.timer_obj.switch_pause()
            self.stop()

    #     self.btn_stop.config(state='normal')
    #     self.btn_pause.config(state='normal')
    #     self.btn_start.config(state='disable')

    def stop(self):
        self.timer_obj.start_end_list.append(datetime.now())

    def stop_timer(self):

        self.stop()
        self.timer_obj.result = self.timer_obj.result_time()
        self.show_all()
        self.timer_obj = None
            

        # self.count_lab.config(state='disable')

    def show_all(self):
        str_timers = ""
        for i in self.obj_list:
            str_timers += f"{i.text} --- {str(i.result)}\n"
        self.all_tasks_text.set(str_timers)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Work timer')
        self.geometry('420x400')
        # self.resizable(False, False)


class Timer:
    def __init__(self, text='t:'):
        self.text = text
        self.start_time = datetime.now()
        self.start_end_list = [self.start_time,]
        self.is_paused = False

    def switch_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

    def result_time(self):
        
        result = datetime.now() - datetime.now()
        # Проверка на четность и количество записей о времени старта и конца
        for i in range(0, len(self.start_end_list), 2):
            result += self.start_end_list[i+1] - self.start_end_list[i]
        return result



if __name__ == "__main__":
    # a = Timer()
    # a.start_end_list = [1,3,5,9,0,5]
    # print(a.start_end_list)
    # print(a.result_time())


    app = App()
    Window(app)
    app.mainloop()
