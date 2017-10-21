import xml.etree.ElementTree as ElementTree
import util
import numpy as np
from collections import OrderedDict


def remove_outliers(file_name):
    """
    Finds and removes the outlier points from the stroke in the given file.
    :param file_name: The file that will be scanned for outliers.
    """
    strokes = build_structure(file_name)

    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    # Removal of the outliers from the xml.
    # The list of indexes is reversed so it won't cause indexation problems, when deleted from the xml.
    for stroke_index, stroke in reversed(get_outliers(strokes, file_name).items()):
        for point_index in reversed(stroke):
            root.find('StrokeSet')[stroke_index].remove(root.find('StrokeSet')[stroke_index][point_index])

    tree.write(file_name)


def get_outliers(data, file_name):
    """
    Discovers the strokes with extraordinarily large distance to registered points ratios in the given
    stroke set, then finds the points, that cause the anomaly.
    :param data: The stroke set of the text.
    :param file_name: The file that will be scanned for outliers.
    :return: Indexes of the points.
    """
    # Calculating the limit of the distance between two points in each stroke.
    timed_data = build_structure(file_name, time=True)
    # The distances are divided by the delta time between sampling, to adjust to the uneven periods.
    normalized_length_limit = get_point_distance_limit(timed_data, time=True)

    faulty_strokes = []
    for stroke_index, stroke in enumerate(timed_data):
        for index, point in enumerate(stroke[:-1]):
                if (util.point_2_point(stroke[index][0], stroke[index + 1][0]) /
                        (stroke[index + 1][1] - stroke[index][1] if stroke[index + 1][1] != stroke[index][1]
                         else 0.01)) > normalized_length_limit*2 and stroke_index not in faulty_strokes:
                    faulty_strokes.append(stroke_index)

    # Dividing the strokes into lines.
    lines = get_lines(data, faulty_strokes, file_name)

    # Calculating the limit of distance between two sequential points in the set of strokes.
    point_length_limit = get_point_distance_limit(data)

    # Ordered dictionary of faulty strokes indexes as keys, and lists of the faulty points' indexes as values.
    points = OrderedDict()
    for stroke_index in faulty_strokes:
        points[stroke_index] = get_outlier_points(data[stroke_index], lines[stroke_index], point_length_limit)

    return points


def get_lines(data, faulty_strokes, file_name):
    """
     Divides the stroke set into lines.
    :param data: Set of strokes.
    :param faulty_strokes: A list of strokes that have been determined as faulty,
    based on their stroke length to number of registered points ratio.
    :param file_name: The file that will be scanned for outliers.
    :return: The data structure containing the strokes separated according to the lines of the text.
    """
    def get_nb_eol(file):
        """
        Counts the EOLs in the text of the xml.
        :param file: The file that will be scanned for outliers.
        :return: Number of EOLs.
        """
        tree = ElementTree.parse(file)
        root = tree.getroot()

        return root.find('Transcription').find('Text').text.strip().count('\n')

    # The calculation of the distances between a text's strokes. The strokes are represented as a single number,
    # the median value of the registered points' x coordinates. This step is directed to find the end of lines
    # in the written text, hence the values of the y coordinates are not necessary, since the outlying distances
    # can be found as the large jumps of distance values at the end the of lines.
    distances = []

    # The length statistics are created only on the correct strokes, so the anomalies in the faulty strokes
    # will not interfere with the detection of EOL.
    correct_strokes = [stroke for stroke_index, stroke in enumerate(data) if stroke_index not in faulty_strokes]
    for stroke_index, stroke in enumerate(correct_strokes):
            median_x = util.get_quartiles([point.x for point in stroke])[2]
            if stroke_index < len(correct_strokes) - 1:
                next_median_x = util.get_quartiles([point.x for point in correct_strokes[stroke_index + 1]])[2]
                distances.append(util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)))

    distances.sort()

    # The largest distances will be the EOLs, so the last get_nb_eol(file_name)th element will be the distance limit.
    length_limit = distances[-get_nb_eol(file_name)] - 0.1

    lines = []
    index = 0

    # Creation of the data structure, that stores the line sequence number, the x and the y median values of a stroke.
    for stroke_index, stroke in enumerate(correct_strokes):
        median_x = util.get_quartiles([point.x for point in stroke])[2]
        median_y = util.get_quartiles([point.y for point in stroke])[2]
        if stroke_index < len(correct_strokes) - 1:
            next_median_x = util.get_quartiles([point.x for point in correct_strokes[stroke_index + 1]])[2]
            if util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)) > length_limit:
                index += 1
        # The list of faulty strokes are ignored in this step, since the iterated data is the list of correct strokes.
        # Reason for this is the extraordinary values in the faulty strokes, which prevent the correct calculation of
        # the stroke's location.
        lines.append((index, median_x, median_y))

    # The faulty strokes are inserted into the list in this step, with the predicted locations.
    for stroke_index in faulty_strokes:
        lines.insert(stroke_index, predict_stroke_position(stroke_index, lines, data))

    return lines


