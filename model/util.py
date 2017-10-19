import math
import copy


class Point:
    """
    Class for storing x, y coordinates.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = math.sqrt(x**2 + y**2)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return Point(self.x + other.x, self.y + other.y)


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


def point_2_set(point, points):
    """
    Distance between a point and a set of points.
    :param point: A single point
    :param points: A set of points.
    :return: Distance
    """
    distances = []
    for element in points:
        distances.append(point_2_point(point, element))
    return min(distances)


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


def get_average(data):
    """
    Calculates the average of a given data set.
    :param data: Provided data.
    :return: Average.
    """
    return sum(copy.copy(data))/len(data)


def get_set_distance(data):
    """
    Calculates the distance between every single point of a given data set.
    :param data: Provided data.
    :return: List of distances.
    """
    distances = []
    for i in range(len(data[:-1])):
        j = i+1
        while j < len(data):
            distances.append(point_2_point(data[i], data[j]))
            j += 1

    return distances


def find_all(data, value):
    """

    :param data:
    :param value:
    :return:
    """
    indexes = []
    for index, element in enumerate(data):
        if element == value:
            indexes.append(index)

    return indexes


def dfs(adjacency_list):

    grouped_points = set()
    grouped_points.add(0)

    grouped_points = grouped_points | _dfs(0, adjacency_list, grouped_points)

    return grouped_points


def _dfs(index, adjacency_list, grouped_points):

    for vertex in adjacency_list[index]:
        if vertex not in grouped_points:
            index = vertex
            grouped_points.add(vertex)
            _dfs(index, adjacency_list, grouped_points)

    return grouped_points


def get_quartiles(data):
    """
    Finds the first, second and third quartiles for a given data set.
    :param data: Data that will be analyzed.
    :return: First, second and third quartiles.
    """
    ordered_data = copy.copy(data)
    ordered_data.sort()

    # Separating the odd and the even length cases.
    if len(ordered_data) % 2 == 1:
        q2 = ordered_data[int(len(ordered_data) / 2)]
    else:
        q2 = (ordered_data[int(len(ordered_data) / 2) - 1] + ordered_data[int(len(ordered_data) / 2)]) / 2

    if len(ordered_data[int(len(ordered_data) / 2) + len(ordered_data) % 2:]) % 2 == 1:
        q1 = ordered_data[int(len(ordered_data) / 2 - 1 - int(len(ordered_data) / 2) / 2)]
        q3 = ordered_data[int(len(ordered_data) / 2 + int(len(ordered_data) / 2) / 2)]
    else:
        q1 = (ordered_data[int(len(ordered_data) / 2 - 1 - int(len(ordered_data) / 2) / 2)] +
              ordered_data[int(len(ordered_data) / 2 - int(len(ordered_data) / 2) / 2)]) / 2
        q3 = (ordered_data[int(len(ordered_data) / 2 - 1 + len(ordered_data) % 2 + int(len(ordered_data) / 2) / 2)] +
              ordered_data[int(len(ordered_data) / 2 + len(ordered_data) % 2 + int(len(ordered_data) / 2) / 2)]) / 2

    return q1, q2, q3

