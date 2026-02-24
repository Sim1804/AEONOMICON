from audit.signal_detectors.stability_detector import StabilityDetector
from audit.signal_detectors.chaos_detector import ChaosDetector
from audit.signal_detectors.dominance_detector import DominanceDetector
from audit.signal_detectors.transition_detector import TransitionDetector

from audit.pattern_classifier.phenomenon_mapper import PhenomenonMapper
from audit.reports.suggestion_builder import SuggestionBuilder
from audit.taxonomy.v1.registry import TaxonomyRegistry


class AuditOrchestrator:

    def __init__(self):
        self.taxonomy = TaxonomyRegistry()
        self.mapper = PhenomenonMapper(self.taxonomy)
        self.suggestion_builder = SuggestionBuilder()

        self.stability = StabilityDetector()
        self.chaos = ChaosDetector()
        self.dominance = DominanceDetector()
        self.transition = TransitionDetector()

    def analyze(self, fork_trajectories, divergence_series,
                success_rates, regime_history):

        signals = {}

        signals.update(self.stability.detect(fork_trajectories))
        signals.update(self.chaos.detect(divergence_series))
        signals.update(self.dominance.detect(success_rates))
        signals.update(self.transition.detect(regime_history))

        phenomena = self.mapper.map_signals(signals)

        suggestions = self.suggestion_builder.build(phenomena, signals)

        return {
            "signals": signals,
            "phenomena": phenomena,
            "suggestions": suggestions
        }

