import xml.etree.ElementTree as ElementTree
import util
import copy


def remove_outlier_points(file_name):
    strokes = build_structure(file_name)

    draw_speed = []

    for index in range(len(strokes)):
        draw_speed.append([])
        for point_index in range(len(strokes[index][:-1])):
            draw_speed[index].append(util.point_2_point(util.Point(strokes[index][point_index][0].x,
                                                                   strokes[index][point_index][0].y),
                                                        util.Point(strokes[index][point_index+1][0].x,
                                                                   strokes[index][point_index+1][0].y)) /
                                     ((strokes[index][point_index + 1][1] - strokes[index][point_index][1]) if
                                      (strokes[index][point_index + 1][1] - strokes[index][point_index][1]) > 0
                                      else 0.01))

    linear_data = []

    for stroke in draw_speed:
        for point in stroke:
            linear_data.append(point)

    q1, q2, q3 = get_quartiles(linear_data)

    outlier = q3 + 1.5*(q3-q1)

    tree = ElementTree.parse(file_name)
    root = tree.getroot()
    for index in range(len(root.find('StrokeSet'))):
        for point_index in range(len(root.find('StrokeSet')[index][:-1])):
            if draw_speed[index][point_index] > outlier:
                try:
                    if point_index == 0:
                        root.find('StrokeSet')[index].remove(root.find('StrokeSet')[index][point_index])
                    else:
                        root.find('StrokeSet')[index].remove(root.find('StrokeSet')[index][point_index + 1])
                except IndexError:
                    print("Failed to remove outlier in stroke: " + str(index))

    tree.write(file_name)


def get_quartiles(data):
    ordered_data = copy.copy(data)
    ordered_data.sort()

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


def mark_horizontal(file_name, indexes):

    tree = ElementTree.parse(file_name)
    root = tree.getroot()

    for i in range(len(root.find('StrokeSet'))):
        if i in indexes:
            root.find('StrokeSet')[i].attrib['Horizontal'] = "Yes"
        else:
            root.find('StrokeSet')[i].attrib['Horizontal'] = "No"

    tree.write(file_name)


def build_structure(file_name):
    with open(file_name, 'r') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        # text_lines = [text_line.attrib['text'] for text_line in root[1][1:]]

        strokes = []
        # StrokeSet tag stores the strokes in the xml
        for index in range(len(root.find('StrokeSet'))):
            strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])),
                             float(point.attrib['time'])) for point in root.find('StrokeSet')[index][:]])

    return strokes


def main():
    # remove_outlier_points('/home/patrik/strokesz.xml')
    pass


if __name__ == "__main__":
    main()
