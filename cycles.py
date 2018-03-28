from _datetime import datetime as dt
from datetime import timedelta as td


class Cycle:
    __slots__ = ["duration", "start", "name", "color"]

    def __init__(self, minutes: int, seconds: int = 0, *, name: str = "Cycle", color: str = "blue") -> None:
        self.duration = td(minutes=minutes, seconds=seconds)
        self.start: dt = dt.now()
        self.name: str = name
        self.color: str = color

    def end(self) -> dt:
        return self.start + self.duration

    def delta(self) -> td:
        return self.end() - dt.now()

    def percent(self) -> float:
        return 100 * (dt.now() - self.start) / (self.end() - self.start)

    def start_cycle(self) -> None:
        self.start = dt.now()
