from audit.analytics.dominance_metrics import dominance_score


class DominanceDetector:
    def detect(self, structure_success_rates):
        score = dominance_score(structure_success_rates)
        return {
            "dominance_score_high": score > 1.5,
            "dominance_value": score,
        }

