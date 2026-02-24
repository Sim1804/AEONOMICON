import numpy as np


class DriftDetector:
    """
    Detects slow, persistent, non-event-driven drifts
    in global fields or metrics.
    """

    def __init__(
        self,
        min_window=20,
        slope_threshold=0.001,
        variance_max=0.05,
    ):
        self.min_window = min_window
        self.slope_threshold = slope_threshold
        self.variance_max = variance_max

    def detect(self, time_series, event_series=None):
        """
        Parameters
        ----------
        time_series : list[float]
            Values of a field or metric over time (ordered).
        event_series : list[bool] | None
            Whether a significant event occurred at each timestep.

        Returns
        -------
        dict[str, bool | float]
        """

        if len(time_series) < self.min_window:
            return {"drift_detected": False}

        window = np.array(time_series[-self.min_window:])
        x = np.arange(len(window))

        # Linear regression slope
        slope = np.polyfit(x, window, 1)[0]
        variance = float(np.var(window))

        # Event decorrelation
        event_density = None
        if event_series:
            recent_events = event_series[-self.min_window:]
            event_density = sum(recent_events) / len(recent_events)

        drift = (
            abs(slope) > self.slope_threshold
            and variance < self.variance_max
            and (event_density is None or event_density < 0.2)
        )

        return {
            "drift_detected": drift,
            "drift_slope": float(slope),
            "drift_variance": variance,
            "event_density": event_density,
        }
