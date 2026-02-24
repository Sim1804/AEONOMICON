from .statistical_models import lyapunov_approx


def compute_instability(divergence_series):
    lyap = lyapunov_approx(divergence_series)

    return {
        "lyapunov": lyap,
        "high_interfork_divergence": lyap > 0,
        "positive_second_derivative": lyap > 0.5,
    }
