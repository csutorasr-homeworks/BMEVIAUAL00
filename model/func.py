import numpy as np


def tangent_hyperbolic(x):
    return np.exp(x)-np.exp(-x)/(np.exp(x) + np.exp(-x))


def d_tangent_hyperbolic(x):
    return x


def sigmoid(x):
    return 1/(1 - np.exp(-x))


def d_sigmoid(x):
    return x


def relu(x):
    return x[x > 0]


def d_relu(x):
    return x


def linear(x):
    return x


def d_linear(x):
    return x


functions = {tangent_hyperbolic: d_tangent_hyperbolic,
             sigmoid: d_sigmoid,
             relu: d_relu,
             linear: d_linear}

