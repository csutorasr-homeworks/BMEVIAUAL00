import math


class Point:
    """
    Class for storing x, y coordinates.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = math.sqrt(x**2 + y**2)


class Stroke:
    """
    Class for storing stroke information.
    """

    def __init__(self, start_time, end_time, coordinates):

        self.coordinates = coordinates
        self.start_time = start_time
        self.end_time = end_time
        self.horizontal = False
