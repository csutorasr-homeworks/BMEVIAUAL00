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


def point_2_point(point_a, point_b):
    """
    Distance between two points.
    :param point_a: First point.
    :param point_b: Second point.
    :return: Distance of the points.
    """
    return math.sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)


def point_2_line(point_a, point_b, point):
    """
    Distance between a point and a line.
    :param point_a: First point of the vector.
    :param point_b: Second point of the vector.
    :param point: The point, which distance is to be measured from the line.
    :return: Distance of the point from the line.
    """
    return (math.fabs(-(point_b.y - point_a.y) * point.x + (point_b.x - point_a.x) * point.y +
                      (point_b.y - point_a.y) * point_a.x -
                      (point_b.x - point_a.x) * point_a.y)) / math.sqrt(
        (point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2)


def calculate_angle(point_a, point_b):
    """
    Calculates the included angle (degrees) of a vector and horizontal line.
    :param point_a: First point of the vector.
    :param point_b: Second point.
    :return: The included angle (degrees) of the vector, defined by the points,
     and a horizontal line.
    """
    vector = Point(point_b.x - point_a.x, point_b.y - point_a.y)
    n_vector = Point(vector.x / vector.length, vector.y / vector.length)
    return math.degrees(math.acos(n_vector.x))