def predict_stroke_position(stroke_index, lines, strokes):
    """
    Predicts the faulty stroke's position, based on the surrounding strokes.
    If the stroke is not on the edges of a line, it will be placed at the middle of
    the distance between the two adjacent strokes. If the stroke is the first or the final
    one, it will be placed at a location calculated by the parameters of the corresponding
    line.
    :param stroke_index: The index of the stroke in the stroke set.
    :param lines: The structured set of strokes, organised into lines.
    :param strokes: The set of strokes.
    :return: The sequence number of the line, in which the stroke has been determined to be in.
    The x and the y coordinates of the position.
    """
    # The distances list stores the distance between the strokes' position in the line.
    distances = []
    # The stroke is not at the first or final index. The values of the surrounding strokes can be used.
    if len(strokes) - 1 > stroke_index > 0:
        # lines[stroke_index] is a tuple, which first element is the sequence number of the line.
        # If the stroke's previous and next neighbours are in the same line, then the stroke is in that line.
        if lines[stroke_index - 1][0] == lines[stroke_index + 1][0]:
            line_index = lines[stroke_index-1][0]
        # If they are in different lines, then the stroke must be either at the end of the line or at the beginning.
        else:
            prev_median_y = util.get_average([stroke[2] for stroke in lines if stroke[0] == lines[stroke_index - 1][0]])
            next_median_y = util.get_average([stroke[2] for stroke in lines if stroke[0] == lines[stroke_index + 1][0]])
            # The stroke will be placed in the line, in which the stroke is closest to its possible location.
            line_index = lines[stroke_index - 1][0] if\
                util.point_2_set(util.Point(lines[stroke_index - 1][1], prev_median_y),
                                 strokes[stroke_index]) <\
                util.point_2_set(util.Point(lines[stroke_index + 1][1], next_median_y),
                                 strokes[stroke_index]) else lines[stroke_index + 1][0]

        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]

        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))

        # If the stroke was determined to be in the line of the previous stroke, then its x position is calculated by
        # adding the average of distances between the strokes' positions in that line, to the final stroke of the line.
        if line_index == lines[stroke_index - 1][0]:
            x_coordinate = lines[stroke_index - 1][1] + util.get_average(distances)
        # If its in the next line, the same principle is applied.
        else:
            x_coordinate = lines[stroke_index + 1][1] - util.get_average(distances)

    # The stroke is the first in the stroke set.
    elif stroke_index == 0:
        line_index = lines[stroke_index + 1][0]
        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]
        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))

        x_coordinate = lines[stroke_index + 1][1] - util.get_average(distances)

    # The stroke is the final stroke in the set.
    else:
        line_index = lines[stroke_index - 1][0]
        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]
        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))

        x_coordinate = lines[stroke_index - 1][1] + util.get_average(distances)

    y_coordinate = util.get_average([stroke[2] for stroke in lines if stroke[0] == line_index])

    return line_index, x_coordinate, y_coordinate


