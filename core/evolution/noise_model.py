from enum import Enum
from typing import  Dict, Optional  

class NoiseType(Enum):
    GAUSSIAN = "gaussian"
    UNIFORM = "uniform"
    DRIFT = "drift"

class NoiseProfile:

    def __init__(self, noise_type: NoiseType, amplitude: float, enabled: bool = True, regime_sensitivity: Optional[float] = None, floor: Optional[float] = None, ceiling: Optional[float] = None):
        self.noise_type = noise_type
        self.amplitude = amplitude
        self.enabled = enabled
        self.regime_sensitivity = regime_sensitivity
        self.floor = floor
        self.ceiling = ceiling

class NoiseModel:

    def __init__(self, rng_manager):
        self._rng_manager = rng_manager

    def _gaussian_noise(self, field_name: str, amplitude: float, tick: int) -> float:
        
        value = self.rng.draw(
            intent_id="FIELD_NOISE_GAUSSIAN",
            stable_ids=[field_name],
            logical_tick=tick,
            consumption_index=0,
        )
        return amplitude * ( value - 0.5)
    
    def _uniform_noise(self, field_name: str, amplitude: float, tick: int) -> float:
        
        value = self.rng.draw(
            intent_id="FIELD_NOISE_UNIFORM",
            stable_ids=[field_name],
            logical_tick=tick,
            consumption_index=0,
        )
        return amplitude * (2.0 * value - 1.0)
    
    def _drift_noise(self, field_name: str, amplitude: float, tick: int) -> float:
        
        value = self.rng.draw(
            intent_id="FIELD_NOISE_FIELD",
            stable_ids=[field_name],
            logical_tick=tick // 10,
            consumption_index=0,
        )
        return amplitude * ( value - 0.5)
    
    
    def apply_noise(self, field_name: str, base_value: float, tick: int, noise_profile: NoiseProfile, context: Dict) -> float:
        if not noise_profile.enabled:
            return base_value

        regime_modifier = context.get("regime_modifier", 1.0)
        amplitude = noise_profile.amplitude

        if noise_profile.regime_sensitivity:
            amplitude *= regime_modifier 
        
        noise = self._compute_noise(
            field_name= field_name,
            noise_type = noise_profile.noise_type,
            amplitude=amplitude,
            tick=tick,
        )

        noisy_value = base_value + noise

        if noise_profile.floor is not None:
            noisy_value = max(noise_profile.floor, noisy_value)

        if noise_profile.ceiling is not None:
            noisy_value = min(noise_profile.ceiling, noisy_value)

        return noisy_value
    
    def _compute_noise(self, field_name: str, noise_type: NoiseType, amplitude: float, tick: int) -> float:

        if noise_type == NoiseType.GAUSSIAN:
            return self._gaussian_noise(field_name, amplitude, tick)
        
        elif noise_type == NoiseType.UNIFORM:
            return self._uniform_noise(field_name, amplitude, tick)
        
        elif noise_type == NoiseType.DRIFT:
            return self._drift_noise(field_name, amplitude, tick)
        
        return 0.0
    
