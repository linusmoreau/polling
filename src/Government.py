from typing import List


class Government:

    def __init__(self, name, parties: List[Party], start=None, end=None, colour=None):
        self.name = name
        self.parties = parties
        self.start = start
        self.end = end
        if colour is None:
            colour = self.parties[0].colour
