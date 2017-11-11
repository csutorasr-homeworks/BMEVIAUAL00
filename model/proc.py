from os.path import isdir, join
import xml.etree.ElementTree as ElementTree
import numpy as np
import os
import math
import util
import copy
import pickle

#
# Data variable contains the set of strokes, for each xml file.
# The structure of the list:
# data[] --> list of xml files
# data[][] --> list of strokes
# data[][][] --> list of points
#
data = []

#
# Horizontal_strokes variable contains the predetermined horizontal values.
# The structure of the list:
# horizontal_strokes[] --> list of xml files
# horizontal_strokes[][] --> list of stroke indexes (strokes that were determined to be horizontal)
#
horizontal_strokes = []


def get_stroke_parameters(stroke, file_index, stroke_index):
    """
    Calculates the parameters of a stroke and concatenates it with the predetermined horizontal value.
    :param stroke: A single stroke of the text.
    :param file_index: The index of the file, which contains the currently processed stroke.
    :param stroke_index: The index of the stroke in the StrokeSet.
    :return: The calculated parameters of the stroke. The values are Nan,
         if the stroke is too short.
    """
    h_line_avg_distance = 0
    d_line_avg_distance = 0
    stroke_length = 0
    avg_degree = 0
    # In case of comas, dots, or xml errors the stroke is marked with null values, and will be removed from the
    # training data in the next processing step.
    if len(stroke) == 0 or len(stroke) == 1 or len(stroke) == 2:
        return None, None, None, 0, None

    else:
        for index in range(len(stroke)):
            try:
                if index in range(0, len(stroke)-1):
                    stroke_length += util.point_2_point(stroke[index], stroke[index+1])
                    avg_degree += math.fabs(util.calculate_angle(stroke[0], stroke[index+1])) / (len(stroke)-1)
                if index in range(1, len(stroke)-1):
                    # Average distance of the stroke's points from the line,
                    # that connects the first and the final point.
                    d_line_avg_distance += util.point_2_line(stroke[0], stroke[-1], stroke[index]) / (len(stroke)-2)
                if index in range(1, len(stroke)):
                    # Average distance of the stroke's points from the horizontal line,
                    # that goes through the first point.
                    h_line_avg_distance += util.point_2_line(stroke[0], util.Point(stroke[0].x + 1, stroke[0].y),
                                                             stroke[index])/(len(stroke)-1)

            except ZeroDivisionError:
                # In case of division error, that occurs during the calculation of the angle (due to faulty xml data)
                # ignore the point and move to the next.
                pass

    if stroke_index == 13:
        print(avg_degree, h_line_avg_distance, d_line_avg_distance, stroke_length, is_horizontal(file_index, stroke_index), file_index)

    return avg_degree, h_line_avg_distance, d_line_avg_distance, stroke_length, is_horizontal(file_index, stroke_index)


def parse_files(location):
    """
    Iterates through the Data directory and gathers the strokes from all of the xml files.
    :param location: String, contains the root directory of the xml files.
    """
    loc = copy.copy(location)
    content = os.listdir(loc)

    # Iteration into the deepest directory layer through recursive calls.
    if len([file for file in content if isdir(join(loc, str(file)))]) == 0:
        for f in content:
            try:
                tree = ElementTree.parse(join(loc, str(f)))
                root = tree.getroot()
                strokes = []
                # root[3] marks the StrokeSet tag of the xml, which contains the list of strokes.
                # Each stroke has a set of x,y coordinates that describe the curve.
                for stroke in root.find('StrokeSet'):
                    strokes.append([(util.Point(float(point.attrib['x']),
                                                float(point.attrib['y']))) for point in stroke])
                data.append(strokes)

            except IOError as e:
                print('I/O error({0}): {1}.'.format(e.errno, e.strerror))

    else:
        for d in content:
            parse_files(join(loc, str(d)))


def create_stroke_statistics():
    """
    Generates the parameter vector for each stroke.
    The strokes are stored in numpy array for each file.
    :return: Stroke statistic as an n by 5 array.
    """
    files = []
    for file_index, strokes in enumerate(data):
        stroke_set = []
        length_sum = 0
        for stroke_index, stroke in enumerate(strokes):
            params = get_stroke_parameters(stroke, file_index, stroke_index)
            length_sum += params[3]
            stroke_set.append(params)

        files.append(np.array([(deg, h_dist, d_dist, length/(length_sum/len(strokes)), is_h)
                               for (deg, h_dist, d_dist, length, is_h) in stroke_set]))

    return files


def clear_faulty_data(files):
    """
    Removes the None rows from the generated stroke statistics.
    :param files: An n by 5 array containing stroke statistics,
     with possibility of several Nan rows.
    :return: The same array, without the Nan rows.
    """
    corrected_files = []
    for file in files:
        corrected_files.append([stroke for stroke in file if None not in stroke])

    return corrected_files


def is_horizontal(file_index, stroke_index):
    """
    Helper function for retrieving the predetermined horizontal value.
    :param file_index: The index of the file that contains the currently examined stroke.
    :param stroke_index: The index of the stroke in the currently processed StrokeSet.
    :return: 1, if the stroke has been determined to be horizontal by the manual examination,
     otherwise 0.
    """
    if stroke_index in horizontal_strokes[file_index]:
        return 1
    else:
        return 0


def save_statistics(location, stat):
    """
    Serializes the stroke statistics using the pickle method.
    :param location: Location of the created stroke statistics' save file.
    :param stat: The created statistics.
    :return:
    """
    pickle.dump(stat, open(location, 'wb'))


def load_marked_strokes(location):
    """
    Loads the predetermined horizontal values.
    :param location: The absolute path of the file, containing the output of the manual examination
     of the sample xml files.
    :return:
    """
    f = open(location, 'r')
    files = str(f.read()).split('\n')
    for strokes in files:
        horizontal_strokes.append(np.array([int(stroke) for stroke in strokes.split(' ')], dtype='int'))


def main():

    parse_files('/media/patrik/1EDB65B8599DD93E/Data/Erika/TestData')
    load_marked_strokes('hstrokes.txt')
    save_statistics('stat', np.array(clear_faulty_data(create_stroke_statistics())))


if __name__ == "__main__":
    main()
