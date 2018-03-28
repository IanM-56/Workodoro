import tkinter as tk
from tkinter import ttk

from cycles import Cycle


class Progressive(tk.Frame):
    __slots__ = ["progress", "mode", "time"]

    def __init__(self) -> None:
        super().__init__()
        self.progress: ttk.Progressbar = ttk.Progressbar(self, length=70)
        self.mode: tk.Label = tk.Label(self, text="Mode")
        self.time: tk.Label = tk.Label(self, text="Time")
        self.progress.pack()
        self.progress.stop()
        self.mode.pack(side=tk.LEFT)
        self.time.pack(side=tk.RIGHT)
        self.pack(padx=5, pady=5)

    def load_cycle(self, cycle: Cycle) -> None:
        self.mode["text"] = cycle.name
        s: ttk.Style = ttk.Style()
        s.theme_use("default")
        s.configure("colored.Horizontal.TProgressbar", background=cycle.color)
        self.progress["style"] = "colored.Horizontal.TProgressbar"
