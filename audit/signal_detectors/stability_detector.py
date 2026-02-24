from audit.analytics.attractor_analysis import detect_attractor


class StabilityDetector:
    def detect(self, fork_trajectories):
        return detect_attractor(fork_trajectories)
