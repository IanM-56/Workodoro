import tkinter as tk
from tkinter import ttk
from winsound import PlaySound, SND_FILENAME, SND_ASYNC
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
        self.percentTime = lambda: int(100 * (datetime.datetime.now() - self.start)/(self.target - self.start))
        self.switch_cycle()

    def work_cycle(self):
        self.start = datetime.datetime.now()
        self.target = self.start + datetime.timedelta(minutes=25)
        self.progressive.mode["text"] = "Work"
        self.after(100, self.progress_check)

    def rest_cycle(self):
        self.start = datetime.datetime.now()
        self.target = self.start + datetime.timedelta(minutes=5)
        self.progressive.mode["text"] = "Rest"
        self.after(100, self.progress_check)

    def switch_cycle(self):
        # PlaySound("sounds/ding.wav", SND_ASYNC)
        self.progressive.progress.stop()
        self.cycles[self.cycle % len(self.cycles)]()
        self.cycle += 1

    def progress_check(self):
        pb = self.progressive.progress
        tm = self.progressive.time
        d = self.deltaTime().seconds
        tm["text"] = "{}:{}".format(int(d / 60), d % 60)
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
        self.progress.grid()
        self.progress.stop()
        self.mode.grid()
        self.time.grid()
        self.pack(padx=5, pady=5)


workodoro = Workodoro()
workodoro.mainloop()
