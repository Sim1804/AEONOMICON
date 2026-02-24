import yaml
from pathlib import Path


class TaxonomyRegistry:

    def __init__(self):
        base = Path(__file__).parent
        self.phenomena = yaml.safe_load(open(base / "phenomena.yaml"))
        self.mapping = yaml.safe_load(open(base / "mapping_rules.yaml"))

    def get_mappings(self):
        return self.mapping["mappings"]
