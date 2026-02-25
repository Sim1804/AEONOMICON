import numpy as np


class DriftDetector:
    """
    Detects slow, persistent, multi-field drifts,
    interpreted in the context of the current regime.
    """

    def __init__(
        self,
        min_window=30,
        slope_threshold=0.001,
        variance_max=0.05,
        min_fields_in_drift=2,
    ):
        self.min_window = min_window
        self.slope_threshold = slope_threshold
        self.variance_max = variance_max
        self.min_fields_in_drift = min_fields_in_drift

    def _analyze_series(self, series):
        """
        Analyze a single time series for drift characteristics.
        """
        window = np.array(series[-self.min_window:])
        x = np.arange(len(window))

        slope = float(np.polyfit(x, window, 1)[0])
        variance = float(np.var(window))

        return slope, variance

    def detect(
        self,
        field_series: dict,
        regime_id: str,
        event_series: list | None = None,
    ):
        """
        Parameters
        ----------
        field_series : dict[str, list[float]]
            Mapping field_id -> time series
        regime_id : str
            Current regime identifier
        event_series : list[bool] | None
            Significant events timeline

        Returns
        -------
        dict[str, bool | float | dict]
        """

        drifting_fields = {}
        analyzed = {}

        for field_id, series in field_series.items():
            if len(series) < self.min_window:
                continue

            slope, variance = self._analyze_series(series)
            analyzed[field_id] = {
                "slope": slope,
                "variance": variance,
            }

            if (
                abs(slope) > self.slope_threshold
                and variance < self.variance_max
            ):
                drifting_fields[field_id] = {
                    "slope": slope,
                    "variance": variance,
                }

        # Event decorrelation (optional but important)
        event_density = None
        if event_series and len(event_series) >= self.min_window:
            recent = event_series[-self.min_window:]
            event_density = sum(recent) / len(recent)

        multi_field_drift = len(drifting_fields) >= self.min_fields_in_drift

        # Regime-aware interpretation
        drift_significance = self._interpret_by_regime(
            regime_id,
            drifting_fields,
        )

        drift_detected = (
            multi_field_drift
            and drift_significance
            and (event_density is None or event_density < 0.2)
        )

        return {
            "drift_detected": drift_detected,
            "multi_field_drift": multi_field_drift,
            "drifting_fields": drifting_fields,
            "regime_sensitive": drift_significance,
            "event_density": event_density,
            "analyzed_fields": analyzed,
        }

    def _interpret_by_regime(self, regime_id, drifting_fields):
        """
        Interpret drift significance depending on regime.
        """

        if not drifting_fields:
            return False

        # Example regime interpretations (abstract, no lore)
        if regime_id in {"STABLE", "RIGID"}:
            # Drift here is suspicious
            return True

        if regime_id in {"TRANSITIONAL"}:
            # Drift is expected but only if mild
            return all(abs(v["slope"]) < self.slope_threshold * 5
                       for v in drifting_fields.values())

        if regime_id in {"CHAOTIC"}:
            # Drift is mostly noise here
            return False

        # Default conservative behavior
        return True