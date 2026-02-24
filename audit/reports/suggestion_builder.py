class SuggestionBuilder:

    def build(self, phenomena, signals):
        suggestions = []

        for phenomenon in phenomena:
            suggestions.append({
                "phenomenon": phenomenon,
                "confidence": self._compute_confidence(signals),
                "details": signals
            })

        return suggestions

    def _compute_confidence(self, signals):
        true_count = sum(1 for v in signals.values() if v is True)
        total = len(signals)
        return true_count / total if total else 0.0

