import numpy as np


class Dense:

    def __init__(self, input_dim, units, activation=None):
        self.input_dim = input_dim
        self.units = units
        self.activation = activation
        self.weights = np.random.random((input_dim, units))

    def output(self):
        self.activation.forward_prop()


class Activation:

    def __init__(self):
        pass

    def forward_prop(self, ):


class Sequential:

    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def fit(self, x_train, y_train, epochs, batch_size):
        pass

    def compile(self, loss, optimizer, ):
        pass

    def predict(self, batch):
        pass