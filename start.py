import json
import tkinter as tk
from datetime import datetime
from tkinter import IntVar, StringVar, ttk


def saver(timers_list: list):
    with open('timers.txt', mode='a') as file:
        str_to_file = ''
        for _ in timers_list:
            str_to_file += f'Задание: {_.text}, время: {_.result_time}\n'
            file.write(str_to_file)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Work timer')
        self.geometry('420x400')
        # self.resizable(False, False)

class Window(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.timer_obj = None
        self.obj_list = []

        self.lbl_head = ttk.Label(text="Задача:")
        self.lbl_head.grid(
            row=0, column=0, columnspan=5)

        self.ent_task_text = ttk.Entry(width=50)
        self.ent_task_text.grid(row=1, column=0, columnspan=5, sticky=('EW'))

        self.btn_start = ttk.Button(text="start", command=self.start_timer)
        self.btn_start.grid(row=2, column=0, columnspan=2, sticky="EW")

        self.btn_pause = ttk.Button(text="pause", command=self.pause, state='disable')
        self.btn_pause.grid(row=2, column=2)

        self.btn_stop = ttk.Button(text="stop", command=self.stop_timer, state='disable')
        self.btn_stop.grid(row=2, column=3, columnspan=2,  sticky="EW")

        self.current_task_text = StringVar()
        self.current_task_text.set("---")
        self.lbl_current_task = ttk.Label(textvariable=self.current_task_text, foreground="red")
        self.lbl_current_task.grid(row=3, column=0, columnspan=3)

        self.all_tasks = StringVar()
        self.all_tasks.set('---')
        self.lbl_all_tasks = ttk.Label(textvariable=self.all_tasks)
        self.lbl_all_tasks.grid(row=4, column=0, columnspan=4)


        self.counter = StringVar()
        self.counter.set("---")
        self.lbl_counter = ttk.Label(textvariable=self.counter, font='bold')
        self.lbl_counter.grid(row=3, column=4, columnspan=4)

    def switch_button(self):
        if self.timer_obj:
            self.btn_stop.config(state='normal')
            self.btn_pause.config(state='normal')
            self.btn_start.config(state='disable')
        else:
            self.btn_stop.config(state='disable')
            self.btn_pause.config(state='disable')
            self.btn_start.config(state='normal')


    def start_timer(self):
        if self.timer_obj == None:
            self.timer_obj = Timer()
            self.timer_obj.text = [self.ent_task_text.get(), self.timer_obj.start_end_list[0]]
            self.obj_list.append(self.timer_obj)
            self.switch_button()
            self.current_task_text.set(self.timer_obj.text)
            self.count()
        else:
            self.timer_obj.start_end_list.append(datetime.now())

        

    def pause(self):

        if self.timer_obj.is_paused:
            self.timer_obj.switch_pause()
            self.start_timer()

        else:
            self.timer_obj.switch_pause()
            self.stop()
            self.btn_start.config(state='normal')


    def stop(self):

        self.timer_obj.start_end_list.append(datetime.now())
        self.count()

    def stop_timer(self):
        if not self.timer_obj.is_paused:
            self.timer_obj.start_end_list.append(datetime.now())
        self.timer_obj.result = self.timer_obj.result_time()
        self.counter.set(self.timer_obj.result_time())
        self.show_all()
        self.timer_obj = None
        self.switch_button()

    def show_all(self):
        str_timers = ""
        for i in self.obj_list:
            str_timers += f"{i.text} --- {str(i.result)}\n"
        self.all_tasks.set(str_timers)

    def count(self):
        
        if (len(self.timer_obj.start_end_list) % 2) == 0: # На паузе или закончился таймер
            self.counter.set(self.timer_obj.result_time())
            self.after(1000, self.count)

        else: # Таймер в работе
            self.timer_obj.start_end_list.append(datetime.now()) # Добавляется а потом удаляется текущее время
            time = self.timer_obj.result_time()
            self.timer_obj.start_end_list.pop()
            self.counter.set(time)
            self.after(1000, self.count)



class Timer:
    def __init__(self, text='t:'):
        self.text = text
        # self.start_time = datetime.now()
        self.start_end_list = [datetime.now(),]
        self.is_paused = False
        # self.result = datetime.now() - datetime.now()

    def switch_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

    def result_time(self):
        
        result = datetime.now() - datetime.now() # AAAAA, нулевой дельтатайм
        for i in range(0, len(self.start_end_list), 2):
            result += self.start_end_list[i+1] - self.start_end_list[i]
        return str(result).split('.')[0]



if __name__ == "__main__":
    app = App()
    Window(app)
    app.mainloop()
