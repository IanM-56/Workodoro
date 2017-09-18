import tkinter as tk
from tkinter import ttk
from cycles import Cycle
from datetime import timedelta
from itertools import cycle


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
        work_cycle = Cycle(25, name="Work", color="red")
        break_cycle = Cycle(5, name="Break", color="lightgreen")
        rest_cycle = Cycle(15, name="Rest", color="green")
        self.cycles = cycle([work_cycle, break_cycle, work_cycle, break_cycle,
                             work_cycle, break_cycle, work_cycle, rest_cycle])
        self.cycle = None
        self.switch_cycle()
        self.fast_forwarding = False
        self.bind("<Button-1>", self.fast_forward)

    def switch_cycle(self):
        self.progressive.progress.stop()
        self.cycle = next(self.cycles)
        self.cycle.start_cycle()
        self.bell()
        self.progressive.load_cycle(self.cycle)
        self.after(100, self.progress_check)
        self.fast_forwarding = False

    def progress_check(self):
        pb = self.progressive.progress
        tm = self.progressive.time
        d = self.cycle.delta().seconds
        tm["text"] = "{}:{}".format(int(d / 60), str(d % 60).zfill(2))
        pb["value"] = self.cycle.percent()
        if pb["value"] >= 99:
            self.switch_cycle()
        elif self.fast_forwarding:
            self.after(1, self.progress_check)
        else:
            self.after(100, self.progress_check)

    def fast_forward(self, event=None):
        if event is not None:
            self.fast_forwarding = True
        if self.fast_forwarding:
            self.cycle.start -= timedelta(seconds=1)
            self.after(1, self.fast_forward)


class Progressive(tk.Frame):

    def __init__(self):
        super().__init__()
        self.progress = ttk.Progressbar(self, length=70)
        self.mode = tk.Label(self, text="Mode")
        self.time = tk.Label(self, text="Time")
        self.progress.pack()
        self.progress.stop()
        self.mode.pack(side=tk.LEFT)
        self.time.pack(side=tk.RIGHT)
        self.pack(padx=5, pady=5)

    def load_cycle(self, cycle):
        self.mode["text"] = cycle.name
        s = ttk.Style()
        s.theme_use("default")
        s.configure("colored.Horizontal.TProgressbar", background=cycle.color)
        self.progress["style"] = "colored.Horizontal.TProgressbar"


workodoro = Workodoro()
workodoro.mainloop()
