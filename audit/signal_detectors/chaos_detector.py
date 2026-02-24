from audit.analytics.instability_metrics import compute_instability


class ChaosDetector:
    def detect(self, divergence_series):
        return compute_instability(divergence_series)
