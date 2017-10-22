import numpy as np


class Dense:

    def __init__(self, units, input_dim=None, activation=None):
        self.input_dim = input_dim + 1
        self.units = units
        self.activation = activation
        self.weights = np.random.random((input_dim, units))
        self.dw = np.zeros(self.weights.shape)

    def output(self, input_data):
        return self.activation.function(input_data, self.weights)

    def modify_weights(self, learning_rate, delta):
        self.weights += learning_rate*delta

    def propagate_backward(self):
        pass


class Activation:

    def __init__(self, activation_function):
        self.activation_function = activation_function

    def function(self, input_data, weights):
        return self.activation_function(input_data*weights)


class Dropout:

    def __init__(self):
        pass


class Sequential:

    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def fit(self, x_train, y_train, epochs, batch_size):
        pass

    def compile(self, loss, optimizer):
        pass

    def predict(self, batch):
        pass
