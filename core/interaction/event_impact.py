from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from core.fields.field_base import FieldState

@dataclass(frozen=True)
class FieldPertubation:

    amplitude: float
    decay_rate: float
    direction: float

class EventImpactModel:

    def __init__(self):
        pass

    def apply(self, state: FieldState, pertubation: FieldPertubation, delta_t: float, context: Dict[str, Any],) -> FieldState:

        regime_modifier = context.get("regime_modifier", 1.0)

        effective_amplitude = (pertubation.amplitude * pertubation.direction * regime_modifier)

        decay = max(0.0, 1.0 - pertubation.decay_rate * delta_t)

        impulse = effective_amplitude * decay

        new_velocity = state.velocity + impulse
        new_velocity *= (1.0 - state.inertia)

        new_value = state.value + new_velocity * delta_t

        return FieldState(value=new_value, velocity=new_velocity, inertia=state.inertia)