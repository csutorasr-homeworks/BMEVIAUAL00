import xml.etree.ElementTree as ElementTree
import util


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

    points = {}
    for stroke_index in faulty_strokes:
        points[stroke_index] = get_outlier_points(stroke_index,
                                                  data[stroke_index],
                                                  [line_element for line_element in lines if
                                                   line_element[0] == lines[stroke_index][0]])

    return points


def get_lines(data, faulty_strokes):
    distances = []

    correct_strokes = [stroke for stroke_index, stroke in enumerate(data) if stroke_index not in faulty_strokes]
    for stroke_index, stroke in enumerate(correct_strokes):
            median_x = util.get_quartiles([point[0] for point in stroke])[2]
            if stroke_index < len(data) - 1:
                next_median_x = util.get_quartiles([point[0] for point in data[stroke_index + 1]])[2]
                distances.append(util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)))

    q1, q2, q3 = util.get_quartiles(distances)

    length_threshold = q3 + 1.5 * (q3 - q1)

    lines = []
    index = 0
    for stroke_index, stroke in enumerate(correct_strokes):
        median_x = util.get_quartiles([point[0] for point in stroke])[2]
        median_y = util.get_quartiles([point[1] for point in stroke])[2]
        if stroke_index < len(data) - 1:
            next_median_x = util.get_quartiles([point[0] for point in data[stroke_index + 1]])[2]
            if util.point_2_point(util.Point(median_x, 0), util.Point(next_median_x, 0)) > length_threshold:
                index += 1
        lines.append((index, median_x, median_y))

    for stroke_index in faulty_strokes:
        lines.insert(stroke_index, (-1, -1, -1))

    for stroke_index in faulty_strokes:
        lines[stroke_index] = predict_stroke_position(stroke_index, lines, data)

    return lines


def predict_stroke_position(stroke_index, lines, strokes):

    distances = []
    if len(strokes)-1 > stroke_index > 0:
        if lines[stroke_index-1][0] == lines[stroke_index+1][0]:
            line_index = lines[stroke_index-1][0]
        else:
            line_index = lines[stroke_index-1][0] if (util.point_2_set(lines[stroke_index-1][1], strokes[stroke_index])
                                                      < util.point_2_set(lines[stroke_index+1][1],
                                                                         strokes[stroke_index])) else\
                lines[stroke_index + 1][0]

        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]
        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))

        if line_index == lines[stroke_index-1][0]:
            median_x = lines[stroke_index-1][1] + util.get_average(distances)
        else:
            median_x = lines[stroke_index+1][1] - util.get_average(distances)

    elif stroke_index == 0:
        line_index = lines[stroke_index + 1][0]
        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]
        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))

        median_x = lines[stroke_index+1][1] - util.get_average(distances)

    else:
        line_index = lines[stroke_index - 1][0]
        x_medians = [stroke[1] for stroke in lines if stroke[0] == line_index]
        for index, x_median in enumerate(x_medians[:-1]):
            distances.append(util.point_2_point(util.Point(x_median, 0), util.Point(x_medians[index + 1], 0)))
        median_x = lines[stroke_index-1][1] + util.get_average(distances)

    median_y = util.get_average([stroke[2] for stroke in lines if stroke[0] == line_index])

    return line_index, median_x, median_y


def get_outlier_points(index, stroke, line):
    points = []





    return points


def get_point_distance_threshold(strokes):
    distances = []
    for stroke in strokes:
        for distance in util.get_set_distance(stroke):
            distances.append(distance)

    q1, q2, q3 = get_outliers(distances)

    return q3 + 1.5 * (q3 - q1)


# def get_outlier_points(length_threshold, stroke_set):
#     suspects = {}
#     default = 0
#     for i, stroke in enumerate(stroke_set):
#         for j, point_pair in enumerate(stroke):
#             if point_pair[0] > length_threshold:
#                 suspects[point_pair[1]] = 1 if suspects.get(point_pair[1], default) == 0 else 2
#                 suspects[point_pair[2]] = 1 if suspects.get(point_pair[2], default) == 0 else 2
#
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
            strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])))
                            for point in root.find('StrokeSet')[index][:]])

        return strokes


def main():
    # remove_outlier_points('/home/patrik/Desktop/TestStrokes/corrected/d10-718.xml')
    pass


if __name__ == "__main__":
    main()