def get_outlier_points(stroke, estimated_position, limit):
    """
    Finds the group of points, that is the closest to the stroke's estimated location,
    and returns the list of those points, which are not in this group.
    :param stroke: The inspected stroke.
    :param estimated_position: The stroke's estimated position.
    :param limit: The length limit of an edge between two vertices in the graph. The graph consists of
    the points of the stroke and it is represented as a graph for the algorithm that groups the points.
    :return: Ordered list of the outlier points' indexes.
    """

    def index_to_point(indexes, point_objects):
        """
        Gets the corresponding point objects in the stroke for the given set of indexes.
        :param indexes: Indexes to be interpreted as points.
        :param point_objects: A single stroke.
        :return: List of point objects.
        """
        return [point for point_index, point in enumerate(point_objects) if point_index in indexes]

    # The connected vertices are stored as ones in the matrix.
    adjacency_matrix = np.ones((len(stroke), len(stroke)))
    for row in range(len(adjacency_matrix)):
        for col in range(len(adjacency_matrix[row])):
            if row == col:
                adjacency_matrix[row][col] = -1
            elif util.point_2_point(stroke[row], stroke[col]) > limit*2:
                adjacency_matrix[row][col] = 0

    # The matrix is converted into a dict, that stores the vertex sequence numbers as keys, and
    # the corresponding connected vertices as values.
    adjacency_list = OrderedDict()
    for index, row in enumerate(adjacency_matrix):
        adjacency_list[index] = util.find_all(row, 1)

    # The connected vertices are organised into groups.
    groups = []
    while len(adjacency_list) > 0:
        group = util.dfs(adjacency_list)
        if len(group) != 0:
            groups.append(group)
        for index in group:
            if index in adjacency_list:
                del adjacency_list[index]

    # The groups are represented by their average position.
    average_positions = []
    for group in groups:
        average_positions.append(util.get_average_point(index_to_point(group, stroke)))

    # The distances between the average position and the predicted location is calculated.
    distances = []
    for position in average_positions:
        distances.append(util.point_2_point(position, util.Point(estimated_position[1], estimated_position[2])))

    # The group that is closest to the predicted location is chosen.
    closest_group = distances.index(min(distances))

    return [index for index, point in enumerate(stroke) if index not in groups[closest_group]]


def get_point_distance_limit(data, time=False):
    """
    Creates the statistics on the data, by the measurement of the distance
     between the registered points in each stroke.
    :param time: Flag, whether the average distance should be normalized by the delta time.
    :param data: Stroke set.
    :return: Length limit, that defines the outlier distance.
    """
    distances = []
    for stroke_index, stroke in enumerate(data):
        for point_index, point in enumerate(stroke[:-1]):
            if time:
                distances.append(util.point_2_point(stroke[point_index][0], stroke[point_index + 1][0]) /
                                 (stroke[point_index + 1][1] - stroke[point_index][1]) if
                                     stroke[point_index + 1][1] != stroke[point_index][1] else 0.01)
            else:
                distances.append(util.point_2_point(stroke[point_index], stroke[point_index+1]))

    q1, q2, q3 = util.get_quartiles(distances)

    return q3 + 1.5 * (q3 - q1)


def mark_horizontal(file_name, indexes):
    """
    Creates an attribute in the given file, for every stroke,
     and gives it value, based on if it is horizontal or not.
    :param file_name: Name of the xml.
    :param indexes: Indexes of horizontal strokes in the stroke set, that will be marked as "Yes".
    """
    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    for index in range(len(root.find('StrokeSet'))):
        if index in indexes:
            root.find('StrokeSet')[index].attrib['Horizontal'] = "Yes"
        else:
            root.find('StrokeSet')[index].attrib['Horizontal'] = "No"

    tree.write(file_name)


def dump_results(file_name, calculated_handedness=None, algorithm_log=None, manual_handedness=None):
    """
    Writes the gives values into the XML file, under the Results tag.
    :param file_name: Path of the XML file.
    :param calculated_handedness: The automatically calculated handedness value.
    :param algorithm_log: The user's description.
    :param manual_handedness: The handedness value determined by the user.
    """
    tree = ElementTree.parse(file_name)
    root = tree.getroot()
    general = root.find('General')

    if 'Results' not in [element.tag for element in general]:
        general.append(ElementTree.Element('Results'))

    if calculated_handedness is not None:
        general.find('Results').attrib['CalculatedHandedness'] = calculated_handedness

    if algorithm_log is not None:
        general.find('Results').attrib['AlgorithmLog'] = algorithm_log

    if manual_handedness is not None:
        general.find('Results').attrib['ManualHandedness'] = manual_handedness

    tree.write(file_name)


def build_structure(file_name, time=False):
    """
    Creates a multi layer list structure from the strokes of the given xml.
    :param file_name: Name of the XML.
    :param time: Flag, whether the time data from the xml is required.
    :return: The structured list of the XML.
    """
    with open(file_name, 'r') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        strokes = []
        # StrokeSet tag stores the strokes in the xml
        if time:
            for index in range(len(root.find('StrokeSet'))):
                strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])),
                                 float(point.attrib['time']))
                                for point in root.find('StrokeSet')[index][:]])
        else:
            for index in range(len(root.find('StrokeSet'))):
                strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])))
                                for point in root.find('StrokeSet')[index][:]])

        return strokes


def main():
    pass
    # remove_outliers('/home/patrik/Desktop/TestStrokes/f04/f04-314/strokesz.xml')
    # dump_results('/home/patrik/Desktop/TestStrokes/strokesz.xml', "asd", "kaki", "majom")


if __name__ == "__main__":
    main()
