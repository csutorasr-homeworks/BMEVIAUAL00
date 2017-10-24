import numpy as np
import func


class Input:

    def __init__(self):
        self.output = None

    def propagate_forward(self, input_data):
        self.output = input_data


class Dense:

    def __init__(self, units, input_dim=None, activation='linear'):

        self.input_dim = input_dim
        self.units = units

        self.activation = func.functions[activation][0]
        self.d_activation = func.functions[activation][1]

        if input_dim is not None:
            self.weights = np.random.random((input_dim + 1, units))
            self.dw = np.zeros(self.weights.shape)

        self.output = None

        self.dropout = None
        self.batch_normalization = None

    def propagate_forward(self, input_data):
        data = np.ones((1, input_data+1))
        data[:-1] = input_data
        self.output = self.activation.function(data, self.weights)

    def modify_weights(self, learning_rate, delta):
        self.weights -= learning_rate*np.dot(self.output.T, delta)

    def add(self, activation=None, dropout=None, batch_normalization=None):

        if activation is not None:
            self.activation = func.functions[activation][0]
            self.d_activation = func.functions[activation][1]

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
        self.learning_rate = None

    def add(self, layer):

        if type(layer) is Activation:
            self.layers[-1].add(activation=layer.activation_function)

        elif type(layer) is Dropout:
            self.layers[-1].add(dropout=layer)

        elif type(layer) is BatchNorm:
            self.layers[-1].add(batch_normalization=layer)

        elif len(self.layers) == 0:
            self.layers.append(Input())
            self.layers.append(layer)

        else:
            self.layers.append(Dense(units=layer.units, input_dim=self.layers[-1].units))

    def fit(self, x_train, y_train, epochs=100, batch_size=32):

        data_set = [(x_train[index], y_train[index]) for index in range(len(x_train))]

        for epoch in range(epochs):

            for data_index, element in enumerate(data_set[::batch_size]):
                if data_index == 0:
                    continue

                deltas = []

                data = data_set[data_index-batch_size:data_index, 0]
                input_data = data[0]

                for layer in self.layers:
                    layer.propagate_forward(input_data)
                    input_data = layer.output

                error = -(data[1] - self.layers[-1].output)

                delta = np.multiply(error, self.layers[-1].d_activation(np.dot(self.layers[-2].output,
                                                                               self.layers[-1].weights)))
                deltas.append(delta)
                for layer_index, layer in enumerate(self.layers[-2::-1]):
                    delta = np.dot(deltas[0], layer.weights.T) * \
                            layer.d_activation(np.dot(self.layers[layer_index - 2].output,
                                                      self.layers[layer_index - 1].weights))
                    deltas.insert(0, delta)

                for layer_index, layer in enumerate(self.layers):
                    layer.modify_weights(deltas[layer_index], learning_rate=self.learning_rate)

    def compile(self, loss, optimizer):
        pass

    def predict(self, batch):
        pass


def main():
    model = Sequential()
    model.add(Dense(units=4, input_dim=4))
    model.add(Activation('relu'))
    model.add(Dense(units=5))
    print(model.layers)


if __name__ == "__main__":
    main()
