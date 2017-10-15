import xml.etree.ElementTree as ElementTree
import util


def clear_xml(file_name):
    strokes = build_structure(file_name)

    for index in range(len(strokes)):
        for point_index in range(len(strokes[index][:-1])):
            pass

    with open(file_name, 'a') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()
        for index in range(len(root.find('StrokeSet'))):
            for point_index in range(len(root.find('StrokeSet')[index][:-1])):
                pass


def mark_horizontal(file_name, indexes):
    file = open(file_name, 'a')

    tree = ElementTree.parse(file)
    root = tree.getroot()

    tree.write(file)
    # Todo


def build_structure(file_name):
    with open(file_name, 'r') as file:
        tree = ElementTree.parse(file)
        root = tree.getroot()

        # text_lines = [text_line.attrib['text'] for text_line in root[1][1:]]

        strokes = []
        # StrokeSet tag stores the strokes in the xml
        for index in range(len(root.find('StrokeSet'))):
            strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])),
                             point.attrib['time']) for point in root.find('StrokeSet')[index][:]])

    return strokes


def main():
    pass


if __name__ == "__main__":
    main()
