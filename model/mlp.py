import numpy as np
import func


class Dense:

    def __init__(self, units, input_dim=None, activation=func.linear):

        self.input_dim = input_dim + 1
        self.units = units

        self.activation = Activation(activation)
        self.d_activation = func.functions[activation]

        self.weights = np.random.random((input_dim, units))
        self.dw = np.zeros(self.weights.shape)

        self.output = None

        self.dropout = None
        self.batch_normalization = None

    def propagate_forward(self, input_data):
        self.output = self.activation.function(input_data, self.weights)

    def modify_weights(self, learning_rate, delta):
        self.weights -= learning_rate*np.dot(self.output.T, delta)

    def add(self, activation=None, dropout=None, batch_normalization=None):

        if activation is not None:
            self.activation = activation
            self.d_activation = func.functions[activation]

        if dropout is not None:
            self.dropout = dropout

        if batch_normalization is not None:
            self.batch_normalization = batch_normalization


class Activation:

    def __init__(self, activation_function):
        self.activation_function = activation_function

    def function(self, input_data, weights):
        return self.activation_function(input_data*weights)


class Dropout:

    def __init__(self):
        pass


class BatchNorm:

    def __init__(self):
        pass


class Sequential:

    def __init__(self):
        self.layers = []

    def add(self, layer):

        if type(layer) is Activation:
            self.layers[-1].add(activation=layer)

        elif type(layer) is Dropout:
            self.layers[-1].add(dropout=layer)

        elif type(layer) is BatchNorm:
            self.layers[-1].add(batch_normalization=layer)

        else:
            self.layers.append(layer)

    def fit(self, x_train, y_train, epochs = 100, batch_size):

        deltas = []

        for epoch in epochs

        input_data =
        for layer in self.layers:
            layer.propagate_forward(input_data)
            input_data = layer.output



        for layer in self.layers[::-1]:
            pass

    def compile(self, loss, optimizer):
        pass

    def predict(self, batch):
        pass


def main():
    model = Sequential()
    model.add(Dense(units=4, input_dim=4))


if __name__ == "__main__":
    main()
