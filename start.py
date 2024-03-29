import json
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import IntVar, StringVar

# from loguru import logger

# logger.debug('loguru logger')
# import sys

# logger.add(sys.stderr, format="{time} {level} {message}")

HISTORY = 'timers.json'

def saver(timer: object):
    file = open(HISTORY, mode='r')
    try:
        timers = json.load(file)
        file.close()
    except json.JSONDecodeError:
        timers = []

    timers.append(
        {
        'date': timer.start_end_list[0].strftime('%d/%m/%Y'),
        'task': timer.text,
        'start_time': timer.start_end_list[0].strftime('%H:%M:%S'),
        'result': timer.result,
        })
    file = open(HISTORY, mode='w')
    json.dump(timers, file, indent=4)            
    file.close()

def read_history():
    with open(HISTORY, mode='r') as file:
        old_timers = ''
        try:
            file_date = json.load(file)
        except json.decoder.JSONDecodeError:
            return ''
        rev_file_date = sorted(file_date, key=lambda x: x['start_time'], reverse=True)
        for i in rev_file_date:
            if i['date'] == datetime.today().strftime('%d/%m/%Y'):
                task = '_'.join(i['task'].rstrip().lstrip().split(' ')) if i['task'] else '___'
                old_timers += f"{i['start_time'][:-3]}.{task}-{i['result']} "
                # logger.debug(old_timers)
        return old_timers

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Work timer')
        self.resizable(False,False)
        self.geometry('700x300')

class App_Frame(tk.Frame):

    def __init__(self, container):
        super().__init__(container)
        self.timer_obj = None
        self.obj_list = []

        self.lbl_head = tk.Label(text="Задача:")
        self.lbl_head.grid(
            row=0, column=0, columnspan=5, pady=10)
        
        self.lbl_history_tasks = tk.Label(text=f"Задачи {datetime.today().strftime('%d/%m/%Y')}")
        self.lbl_history_tasks.grid(row=0, column=5, columnspan=2,sticky='E')
        
        # list of history tasks
        self.history_l = read_history()
        self.history_val = StringVar(value=self.history_l)
        self.history_listbox = tk.Listbox(listvariable=self.history_val, width=30)
        self.history_listbox.grid(row=1, column=5, columnspan=2, rowspan=3, sticky='EW', padx=10)

        self.task_text = StringVar()
        self.task_text.set('Task')
        self.ent_task_text = tk.Entry(width=50, textvariable=self.task_text)
        self.ent_task_text.grid(row=1, column=0, columnspan=5, sticky=('EW'), padx=10)

        self.btn_start = tk.Button(text="start", command=self.start_timer)
        self.btn_start.grid(row=2, column=0, columnspan=2, sticky="EW", padx=10)

        self.btn_pause = tk.Button(text="pause", command=self.pause, state='disable')
        self.btn_pause.grid(row=2, column=2)

        self.btn_stop = tk.Button(text="stop", command=self.stop_timer, state='disable')
        self.btn_stop.grid(row=2, column=3, columnspan=2,  sticky="EW")

        self.current_task_text = StringVar()
        self.current_task_text.set("---")
        self.lbl_current_task = tk.Label(textvariable=self.current_task_text, fg="red")
        self.lbl_current_task.grid(row=3, column=0, columnspan=4)

        self.counter = StringVar()
        self.counter.set("---")
        self.lbl_counter = tk.Label(textvariable=self.counter, font='bold')
        self.lbl_counter.grid(row=3, column=3)


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

        self.timer_obj = Timer()
        self.timer_obj.text = self.ent_task_text.get()
        self.obj_list.append(self.timer_obj)
        self.switch_button()
        self.current_task_text.set(
            f'{self.timer_obj.text} - {self.timer_obj.start_end_list[0].strftime("%H:%M:%S")}')
        self.count()
            

    def pause(self):

        if self.timer_obj.is_paused:
            self.timer_obj.switch_pause()
            self.timer_obj.start_end_list.append(datetime.now())

        else:
            self.timer_obj.switch_pause()
            self.stop()


    def stop(self):

        self.timer_obj.start_end_list.append(datetime.now())
        self.count()

    # @logger.catch
    def stop_timer(self):

        if not self.timer_obj.is_paused:
            self.timer_obj.start_end_list.append(datetime.now())
        self.timer_obj.result = self.timer_obj.result_time()
        self.counter.set(self.timer_obj.result_time())
        self.save_timers()
        self.timer_obj = None
        self.switch_button()
        self.task_text.set('')
        self.current_task_text.set('')
        self.counter.set('')

    # @logger.catch
    def save_timers(self):
        saver(self.timer_obj)
        self.history_val.set(read_history())

    def count(self):
        
        if self.timer_obj:
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
        self.start_end_list = [datetime.now(),]
        self.is_paused = False
        self.result = False

    def switch_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

    def result_time(self):
        
        result = timedelta()
        for i in range(0, len(self.start_end_list), 2):
            result += self.start_end_list[i+1] - self.start_end_list[i]
        return str(result).split('.')[0]


# if __name__ == "__main__":

# @logger.catch
def main():

    root = Window()
    App_Frame(root)
    root.mainloop()

main()