from datetime import datetime
from tkinter import *
from tkinter import ttk


start_t = 0
stop_t = 0

def start():
    global start_t
    start_t = datetime.now()
    str_start = start_t.strftime('%H:M:%S')
    work_label['text'] = 'Начало:', str_start, subscribe.get()

def stop():
    stop_t = datetime.now()
    print (start_t, stop_t)
    delta_t = stop_t - start_t
    work_label['text'] = f'{delta_t} ушло на выполнение задачи: {subscribe.get()}'


root = Tk()
root.title('Timer for work')

content = ttk.Frame(root)

l1 = Label(root, text='Описание работы')
l1.grid(row=0, columnspan=5)

subscribe = ttk.Entry(root, width=100)
subscribe.grid(row=1, columnspan=5, pady=3)

start_btn = ttk.Button(root, text='START', width=40, command=start)
start_btn.grid(column='0', row='2', columnspan=2, sticky=(W), pady=3)
pause_btn = ttk.Button(root, text='PAUSE')
pause_btn.grid(column='2', row='2')

pause_btn = ttk.Button(root, text='STOP', width=40, command=stop)
pause_btn.grid(column='3', row='2', columnspan=2,sticky=(E))

work_label = ttk.Label(root, text='Начало:')
work_label.grid(column=0, row=4, sticky=(W))


root.mainloop()
