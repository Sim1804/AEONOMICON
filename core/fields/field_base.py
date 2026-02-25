from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class FieldState:
    value: float
    velocity: float
    inertia: float


class Field(ABC):
    def __init__(self, field_id: str, initial_state: FieldState):
        self._field_id = field_id
        self._state = initial_state

    @property
    def field_id(self)-> str:
        return self._field_id
    
    @property
    def state(self) -> FieldState:
        return self._state
    
    @property
    def value(self) -> float:
        return self._state.value
    
    @property
    def inertia(self) -> float:
        return self._state.inertia
    
    @property
    def velocity(self) -> float:
        return self._state.velocity
    

    @abstractmethod
    def evolve(self, delta_t: float, context: Dict[str, Any],)-> FieldState:
        raise NotImplementedError
    
    def apply_state(self, new_state: FieldState) -> None:
        self._state = new_state

    def export_metrics(self) -> Dict[str, float]:
        return { 
            "value": self.value,
            "velocity": self.velocity,
            "inertia": self.inertia
            }
    
    def __repr__(self)-> str:
        return ( 
            f"<Field id={self.field_id}"
            f"value ={self.value:.4f}"
            f"velocity ={self.velocity:.4f}"
            f"inertia ={self.inertia:.4f}"
                )