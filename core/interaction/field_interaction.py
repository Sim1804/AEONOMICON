from enum import Enum
from typing import Any, Dict

class InteractionType(Enum):
    LINEAR = "linear"
    DAMPING = "damping"
    AMPLIFICATION = "amplification"
    SATURATION = "saturation"

class FieldInteraction:

    def __init__(self, source_field: str, target_field: str, interaction_type: InteractionType, strength:float, enabled:bool = True):

        self.source_field = source_field
        self.target_field = target_field
        self.interaction_type = interaction_type
        self.strength = strength
        self.enabled = enabled

    def compute_effect(self, source_value: float, target_value: float) -> float:
        if not self.enabled:
            return 0.0

        if self.interaction_type == InteractionType.LINEAR:
            return self.strength * source_value
        elif self.interaction_type == InteractionType.DAMPING:
            return -self.strength * source_value * target_value
        elif self.interaction_type == InteractionType.AMPLIFICATION:
            return self.strength * source_value * (1.0 - target_value)
        elif self.interaction_type == InteractionType.SATURATION:
            return self.strength * source_value * (1.0 - target_value)
        return 0.0
    
class InteractionRegistery:

    def __init__(self):
        self._interactions: list[FieldInteraction] = []
    
    def register(self, interaction: FieldInteraction):
        self._interactions.append(interaction)
    
    def get_for_target(self, target_field: str) -> list[FieldInteraction]:
        return [
            interaction for interaction in self._interactions 
            if interaction.target_field == target_field and interaction.enabled
            ]
    
    def all(self) -> list[FieldInteraction]:
        return self._interactions

class InteractionEngine:

    def __init__(self, registery: InteractionRegistery):
        self._registery = registery

    def compute_interaction_effect(self, field_values: Dict[str, float]) -> Dict[str, float]:

        deltas: Dict[str, float] = {name: 0.0 for name in field_values.keys()}

        for interaction in self._registery.all():
            source = interaction.source_field
            target = interaction.target_field

            if source in field_values and target in field_values:
                continue

            source_value = field_values[source]
            target_value = field_values[target]

            effect = interaction.compute_effect(source_value, target_value)
            deltas[target] += effect
        return deltas