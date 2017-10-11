import xml.etree.ElementTree as ElementTree
import numpy as np
import math
import util
import sys
from keras.models import load_model
from sklearn import preprocessing


class Algorithm:
    """
    Collection of algorithms to calculate the handedness of the writer of the given text.
    For basic usage import ...
    """

    def __init__(self, file_name):
        self.model = load_model('right_left.h5')

        self.text_lines = []
        self.strokes = []
        self.h_line_indexes = []

        self.load_data(file_name)

    def load_data(self, file_name):
        """
        Loads the data from the xml, and calculates the horizontal lines.
        :param file_name: String, containing the absolute path of the file.
        :return:
        """
        try:
            file = open(file_name, 'r')

            tree = ElementTree.parse(file)
            root = tree.getroot()

            self.text_lines = [text_line.attrib['text'] for text_line in root[1][1:]]

            self.strokes = []
            # root[3] marks the StrokeSet tag in the xml.
            for i in range(len(root[3])):
                self.strokes.append([(util.Point(float(point.attrib['x']), float(point.attrib['y'])))
                                     for point in root[3][i][:]])

        except IOError as e:
            print('I/O error({0}): {1}.'.format(e.errno, e.strerror))

        self.h_line_indexes = self.predict(self.standardize_input(self.create_stroke_statistics()))

    @staticmethod
    def point_2_point(point_a, point_b):
        """
        Distance between two points.
        :param point_a: First point.
        :param point_b: Second point.
        :return: Distance of the points.
        """
        return math.sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)

    @staticmethod
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

    @staticmethod
    def calculate_angle(point_a, point_b):
        """
        Calculates the included angle (degrees) of a vector and horizontal line.
        :param point_a: First point of the vector.
        :param point_b: Second point.
        :return: The included angle (degrees) of the vector, defined by the points,
         and a horizontal line.
        """
        vector = util.Point(point_b.x - point_a.x, point_b.y - point_a.y)
        n_vector = util.Point(vector.x / vector.length, vector.y / vector.length)
        return math.degrees(math.acos(n_vector.x))

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
            if output[index] > 0.2:
                h_lines.append(index)

        return h_lines

    def get_horizontal_lines(self):
        return self.h_line_indexes

    def get_stroke_parameters(self, stroke):
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
                        stroke_length += self.point_2_point(stroke[index], stroke[index + 1])
                        avg_degree += math.fabs(self.calculate_angle(stroke[0], stroke[index + 1])) / (len(stroke) - 1)
                    if index in range(1, len(stroke) - 1):
                        # Average distance of the stroke's points from the line,
                        # that connects the first and the final point.
                        d_line_avg_distance += self.point_2_line(stroke[0], stroke[-1],
                                                                 stroke[index]) / (len(stroke) - 2)
                    if index in range(1, len(stroke)):
                        # Average distance of the stroke's points from the horizontal line,
                        # that goes through the first point.
                        h_line_avg_distance += \
                            self.point_2_line(stroke[0], util.Point(stroke[0].x + 1, stroke[0].y),
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

    @staticmethod
    def standardize_input(stat):
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
        """
        Calculates the handedness based on ...
        """
        line_dir = []
        for index in self.h_line_indexes:
            if self.strokes[int(index)][0].x < self.strokes[int(index)][-1].x:
                line_dir.append(False)
            else:
                line_dir.append(True)

        line_dir.count(True)

        # Todo


def main():
    alg = Algorithm(str(sys.argv[1]))
    print(alg.h_line_indexes)


if __name__ == "__main__":
    main()
