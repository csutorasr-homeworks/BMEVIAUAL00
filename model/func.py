import math
import numpy as np


def tangent_hyperbolic(x):
    return np.exp(x)-np.exp(-x)/(np.exp(x) + np.exp(-x))


def sigmoid(x):
    return 1/(1 - np.exp(-x))


def relu(x):
    return x[x > 0]
