import numpy as np
import func


def max_1_dim()


class Input:

    def __init__(self):
        self.output = None

    def propagate_forward(self, input_data, batch_size):
        self.output = input_data


class Dense:

    def __init__(self, units, input_dim=None, activation='linear'):

        self.input_dim = input_dim
        self.units = units

        self.activation = Activation(activation)

        if input_dim is not None:
            self.weights = np.random.random((input_dim + 1, units))
            self.dw = np.zeros(self.weights.shape)

        self.batch_size = None
        self.output = None

        self.dropout = None
        self.batch_normalization = None

    def propagate_forward(self, input_data, batch_size):
        data = np.ones((1, (self.input_dim+1)*batch_size))
        for index in range(len(input_data)):
            for feature_index in range(len(input_data/batch_size)):
                data[0, index * int((len(input_data)/batch_size)) + feature_index] = input_data[index][feature_index]

        self.output = self.activation.function(data, self.weights)

    def modify_weights(self, learning_rate, delta):
        self.weights -= learning_rate*np.dot(self.output.T, delta)

    def add(self, activation=None, dropout=None, batch_normalization=None):

        if activation is not None:
            self.activation = activation

        if dropout is not None:
            self.dropout = dropout

        if batch_normalization is not None:
            self.batch_normalization = batch_normalization


class Activation:

    def __init__(self, activation_function):
        self.activation_function = func.activations[activation_function][0]
        self.d_activation_function = func.activations[activation_function][1]

    def function(self, input_data, weights):
        return self.activation_function(np.dot(input_data, weights))

    def d_function(self, input_data, weights):
        return self.d_activation_function(np.dot(input_data, weights))


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
            self.layers[-1].add(activation=layer)

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

        data_set = np.array([(x_train[index], y_train[index]) for index in range(len(x_train))])

        for epoch in range(epochs):
            for index in range(batch_size, len(data_set), batch_size):

                deltas = []

                data = data_set[index-batch_size:index]
                input_data = data[:, 0]
                print(input_data)
                for layer in self.layers:
                    layer.propagate_forward(input_data, batch_size)
                    input_data = layer.output

                error = -(data[:, 1] - self.layers[-1].output)

                delta = np.multiply(error, self.layers[-1].activation.d_function(np.dot(self.layers[-2].output,
                                                                                        self.layers[-1].weights)))

                deltas.append(delta)
                for layer_index, layer in enumerate(self.layers[-2:0:-1]):
                    delta = np.dot(deltas[0], self.layers[layer_index + 1].weights.T) * \
                            layer.activation.d_function(np.dot(self.layers[layer_index - 1].output,
                                                                self.layers[layer_index].weights))
                    deltas.insert(0, delta)

                for layer_index, layer in enumerate(self.layers[1:]):
                    layer.modify_weights(deltas[layer_index-1], learning_rate=self.learning_rate)

                print("asd")

    def compile(self, loss, optimizer):
        pass

    def predict(self, batch):
        pass


def main():
    np.random.seed(1)
    model = Sequential()
    model.add(Dense(units=4, input_dim=2))
    model.add(Activation('relu'))
    model.add(Dense(units=5))
    model.fit(np.array([[1, 2], [2, 3], [4, 5]]), np.array([1, 3, 4]), batch_size=2)


if __name__ == "__main__":
    main()
