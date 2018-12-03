import tkinter as tk
import time

class PopupWindow:
    def __init__(self, master):
        top = self.top = tk.Toplevel(master, bg='black')
        self.l = tk.Label(top, text='Enter the name of your task.', fg='red', bg='black')
        self.l.pack()
        self.e = tk.Entry(top)
        self.e.pack()
        self.b = tk.Button(top, text='Ok', command=self.cleanup)
        self.b.pack()


    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        # if you have a large number of widgets you can specify
        # the attributes for all widgets simply like this.
        master.option_add('*Button.Background', 'black')
        master.option_add('*Button.Foreground', 'red')

        master.title('Time Keeping App')
        # you can set the geometry attribute to change the root windows size
        master.geometry('150x100') # the size you want the app to be
        master.resizable(0, 0) # don't allow resizing in the x or y direction

        self.back = tk.Frame(master=root, bg='black')
        # don't allow the widgets inside to determine the frame's width / height
        self.back.pack_propagate(0)
        # expand the frame to fill the root window
        self.back.pack(fill=tk.BOTH, expand=1)

        self.master = master
        self.start_task_btn = tk.Button(self.back, text='Start Task', command=self.start_task)
        self.start_task_btn.pack()
        self.stop_task_btn = tk.Button(self.back, text='Stop Task', command=self.stop_task)
        self.stop_task_btn.pack()
        self.stop_task_btn['state'] = 'disabled'
        self.close_btn = tk.Button(self.back, text='Quit', command=master.destroy)


    def _get_duration(self, start, end):
        duration = ''
        current_time = end - start

        days = current_time // 86400
        if days != 0:
            current_time -= 86400 * days
            duration += f'{days} {"Day" if days == 1 else "Days"} '

        hours = current_time // 3600
        if hours != 0:
            duration += f'{hours} {"Hour" if hours == 1 else "Hours"} '
            current_time -= 3600 * hours
        elif duration:
            duration += '0 hours '

        mins = current_time // 60
        if mins != 0:
            duration += f'{mins} {"Minute" if mins == 1 else "Minutes"} '
            current_time -= 60 * mins
        elif duration:
            duration += '0 Minutes '

        secs = round(current_time, 2)
        if secs == 1.0:
            secs = int(secs)
        if not duration:
            duration = f'{secs} {"Second" if secs == 1 else "Seconds"}'
        else:
            duration += f'and {secs} {"Second" if secs == 1 else "Seconds"}'

        return duration


    def start_task(self):
        self.w = PopupWindow(self.master)
        self.start_task_btn['state'] = 'disabled'
        self.master.wait_window(self.w.top)
        self.timer = time.time()
        self.start_time = time.ctime()
        self.stop_task_btn['state'] = 'normal'

    def stop_task(self):
        stopped = time.ctime()
        duration = self._get_duration(self.timer, time.time())
        with open('Tasks.txt', 'a+') as f:
            f.write(f'Task: {self.w.value}\n')
            f.write(f'{"-" * (len(self.w.value) + 6)}\n')
            f.write(f'Started: {self.start_time}\n')
            f.write(f'Stopped: {stopped}\n')
            f.write(f'Duration: {duration}\n\n')

        self.stop_task_btn['state'] = 'disabled'
        self.start_task_btn['state'] = 'normal'


if __name__ == '__main__':
    root = tk.Tk()
    m = mainWindow(root)
    root.mainloop()
