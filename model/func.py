import numpy as np


def tangent_hyperbolic(x):
    return np.exp(x)-np.exp(-x)/(np.exp(x) + np.exp(-x))


def d_tangent_hyperbolic(x):
    return x


def sigmoid(x):
    return 1/(1 + np.exp(-x))


def d_sigmoid(x):
    np.exp(-x)/(1 + np.exp(-x))**2


def relu(x):
    return x[x > 0]


def d_relu(x):
    return 1 if x > 0 else 0


def linear(x):
    return x


def d_linear(x):
    return 1


functions = {'tanh': (tangent_hyperbolic, d_tangent_hyperbolic),
             'sigmoid': (sigmoid, d_sigmoid),
             'relu': (relu, d_relu),
             'linear': (linear, d_linear)}

