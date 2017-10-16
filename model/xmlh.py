import xml.etree.ElementTree as ElementTree
import util
import copy


def remove_outlier_points(file_name):
    # Todo
    """
    Finds and removes the outlier points from the stroke in the given file.
    :param file_name: The file that will be scanned for outliers.
    :return:
    """
    strokes, xml = build_structure(file_name, get_xml=True)

    distance_data = []

    # Creating a list that contains the speed of the pen between two points.
    for index in range(len(strokes)):
        distance_data.append([])
        for point_index in range(len(strokes[index][:-1])):
            distance_data[index].append((util.point_2_point(util.Point(strokes[index][point_index][0].x,
                                                                               strokes[index][point_index][0].y),
                                                                    util.Point(strokes[index][point_index+1][0].x,
                                                                               strokes[index][point_index+1][0].y)),
                                        (index, point_index),
                                        (index, point_index+1)))
            # If the delta time is 0 then it is set to 0.01 (the shortest time spam that can be recorded)

    length_data = []

    for stroke in distance_data:
        for point in stroke:
            length_data .append(point[0])

    # Finding the quartiles for outlier detection
    q1, q2, q3 = get_quartiles(length_data)

    length_threshold = q3 + 1.5*(q3-q1)

    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    outliers = get_outlier_points(length_threshold, distance_data)

    i = 0
    while i < len(outliers):
        print(str(outliers[i][0]) + " " + str(outliers[i][1]))
        root.find('StrokeSet')[outliers[i][0]].remove(root.find('StrokeSet')[outliers[i][0]][outliers[i][1]])
        for j in range(len(outliers)):
            if outliers[i][0] == outliers[j][0]:
                outliers[j] = (outliers[j][0], outliers[j][1]-1)
        del outliers[i]
        i += 1

    tree.write(file_name)


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


def get_outlier_points(length_threshold, distance_data):
    # Todo
    suspects = {}
    default = 0
    for i, stroke in enumerate(distance_data):
        for j, point_distance in enumerate(stroke):
            if point_distance[0] > length_threshold:
                suspects[point_distance[1]] = 1 if suspects.get(point_distance[1], default) == 0 else 2
                suspects[point_distance[2]] = 1 if suspects.get(point_distance[2], default) == 0 else 2
            elif j == 1 and suspects.get(point_distance[1], default) != 0:
                suspects[distance_data[i][0][1]] = 2
            if j == len(stroke)-1 and suspects.get(point_distance[1], default) != 0\
                    and suspects[point_distance[1]] == 1 and suspects.get(point_distance[2], default) != 0 and\
                            suspects[point_distance[2]] == 1:
                suspects[point_distance[1]] = 2
                suspects[point_distance[2]] = 2

    outliers = []
    for key, value in suspects.items():
        if value == 2:
            outliers.append(key)

    return outliers


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


def build_structure(file_name, get_xml):
    """
    Creates a multi layer list structure of the given xml.
    :param file_name: Name of the XML.
    :param get_xml: Boolean value determining, whether the xml object structure is required.
    :return: The structured list of the XML.
    """
    with open(file_name, 'r') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        # text_lines = [text_line.attrib['text'] for text_line in root[1][1:]]

        strokes = []
        xml = []
        # StrokeSet tag stores the strokes in the xml
        for index in range(len(root.find('StrokeSet'))):
            strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])),
                             float(point.attrib['time'])) for point in root.find('StrokeSet')[index][:]])
            xml.append([point for point in root.find('StrokeSet')[index]])

    if get_xml:
        return strokes, xml
    else:
        return strokes


def main():
    remove_outlier_points('/home/patrik/Desktop/TestStrokes/corrected/d10-718.xml')


if __name__ == "__main__":
    main()
