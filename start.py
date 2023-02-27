import time
from tkinter import *
from tkinter import ttk


class Timer():
    def __init__(self, subscribe, start):
        self.subscribe = subscribe
        self.start = start
        
    def stop(self):
        print(self.start + 'stop')
        return self.start + 'stop'

def start(subscribe):
    timer_work = Timer(subscribe, time.time())
    return timer_work
    

root = Tk()
root.title('Timer for work')

content = ttk.Frame(root)

s = Label(root, text='Описание работы')
s.grid(row=0, columnspan=5)

subscribe = StringVar()
ent = ttk.Entry(root, textvariable=subscribe, width=100)
ent.grid(row=1, columnspan=5, pady=3)

start_time = IntVar()
start_btn = ttk.Button(root, text='START', width=40, command=start)
start_btn.grid(column='0', row='2', columnspan=2, sticky=(W), pady=3)
pause_btn = ttk.Button(root, text='PAUSE')
pause_btn.grid(column='2', row='2')

pause_btn = ttk.Button(root, text='STOP', width=40, command=timer_work.stop)
pause_btn.grid(column='3', row='2', columnspan=2,sticky=(E))



root.mainloop()
