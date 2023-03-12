from typing import List


class Group:
    def __init__(self, name, parties, colour=None):
        self.name = name
        self.parties = parties
        self.colour = colour


class Period:
    def __init__(self, groups: List[Group], start, end=None):
        self.groups = groups
        self.start = start
        self.end = end
