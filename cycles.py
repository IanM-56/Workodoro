import datetime


class Cycle:

    def __init__(self, minutes, seconds=0, *, name="Cycle", color="blue"):
        self.duration = datetime.timedelta(minutes=minutes, seconds=seconds)
        self.start = datetime.datetime.now()
        self.end = lambda: self.start + self.duration
        self.delta = lambda: self.end() - datetime.datetime.now()
        self.percent = lambda: 100 * (datetime.datetime.now() - self.start) / (self.end() - self.start)
        self.name = name
        self.color = color

    def start_cycle(self):
        self.start = datetime.datetime.now()
