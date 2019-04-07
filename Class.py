from itertools import count
from datetime import datetime


class Node:
    registry = []
    _ids = count(0)

    def __init__(self):
        self.registry.append(self)
        self.name = str(next(self._ids))
        self.label = str(self.name)
        self.dur = 0
        self.dep = []
        self.crit = []
        self.lvl = 0
        self.start = datetime.date
        self.end = datetime.date
        self.x = 0
        self.y = 0
        self.ix = 0
        self.iy = 0
        self.ox = 0
        self.oy = 0
        self.tasks = []
