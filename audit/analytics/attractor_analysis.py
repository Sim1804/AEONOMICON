from .statistical_models import variance


def detect_attractor(fork_trajectories, threshold=0.01):
    """
    fork_trajectories: dict[fork_id] -> list of values
    """
    final_values = [traj[-1] for traj in fork_trajectories.values()]
    v = variance(final_values)

    return {
        "attractor_detected": v < threshold,
        "low_interfork_variance": v < threshold,
        "variance_value": v,
    }
