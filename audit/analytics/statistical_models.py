import numpy as np


def variance(series):
    return float(np.var(series))


def mean(series):
    return float(np.mean(series))


def second_derivative(series):
    if len(series) < 3:
        return 0.0
    return float(series[-1] - 2 * series[-2] + series[-3])


def lyapunov_approx(divergences):
    """
    Approximation simple du coefficient de Lyapunov.
    """
    if len(divergences) < 2:
        return 0.0

    ratios = []
    for i in range(1, len(divergences)):
        if divergences[i - 1] == 0:
            continue
        ratios.append(divergences[i] / divergences[i - 1])

    if not ratios:
        return 0.0

    return float(np.mean(np.log(np.abs(ratios))))
