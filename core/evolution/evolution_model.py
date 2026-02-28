from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any

from core.fields.field_base import FieldState

class EvolutionModel(ABC):

    @abstractmethod
    def step(self, state: FieldState, delta_t: float, context: Dict[str, Any],) -> FieldState:

       raise NotImplementedError

class RelaxationEvolution(EvolutionModel):

    def __init__(self, equilibrium: float, stiffness: float):
        self._equilibrium = equilibrium
        self._stiffness = stiffness

    def step(self, state: FieldState, delta_t: float, context: Dict[str, Any],) -> FieldState:
        displacement = self._equilibrium - state.value

        acceleration = self._stiffness * displacement
        new_velocity = state.velocity + acceleration * delta_t
        new_velocity *= (1.0 - state.inertia)

        new_value = state.value + new_velocity * delta_t

        return FieldState(value=new_value, velocity=new_velocity, inertia=state.inertia)
    
class InertiaDriftEvolution(EvolutionModel):

    def __init__(self, drift_strenght: float, damping: float):
        self._drift_strenght = drift_strenght
        self._damping = damping

    def step(self, state: FieldState, delta_t: float, context: Dict[str, Any],) -> FieldState:
        drift_force = self._drift_strenght * (1.0 - state.inertia)
        damping_force = self._damping * state.velocity

        acceleration = drift_force + damping_force
        new_velocity = state.velocity + acceleration * delta_t
        new_value = state.value + new_velocity * delta_t

        return FieldState(value=new_value, velocity=new_velocity, inertia=state.inertia)
    
class RegimeAwareEvolution(EvolutionModel):

    def __init__(self, base_model: EvolutionModel):
        self._base_model = base_model
    
    def step(self, state: FieldState, delta_t: float, context: Dict[str, Any],) -> FieldState:
        regime_modifier = context.get(" regime_modifier", 1.0)

        adjusted_delta_t = delta_t * regime_modifier

        return self._base_model.step(
            state=state,
            delta_t=adjusted_delta_t,
            context=context,
        )