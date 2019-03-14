from itertools import count
from datetime import datetime, timedelta


class Node:
    registry = []
    _ids = count(0)

    def __init__(self):
        self.registry.append(self)
        self.name = next(self._ids)
        self.dur = 0
        self.dep = []
        self.crit = []
        self.lvl = 0
        self.start = datetime.date
        self.end = datetime.date
        self.x = 0
        self.y = 0
        self.cx = 0
        self.cy = 0
        self.tasks = []
