import numpy as np
import func


class Input:

    def __init__(self):
        self.output = None
        self.bias = None

    def propagate_forward(self, input_data, batch_size):
        output = self.flatten(np.array(input_data)).\
            reshape(batch_size, int(len(self.flatten(np.array(input_data)))/batch_size))

        self.output = output
        if self.bias == 1 and batch_size > 1:
            self.output = np.ones((self.output.shape[0], self.output.shape[1]+1))
            for index in range(batch_size):
                self.output[index] = np.append(output[index], np.array([1]))
        elif self.bias == 1:
            self.output = np.append(self.output, np.array([1]))

    @staticmethod
    def flatten(data):
        flattened_data = []

        for features in data:
            for feature in features:
                flattened_data.append(feature)

        return np.array(flattened_data)


class Dense:

    def __init__(self, units, input_dim=None, activation='linear', bias=True):

        self.input_dim = input_dim
        self.units = units
        self.bias_enabled = bias
        self.last_layer = False
        self.bias = 1 if self.bias_enabled and not self.last_layer else 0

        self.activation = Activation(activation)

        self.weights = None
        self.dw = None
        if input_dim is not None:
            self.init_weights(self.input_dim, self.units)

        self.batch_size = None
        self.output = None

        self.dropout = None
        self.batch_normalization = None

    def init_weights(self, input_dim, output_dim):
        self.weights = np.random.random((input_dim + self.bias, output_dim))
        self.dw = np.zeros(self.weights.shape)

    def propagate_forward(self, input_data, batch_size):
        output = self.activation.function(input_data, self.weights)
        print(output)
        self.output = output
        if self.bias == 1 and batch_size > 1:
            self.output = np.ones((output.shape[0], output.shape[1]+1))
            for index in range(batch_size):
                self.output[index] = np.append(output[index], np.array([1]))
        elif self.bias == 1:
            self.output = np.append(output, np.array([1]))

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
            self.layers[0].bias = 1 if layer.bias_enabled else 0
            self.layers.append(layer)

        else:
            self.layers[-1].last_layer = False
            self.layers.append(Dense(units=layer.units, input_dim=self.layers[-1].units, bias=layer.bias))
            self.layers[-2].init_weights(self.layers[-2].input_dim, self.layers[-1].input_dim + self.layers[-1].bias)
            self.layers[-1].last_layer = True

    def fit(self, x_train, y_train, epochs=100, batch_size=32):

        data_set = np.array([(x_train[index], y_train[index]) for index in range(len(x_train))])

        for epoch in range(epochs):
            for index in range(batch_size, len(data_set), batch_size):

                deltas = []

                data = data_set[index-batch_size:index]
                input_data = data[:, 0]
                for layer in self.layers:
                    layer.propagate_forward(input_data, batch_size)
                    input_data = layer.output

                error = -(np.array(data[:, 1]).reshape(self.layers[-1].output.shape) - self.layers[-1].output)

                delta = np.multiply(error, self.layers[-1].activation.d_function(self.layers[-2].biased_output,
                                                                                        self.layers[-1].weights))

                deltas.append(delta)

                for layer_index in range(len(self.layers)-2, 0, -1):
                    print(np.dot(deltas[0], self.layers[layer_index + 1].weights.T).shape)
                    delta = np.dot(deltas[0], self.layers[layer_index + 1].weights.T) * \
                            self.layers[layer_index].activation.d_function(
                                self.layers[layer_index - 1].biased_output, self.layers[layer_index].weights)
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
    model.add(Dense(input_dim=2, units=4, bias=True))
    model.add(Activation('sigmoid'))
    model.add(Dense(units=1, bias=True))
    print(model.layers[1].weights)
    #model.fit(np.array([[1, 2], [2, 3], [4, 5]]), np.array([1, 3, 4]), batch_size=2)


if __name__ == "__main__":
    main()
