import tkinter as tk
from tkinter import ttk
import datetime


class Workodoro(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Workodoro")
        self.grid()
        self.resizable(False, False)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.lift()
        self.progressive = Progressive()
        self.cycle = 0
        self.cycles = [self.work_cycle, self.rest_cycle]
        self.start = datetime.datetime.now()
        self.target = datetime.datetime.now()
        self.deltaTime = lambda: self.target - datetime.datetime.now()
        self.percentTime = lambda: 100 * (datetime.datetime.now() - self.start)/(self.target - self.start)
        self.switch_cycle()

    def work_cycle(self):
        self.start = datetime.datetime.now()
        self.target = self.start + datetime.timedelta(minutes=25)
        self.progressive.mode["text"] = "Work"
        self.progressive.set_bar_color("red")
        self.after(100, self.progress_check)

    def rest_cycle(self):
        self.start = datetime.datetime.now()
        self.target = self.start + datetime.timedelta(minutes=5)
        self.progressive.mode["text"] = "Rest"
        self.progressive.set_bar_color("green")
        self.after(100, self.progress_check)

    def switch_cycle(self):
        self.progressive.progress.stop()
        self.cycles[self.cycle % len(self.cycles)]()
        self.cycle += 1
        self.bell()

    def progress_check(self):
        pb = self.progressive.progress
        tm = self.progressive.time
        d = self.deltaTime().seconds
        tm["text"] = "{}:{}".format(int(d / 60), str(d % 60).zfill(2))
        pb["value"] = self.percentTime()
        if pb["value"] >= 99:
            self.switch_cycle()
        else:
            self.after(100, self.progress_check)


class Progressive(tk.Frame):

    def __init__(self):
        super().__init__()
        self.progress = ttk.Progressbar(self, length=100)
        self.mode = tk.Label(self, text="Mode")
        self.time = tk.Label(self, text="Time")
        self.progress.pack()
        self.progress.stop()
        self.mode.pack(side=tk.LEFT)
        self.time.pack(side=tk.RIGHT)
        self.pack(padx=5, pady=5)

    def set_bar_color(self, color):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("colored.Horizontal.TProgressbar", background=color)
        self.progress["style"] = "colored.Horizontal.TProgressbar"


workodoro = Workodoro()
workodoro.mainloop()
