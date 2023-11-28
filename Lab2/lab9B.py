
import queue

class Node:
    def __init__(self, prio, data):
        self.prio = prio
        self.data = data

    def __lt__(self, other):
        return self.prio<other.prio
    