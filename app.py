import tkinter as tk
from datetime import timedelta
from itertools import cycle
from tkinter import ttk

from cycles import Cycle
from progressive import Progressive


class Workodoro(tk.Tk):
    __slots__ = ["cycles", "cycle", "fast_forwarding"]

    def __init__(self) -> None:
        super().__init__()
        self.title("Workodoro")
        self.grid()
        self.resizable(False, False)
        self.attributes("-toolwindow", True)
        self.attributes("-topmost", True)
        self.lift()
        self.progressive: Progressive = Progressive()
        work_cycle: Cycle = Cycle(25, name="Work", color="red")
        break_cycle: Cycle = Cycle(5, name="Break", color="lightgreen")
        rest_cycle: Cycle = Cycle(15, name="Rest", color="green")
        self.cycles: cycle[Cycle] = cycle(
            [work_cycle, break_cycle, work_cycle, break_cycle,
             work_cycle, break_cycle, work_cycle, rest_cycle])
        self.switch_cycle()
        self.cycle: Cycle = None
        self.fast_forwarding: bool = False
        self.bind("<Button-1>", self.fast_forward)

    def switch_cycle(self) -> None:
        self.progressive.progress.stop()
        self.cycle = next(self.cycles)
        self.cycle.start_cycle()
        self.bell()
        self.progressive.load_cycle(self.cycle)
        self.after(100, self.progress_check)
        self.fast_forwarding = False

    def progress_check(self) -> None:
        pb: ttk.Progressbar = self.progressive.progress
        tm: tk.Label = self.progressive.time
        d: int = self.cycle.delta().seconds
        tm["text"] = "{}:{}".format(int(d / 60), str(d % 60).zfill(2))
        pb["value"] = self.cycle.percent()
        if pb["value"] >= 99:
            self.switch_cycle()
        elif self.fast_forwarding:
            self.after(1, self.progress_check)
        else:
            self.after(100, self.progress_check)

    def fast_forward(self, event=None) -> None:
        if event is not None:
            self.fast_forwarding = True
        if self.fast_forwarding:
            self.cycle.start -= timedelta(seconds=1)
            self.after(1, self.fast_forward)


workodoro: Workodoro = Workodoro()
workodoro.mainloop()
