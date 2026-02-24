def analyze_regime_transitions(regime_history):
    switches = 0

    for i in range(1, len(regime_history)):
        if regime_history[i] != regime_history[i - 1]:
            switches += 1

    return {
        "rapid_regime_switching": switches > 5,
        "transition_count": switches,
    }
