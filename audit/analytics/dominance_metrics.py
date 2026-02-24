import numpy as np


def dominance_score(structure_success_rates):
    """
    structure_success_rates: dict[str] -> float
    """
    values = np.array(list(structure_success_rates.values()))
    if len(values) == 0:
        return 0.0

    max_val = np.max(values)
    mean_val = np.mean(values)

    if mean_val == 0:
        return 0.0

    return float(max_val / mean_val)
