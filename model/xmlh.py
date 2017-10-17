import xml.etree.ElementTree as ElementTree
import util
import copy


def remove_outliers(file_name):
    """
    Finds and removes the outlier points from the stroke in the given file.
    :param file_name: The file that will be scanned for outliers.
    :return:
    """
    strokes = build_structure(file_name)

    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    outliers = get_outliers(strokes)

    i = 0
    while i < len(outliers):
        root.find('StrokeSet')[outliers[i][0]].remove(root.find('StrokeSet')[outliers[i][0]][outliers[i][1]])
        for j in range(len(outliers)):
            if outliers[i][0] == outliers[j][0]:
                outliers[j] = (outliers[j][0], outliers[j][1]-1)
        del outliers[i]
        i += 1

    tree.write(file_name)


def get_outliers(data):

    stroke_lengths = []
    for stroke in data:
        stroke_length = 0
        for index, point in enumerate(stroke[:-1]):
            try:
                stroke_length += util.point_2_point(stroke[index], stroke[index + 1])
            except IndexError:
                pass
        stroke_lengths.append(stroke_length/len(stroke))

    q1, q2, q3 = util.get_quartiles(stroke_lengths)

    length_threshold = q3 + 1.5 * (q3 - q1)

    faulty_strokes = []
    for stroke_index, stroke in enumerate(data):
        if stroke_lengths[stroke_index] > length_threshold:
            faulty_strokes.append(stroke_index)

    lines = get_lines(data, faulty_strokes)

    first_x_pos = util.get_quartiles([line[0][0] for line in lines])[2]

    points = {}
    for stroke_index in faulty_strokes:
        points[stroke_index] = get_outlier_points(stroke_index, data[stroke_index], lines, first_x_pos)

    return points


def get_lines(data, faulty_strokes):
    distances = []
    for stroke_index, stroke in enumerate(data):
        if stroke_index not in faulty_strokes:
            median_x = util.get_quartiles([point[0] for point in stroke])[2]
            if stroke_index < len(data) - 1:
                next_median_x = util.get_quartiles([point[0] for point in data[stroke_index + 1]])[2]
                distances.append(util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)))

    q1, q2, q3 = util.get_quartiles(distances)

    length_threshold = q3 + 1.5 * (q3 - q1)

    # Todo

    lines = []
    index = 0
    for stroke_index, stroke in enumerate(data):
        median_x = util.get_quartiles([point[0] for point in stroke])[2]
        median_y = util.get_quartiles([point[1] for point in stroke])[2]
        if stroke_index < len(data) - 1:
            next_median_x = util.get_quartiles([point[0] for point in data[stroke_index + 1]])[2]
            if util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)) > length_threshold:
                index += 1
        lines.append((index, median_x, median_y))

    return lines


def get_outlier_points(index, stroke, line, first_x_pos):
    points = []
    for points in stroke:
        pass

    # Todo

    return points


# def get_outlier_points(length_threshold, stroke_set):
#     suspects = {}
#     default = 0
#     for i, stroke in enumerate(stroke_set):
#         for j, point_pair in enumerate(stroke):
#             if point_pair[0] > length_threshold:
#                 suspects[point_pair[1]] = 1 if suspects.get(point_pair[1], default) == 0 else 2
#                 suspects[point_pair[2]] = 1 if suspects.get(point_pair[2], default) == 0 else 2
#
#             # Todo
#         for point_pair in [key for key in suspects if key[0] == i]:
#             pass
#
#         # for point_pair in []
#             # elif j == 1 and suspects.get(point_pair[1], default) != 0:
#             #     suspects[distance_data[i][0][1]] = 2
#             #     suspects[distance_data[i][0][2]] = 2
#             # if j == len(stroke)-1 and suspects.get(point_pair[1], default) != 0\
#             #         and suspects[point_pair[1]] == 1 and suspects.get(point_pair[2], default) != 0 and\
#             #                 suspects[point_pair[2]] == 1:
#             #     print("asd")
#             #     suspects[point_pair[1]] = 2
#             #     suspects[point_pair[2]] = 2
#
#     outliers = []
#     for key, value in suspects.items():
#         if value == 2:
#             outliers.append(key)
#
#     return outliers


def mark_horizontal(file_name, indexes):
    """
    Creates an attribute in the given file, for every stroke,
     and gives it value, based on if it is horizontal or not.
    :param file_name: Name of the xml.
    :param indexes: Horizontal indexes, that will be marked as "Yes".
    :return:
    """
    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    for i in range(len(root.find('StrokeSet'))):
        if i in indexes:
            root.find('StrokeSet')[i].attrib['Horizontal'] = "Yes"
        else:
            root.find('StrokeSet')[i].attrib['Horizontal'] = "No"

    tree.write(file_name)


def build_structure(file_name):
    """
    Creates a multi layer list structure of the given xml.
    :param file_name: Name of the XML.
    :return: The structured list of the XML.
    """
    with open(file_name, 'r') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        strokes = []
        # StrokeSet tag stores the strokes in the xml
        for index in range(len(root.find('StrokeSet'))):
            strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])),
                             float(point.attrib['time'])) for point in root.find('StrokeSet')[index][:]])

        return strokes


def main():
    # remove_outlier_points('/home/patrik/Desktop/TestStrokes/corrected/d10-718.xml')
    pass


if __name__ == "__main__":
    main()
