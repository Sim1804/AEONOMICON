from typing import Dict
import math

class FieldMetrics:

    @staticmethod
    def _entropy(values):

        total = sum(abs(v) for v in values) + 1e-6
        probs = [abs(v) / total for v in values]

        entropy = -sum(p * math.log(p +1e-9) for p in probs)
        return entropy

    @staticmethod
    def compute_global_metrics(field_values: Dict[str, float]) -> Dict[str, float]:
        metrics = {}

        values = list(field_values.values())
        n = len(values)

        if n == 0:
            return metrics
        
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        std_dev = math.sqrt(variance)

        metrics["field_mean"] = mean
        metrics["field_variance"] = variance
        metrics["field_std_dev"] = std_dev

        metrics["field_energy"] = sum(abs(v) for v in values)
        metrics["field_instability"] = std_dev / (abs(mean) + 1e-6)

        metrics["field_entropy"] = FieldMetrics._entropy(values)

        return metrics
    
    @staticmethod
    def compute_field_specific_metrics(field_name: str, value: float, previous_value: float) -> Dict[str, float]:

        delta = value -previous_value

        return{
            "value": value,
            "delta": delta,
            "abs_delta": abs(delta),
            "direction": 1 if delta > 0 else -1 if delta < 0 else 0,
        }