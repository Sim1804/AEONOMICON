class PhenomenonMapper:

    def __init__(self, taxonomy_registry):
        self.registry = taxonomy_registry

    def map_signals(self, signals):
        detected = []

        for mapping in self.registry.get_mappings():
            required = mapping["required_signals"]

            if all(signals.get(sig, False) for sig in required):
                detected.append(mapping["phenomenon"])

        return detected
