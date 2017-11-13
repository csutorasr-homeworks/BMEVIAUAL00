import numpy as np
import math
import util
import xmlh
import sys
import os
from os.path import isfile, join
from keras.models import load_model
from sklearn import preprocessing


class Algorithm:
    """
    Collection of algorithms to calculate the handedness of the writer of the given text.
    For basic usage import ...
    """

    def __init__(self, file_name):
        self.model = load_model('right_left.h5')

        self.strokes = []
        self.h_line_indexes = []
        self.length = None
        self.file_name = file_name

        self.right_strokes = []

        self.load_data()

    def load_data(self):
        """
        Loads the data from the xml, and calculates the horizontal lines.
        :return:
        """
        try:
            self.strokes = xmlh.build_structure(self.file_name)

        except IOError as e:
            print('I/O error({0}): {1}.'.format(e.errno, e.strerror))

        self.h_line_indexes = self.predict(self.standardize_input(self.create_stroke_statistics()))

    def predict(self, stroke_params):
        """
        Predicts the horizontal lines, using the loaded model.
        :param stroke_params: Standardized n by 4 array of stroke parameters.
        :return: Indexes of the horizontal lines.
        """
        stroke_params = np.array(stroke_params)
        stroke_params = stroke_params.reshape(stroke_params.shape[0], stroke_params.shape[1])
        h_lines = []
        output = []
        for params in stroke_params:
            output.append(self.model.predict(np.array(params).reshape(-1, 4)))

        for index, stroke in enumerate(self.strokes):
            if output[index] > 0.2 and self.length[index] > 0.15:
                h_lines.append(index)

        return h_lines

    def get_horizontal_lines(self):
        return self.h_line_indexes

    @staticmethod
    def get_stroke_parameters(stroke):
        """
        Calculates the parameters of a stroke and concatenates it
        with the predetermined horizontal value.
        :param stroke: A single stroke of the text.
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
            return -1, -1, -1, 0

        else:
            for index in range(len(stroke)):
                try:
                    if index in range(0, len(stroke) - 1):
                        stroke_length += util.point_2_point(stroke[index], stroke[index + 1])
                        avg_degree += math.fabs(util.calculate_angle(stroke[0],
                                                                     stroke[index + 1])) / (len(stroke) - 1)
                    if index in range(1, len(stroke) - 1):
                        # Average distance of the stroke's points from the line,
                        # that connects the first and the final point.
                        d_line_avg_distance += util.point_2_line(stroke[0], stroke[-1],
                                                                 stroke[index]) / (len(stroke) - 2)
                    if index in range(1, len(stroke)):
                        # Average distance of the stroke's points from the horizontal line,
                        # that goes through the first point.
                        h_line_avg_distance += \
                            util.point_2_line(stroke[0], util.Point(stroke[0].x + 1, stroke[0].y),
                                              stroke[index]) / (len(stroke) - 1)

                except ZeroDivisionError:
                    # In case of division error, that occurs during the calculation of the angle
                    # (due to faulty xml data)
                    # ignore the point and move to the next.
                    pass

        return avg_degree, h_line_avg_distance, d_line_avg_distance, stroke_length

    def create_stroke_statistics(self):
        """
        Generates the parameter vector for each stroke.
        The strokes are stored in numpy array for each file.
        :return: An n by 4 array, containing stroke parameters per column.
        """
        length_sum = 0
        stroke_set = []
        for stroke_index, stroke in enumerate(self.strokes):
            params = self.get_stroke_parameters(stroke)
            length_sum += params[3]
            stroke_set.append(params)

        return np.array([(deg, h_dist, d_dist, length / (length_sum / len(self.strokes))) for
                         (deg, h_dist, d_dist, length) in stroke_set])

    def standardize_input(self, stat):
        """
        Standardizes the statistics.
        :param stat: An n by 4 matrix, that contains the stroke parameters per column.
        :return: The standardized input, that will be processed by the model.
        """

        # Dividing the parameters into separate lists for scaling.
        avg_degree = stat[:, 0].reshape(-1, 1)
        h_distance = stat[:, 1].reshape(-1, 1)
        d_distance = stat[:, 2].reshape(-1, 1)
        length = stat[:, 3].reshape(-1, 1)
        self.length = length

        # If the parameter is None due to faulty xml or outlying stroke length, it is necessary to
        # define them before scaling. To make sure these wont be classified as horizontal lines,
        # the highest values are given.
        avg_degree = np.array([np.nanmax(avg_degree) if deg is None else deg for deg in avg_degree])
        h_distance = np.array([np.nanmax(h_distance) if dist is None else dist for dist in h_distance])
        d_distance = np.array([np.nanmax(d_distance) if dist is None else dist for dist in d_distance])

        # Calculating mean average
        degree_scale = preprocessing.StandardScaler().fit(avg_degree)
        h_distance_scale = preprocessing.StandardScaler().fit(h_distance)
        d_distance_scale = preprocessing.StandardScaler().fit(d_distance)
        length_scale = preprocessing.StandardScaler().fit(length)

        # Transforming data
        avg_degree = degree_scale.transform(avg_degree)
        h_distance = h_distance_scale.transform(h_distance)
        d_distance = d_distance_scale.transform(d_distance)
        length = length_scale.transform(length)

        temp_array = np.array([avg_degree, h_distance, d_distance, length])
        std_input = []
        for i in range(temp_array.shape[1]):
            std_input.append(temp_array[:, i])

        return std_input

    def determine_handedness(self):
        line_dir = []

        for index in self.h_line_indexes:
            if self.strokes[int(index)][0].x < self.strokes[int(index)][-1].x:
                line_dir.append(False)
                self.right_strokes.append(index)
            else:
                line_dir.append(True)

        if line_dir.count(True) > 2:
            return "left"

        elif len(line_dir) <= 2:
            return "unknown"

        else:
            return "right"


def dump_predictions(root_dir):
    for file in os.listdir(root_dir):
        if isfile(join(root_dir, file)):
            alg = Algorithm(join(root_dir, file))
            xmlh.dump_results(join(root_dir, file), calculated_handedness=alg.determine_handedness())
            xmlh.mark_horizontal(join(root_dir, file), alg.get_horizontal_lines(), alg.right_strokes)
            print(join(root_dir, file) + "-Completed")

        else:
            dump_predictions(join(root_dir, file))


def main():
    dump_predictions(str(sys.argv[1]))


if __name__ == "__main__":
    main()
