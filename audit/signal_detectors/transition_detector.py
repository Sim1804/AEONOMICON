from audit.analytics.regime_dynamics import analyze_regime_transitions


class TransitionDetector:
    def detect(self, regime_history):
        return analyze_regime_transitions(regime_history)

