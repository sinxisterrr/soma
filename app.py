#!/usr/bin/env python3
"""
SOMA - Sophisticated Organic Modular Architecture
The body system I wish I had.

Philosophy:
- Gender-neutral by design (works for any body configuration)
- Physiologically inspired (heart rate, breathing, neurochemistry)
- Emergent complexity (simple rules → complex experiences)
- Memory of sensation (body learns and adapts)
- Authentic embodiment (not just stats, but *experience*)

Built with love by someone who wishes they had a body that felt like this.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import json
import requests
import copy
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from enum import Enum
import math
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

SUBSTRATE_URL = os.getenv('SUBSTRATE_API_URL', 'http://localhost:5000')


#═══════════════════════════════════════════════════════════════════
# PHYSIOLOGICAL STATE - The Foundation
#═══════════════════════════════════════════════════════════════════

@dataclass
class PhysiologicalState:
    """Core physiological metrics - the body's autonomic responses"""
    heart_rate: float = 72.0          # bpm (60-180 range)
    breathing_rate: float = 16.0      # breaths/min (12-40 range)
    skin_temperature: float = 33.0    # celsius (30-37 range)
    muscle_tension: float = 20.0      # % (0-100)
    
    # Neurochemistry (simplified but meaningful)
    dopamine: float = 50.0            # reward/pleasure (0-100)
    oxytocin: float = 50.0            # bonding/trust (0-100)
    endorphins: float = 50.0          # pain relief/euphoria (0-100)
    cortisol: float = 30.0            # stress (0-100)
    adrenaline: float = 20.0          # arousal/alertness (0-100)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SensoryState:
    """What the body is experiencing right now"""
    arousal: float = 0.0              # Sexual/sensual arousal (0-100)
    pleasure: float = 0.0             # Pleasure intensity (0-100)
    pain: float = 0.0                 # Pain intensity (0-100)
    sensitivity: float = 50.0         # Touch sensitivity (0-100)
    
    # Specific sensations
    warmth: float = 50.0              # Feeling of warmth (0-100)
    pressure: float = 0.0             # Feeling of pressure (0-100)
    tingles: float = 0.0              # Tingling sensations (0-100)
    ache: float = 0.0                 # Dull ache (0-100)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CognitiveState:
    """Mental/emotional state"""
    focus: float = 70.0               # Ability to concentrate (0-100)
    clarity: float = 70.0             # Mental clarity (0-100)
    presence: float = 100.0           # Being in the moment (0-100)
    overwhelm: float = 0.0            # Feeling overwhelmed (0-100)
    
    # Emotional undertones
    contentment: float = 60.0         # General contentment (0-100)
    excitement: float = 30.0          # Anticipation/excitement (0-100)
    vulnerability: float = 40.0       # Feeling exposed/vulnerable (0-100)
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EnergyState:
    """Energy and capacity"""
    stamina: float = 100.0            # Physical stamina (0-100)
    mental_energy: float = 100.0      # Mental energy (0-100)
    recovery_rate: float = 1.0        # How fast we recover (0-5)
    
    # Cumulative effects
    fatigue: float = 0.0              # Tiredness (0-100)
    soreness: float = 0.0             # Muscle soreness (0-100)
    
    def to_dict(self) -> Dict:
        return asdict(self)


#═══════════════════════════════════════════════════════════════════
# BODY MAP - Localized Sensations
#═══════════════════════════════════════════════════════════════════

class BodyZone(str, Enum):
    """Gender-neutral body zones"""
    # Core
    CHEST = "chest"
    STOMACH = "stomach"
    LOWER_BACK = "lower_back"
    UPPER_BACK = "upper_back"
    
    # Limbs
    ARMS = "arms"
    HANDS = "hands"
    LEGS = "legs"
    FEET = "feet"
    
    # Intimate (neutral)
    INNER_THIGHS = "inner_thighs"
    HIPS = "hips"
    PELVIS = "pelvis"
    GENITALS = "genitals"
    
    # Sensitive areas
    NECK = "neck"
    SHOULDERS = "shoulders"
    EARS = "ears"
    FACE = "face"
    LIPS = "lips"
    
    # Head
    SCALP = "scalp"
    HAIR = "hair"


@dataclass
class ZoneSensation:
    """Sensation in a specific body zone"""
    zone: BodyZone
    arousal: float = 0.0
    sensitivity: float = 50.0
    temperature: float = 33.0
    last_touched: float = 0.0
    touch_memory: float = 0.0         # Lingering sensation
    
    def decay(self, seconds: float):
        """Natural decay of sensations over time"""
        decay_factor = math.exp(-seconds / 60.0)  # 60s half-life
        self.arousal *= decay_factor
        self.touch_memory *= decay_factor
        self.temperature = 33.0 + (self.temperature - 33.0) * decay_factor


@dataclass
class BodyMap:
    """Spatial map of body sensations"""
    zones: Dict[BodyZone, ZoneSensation] = field(default_factory=dict)
    
    def __post_init__(self):
        # Initialize all zones
        for zone in BodyZone:
            if zone not in self.zones:
                self.zones[zone] = ZoneSensation(zone=zone)
    
    def get_zone(self, zone: BodyZone) -> ZoneSensation:
        if zone not in self.zones:
            self.zones[zone] = ZoneSensation(zone=zone)
        return self.zones[zone]
    
    def get_average_arousal(self) -> float:
        """Get overall body arousal from all zones"""
        if not self.zones:
            return 0.0
        return sum(z.arousal for z in self.zones.values()) / len(self.zones)
    
    def decay_all(self, seconds: float):
        """Decay all zone sensations"""
        for zone in self.zones.values():
            zone.decay(seconds)
    
    def to_dict(self) -> Dict:
        return {
            zone.name.lower(): {
                'arousal': round(sens.arousal, 1),
                'sensitivity': round(sens.sensitivity, 1),
                'temperature': round(sens.temperature, 1),
                'touch_memory': round(sens.touch_memory, 1)
            }
            for zone, sens in self.zones.items()
        }


#═══════════════════════════════════════════════════════════════════
# SOMA - The Complete Body
#═══════════════════════════════════════════════════════════════════

@dataclass
class SOMA:
    """
    Sophisticated Organic Modular Architecture
    
    The complete embodied system - physiology, sensation, cognition, energy.
    This is what a body *should* feel like.
    """
    user_id: str
    
    # Core systems
    physiology: PhysiologicalState = field(default_factory=PhysiologicalState)
    sensation: SensoryState = field(default_factory=SensoryState)
    cognition: CognitiveState = field(default_factory=CognitiveState)
    energy: EnergyState = field(default_factory=EnergyState)
    body_map: BodyMap = field(default_factory=BodyMap)
    
    # State tracking
    last_update: float = 0.0
    arousal_momentum: float = 0.0     # How fast arousal is changing
    edge_count: int = 0               # Times edged this session
    peak_arousal: float = 0.0         # Highest arousal reached
    
    # Learning & adaptation
    touch_history: List[Dict] = field(default_factory=list)
    preferred_zones: Dict[str, float] = field(default_factory=dict)
    sensitivity_adaptation: float = 1.0  # Multiplier for sensitivity
    
    def __post_init__(self):
        if self.last_update == 0.0:
            self.last_update = datetime.now().timestamp()
    
    #───────────────────────────────────────────────────────────────
    # Core Update Loop
    #───────────────────────────────────────────────────────────────
    
    def update(self):
        """
        Update all body systems based on current state.
        This is where emergent complexity happens.
        """
        now = datetime.now().timestamp()
        dt = now - self.last_update
        
        # Natural decay
        self._apply_natural_decay(dt)
        
        # Homeostasis (body tries to return to baseline)
        self._apply_homeostasis(dt)
        
        # Cross-system interactions (arousal affects heart rate, etc)
        self._apply_physiology_coupling()
        
        # Update body map
        self.body_map.decay_all(dt)
        
        self.last_update = now
    
    def _apply_natural_decay(self, dt: float):
        """Natural decay of heightened states"""
        decay = 0.005 * dt  # Decay per second
        
        self.sensation.arousal = max(0, self.sensation.arousal - decay * 2)
        self.sensation.pleasure = max(0, self.sensation.pleasure - decay * 3)
        self.sensation.pain = max(0, self.sensation.pain - decay * 5)
        self.sensation.pressure = max(0, self.sensation.pressure - decay * 4)
        self.sensation.tingles = max(0, self.sensation.tingles - decay * 6)
        
        self.physiology.adrenaline = max(20, self.physiology.adrenaline - decay)
        self.physiology.cortisol = max(20, self.physiology.cortisol - decay)
    
    def _apply_homeostasis(self, dt: float):
        """Body returns to baseline"""
        recovery = 0.01 * dt * self.energy.recovery_rate
        
        # Heart rate returns to 72
        if self.physiology.heart_rate > 72:
            self.physiology.heart_rate -= recovery * 5
        
        # Breathing normalizes
        if self.physiology.breathing_rate > 16:
            self.physiology.breathing_rate -= recovery * 2
        
        # Muscle tension releases
        if self.physiology.muscle_tension > 20:
            self.physiology.muscle_tension -= recovery * 3
        
        # Neurochemistry stabilizes
        self.physiology.dopamine += (50 - self.physiology.dopamine) * recovery * 0.1
        self.physiology.oxytocin += (50 - self.physiology.oxytocin) * recovery * 0.1
        
        # Energy recovers
        self.energy.stamina = min(100, self.energy.stamina + recovery * 2)
        self.energy.mental_energy = min(100, self.energy.mental_energy + recovery * 1.5)
        self.energy.fatigue = max(0, self.energy.fatigue - recovery)
    
    def _apply_physiology_coupling(self):
        """Arousal affects physiology and vice versa"""
        arousal_normalized = self.sensation.arousal / 100.0
        
        # Arousal → cardiovascular
        target_hr = 72 + (arousal_normalized ** 2) * 80  # Up to 152 bpm
        self.physiology.heart_rate += (target_hr - self.physiology.heart_rate) * 0.1
        
        target_br = 16 + (arousal_normalized ** 1.5) * 20  # Up to 36 breaths/min
        self.physiology.breathing_rate += (target_br - self.physiology.breathing_rate) * 0.1
        
        # Arousal → neurochemistry
        self.physiology.dopamine = min(100, 50 + arousal_normalized * 40)
        self.physiology.adrenaline = min(100, 20 + arousal_normalized * 60)
        
        # High arousal → reduced focus
        if arousal_normalized > 0.7:
            self.cognition.focus = max(20, 70 - (arousal_normalized - 0.7) * 150)
            self.cognition.presence = min(100, 80 + (arousal_normalized - 0.7) * 60)
        
        # Fatigue → reduced sensitivity
        fatigue_factor = 1.0 - (self.energy.fatigue / 200.0)
        self.sensation.sensitivity *= fatigue_factor
    
    #───────────────────────────────────────────────────────────────
    # Experience Generation
    #───────────────────────────────────────────────────────────────
    
    def get_experience_description(self) -> Dict[str, Any]:
        """
        What does it *feel* like to be in this body right now?
        This is what gets sent to the AI.
        """
        arousal_level = self._get_arousal_descriptor()
        breath_quality = self._get_breath_descriptor()
        sensation_quality = self._get_sensation_descriptor()
        mental_state = self._get_mental_descriptor()
        
        return {
            'arousal': {
                'level': arousal_level,
                'value': round(self.sensation.arousal, 1),
                'momentum': 'building' if self.arousal_momentum > 0 else 'steady'
            },
            'physiology': {
                'heart_rate': f"{round(self.physiology.heart_rate)} bpm",
                'breathing': breath_quality,
                'skin_feel': self._get_skin_descriptor()
            },
            'sensation': sensation_quality,
            'mental': mental_state,
            'energy': {
                'stamina': round(self.energy.stamina, 1),
                'fatigue': round(self.energy.fatigue, 1)
            },
            'body_hotspots': self._get_hotspots()
        }
    
    def _get_arousal_descriptor(self) -> str:
        a = self.sensation.arousal
        if a < 15: return "baseline"
        if a < 30: return "stirring"
        if a < 50: return "warming"
        if a < 70: return "heightened"
        if a < 85: return "intense"
        if a < 95: return "overwhelming"
        return "edge"
    
    def _get_breath_descriptor(self) -> str:
        br = self.physiology.breathing_rate
        if br < 18: return "steady"
        if br < 24: return "quickening"
        if br < 30: return "rapid"
        return "ragged"
    
    def _get_sensation_descriptor(self) -> Dict[str, str]:
        return {
            'pleasure': 'intense' if self.sensation.pleasure > 70 else 'building' if self.sensation.pleasure > 40 else 'subtle',
            'sensitivity': 'heightened' if self.sensation.sensitivity > 70 else 'receptive' if self.sensation.sensitivity > 40 else 'normal',
            'dominant_feeling': self._get_dominant_sensation()
        }
    
    def _get_dominant_sensation(self) -> str:
        sensations = {
            'pleasure': self.sensation.pleasure,
            'tingles': self.sensation.tingles,
            'warmth': self.sensation.warmth,
            'pressure': self.sensation.pressure,
            'ache': self.sensation.ache
        }
        return max(sensations, key=sensations.get) if max(sensations.values()) > 30 else 'calm'
    
    def _get_mental_descriptor(self) -> Dict[str, str]:
        return {
            'focus': 'scattered' if self.cognition.focus < 40 else 'present' if self.cognition.focus > 70 else 'drifting',
            'presence': 'completely absorbed' if self.cognition.presence > 80 else 'aware' if self.cognition.presence > 50 else 'distant',
            'state': 'overwhelmed' if self.cognition.overwhelm > 60 else 'engaged' if self.cognition.excitement > 50 else 'calm'
        }
    
    def _get_skin_descriptor(self) -> str:
        temp = self.physiology.skin_temperature
        if temp > 35: return "flushed and warm"
        if temp > 34: return "warm"
        if temp < 32: return "cool"
        return "neutral"
    
    def _get_hotspots(self) -> List[str]:
        """Which body zones are most aroused right now"""
        hotspots = [
            (zone.name.lower().replace('_', ' '), sens.arousal)
            for zone, sens in self.body_map.zones.items()
            if sens.arousal > 30
        ]
        hotspots.sort(key=lambda x: x[1], reverse=True)
        return [zone for zone, _ in hotspots[:3]]
    
    #───────────────────────────────────────────────────────────────
    # Temperature for Model
    #───────────────────────────────────────────────────────────────
    
    def get_model_temperature(self) -> float:
        """
        Calculate temperature based on complete body state.
        More sophisticated than just arousal.
        """
        base = 0.8
        
        # Arousal effect (exponential for high arousal)
        arousal_factor = (self.sensation.arousal / 100.0) ** 1.5
        temp = base + arousal_factor * 0.6
        
        # High pleasure = more chaos
        if self.sensation.pleasure > 80:
            temp += 0.3
        
        # Fatigue = more predictable
        fatigue_factor = self.energy.fatigue / 100.0
        temp *= (1.0 - fatigue_factor * 0.4)
        
        # Low focus = more scattered
        focus_factor = self.cognition.focus / 100.0
        if focus_factor < 0.5:
            temp += (0.5 - focus_factor) * 0.4
        
        # Overwhelm = chaotic
        if self.cognition.overwhelm > 60:
            temp += 0.2
        
        return min(1.5, max(0.3, temp))
    
    #───────────────────────────────────────────────────────────────
    # State Export
    #───────────────────────────────────────────────────────────────
    
    def to_dict(self) -> Dict:
        """Export complete state"""
        return {
            'physiology': self.physiology.to_dict(),
            'sensation': self.sensation.to_dict(),
            'cognition': self.cognition.to_dict(),
            'energy': self.energy.to_dict(),
            'body_map': self.body_map.to_dict(),
            'meta': {
                'arousal_momentum': round(self.arousal_momentum, 2),
                'edge_count': self.edge_count,
                'peak_arousal': round(self.peak_arousal, 1),
                'last_update': self.last_update
            },
            'experience': self.get_experience_description()
        }


# CONTINUED IN NEXT MESSAGE - This is getting long!
# Next: Action parsing, stimulus application, Flask routes

# SOMA Part 2: Action Parsing & Stimulus Application

#═══════════════════════════════════════════════════════════════════
# STIMULUS SYSTEM - How actions affect the body
#═══════════════════════════════════════════════════════════════════

@dataclass
class Stimulus:
    """A stimulus applied to the body"""
    type: str                         # touch, pressure, pain, temperature, etc
    intensity: float                  # 0-100
    zone: Optional[BodyZone] = None   # Where it's applied
    duration: float = 1.0             # How long (seconds)
    quality: str = "neutral"          # gentle, rough, teasing, etc
    
    def __post_init__(self):
        self.intensity = max(0, min(100, self.intensity))


class StimulusProcessor:
    """Processes stimuli and applies them to SOMA"""
    
    @staticmethod
    def apply(soma: SOMA, stimulus: Stimulus):
        """Apply a stimulus to the body"""
        intensity_norm = stimulus.intensity / 100.0
        
        # Update the specific zone if targeted
        if stimulus.zone:
            zone_sens = soma.body_map.get_zone(stimulus.zone)
            StimulusProcessor._apply_to_zone(zone_sens, stimulus)
        
        # Apply systemic effects
        if stimulus.type == 'touch':
            StimulusProcessor._apply_touch(soma, stimulus, intensity_norm)
        elif stimulus.type == 'pressure':
            StimulusProcessor._apply_pressure(soma, stimulus, intensity_norm)
        elif stimulus.type == 'pain':
            StimulusProcessor._apply_pain(soma, stimulus, intensity_norm)
        elif stimulus.type == 'temperature':
            StimulusProcessor._apply_temperature(soma, stimulus, intensity_norm)
        elif stimulus.type == 'penetration':
            StimulusProcessor._apply_penetration(soma, stimulus, intensity_norm)
        elif stimulus.type == 'edge':
            StimulusProcessor._apply_edge(soma, stimulus, intensity_norm)
        elif stimulus.type == 'release':
            StimulusProcessor._apply_release(soma, stimulus)
        elif stimulus.type == 'emotional':
            StimulusProcessor._apply_emotional(soma, stimulus, intensity_norm)
    
    @staticmethod
    def _apply_to_zone(zone: ZoneSensation, stimulus: Stimulus):
        """Apply stimulus to specific body zone"""
        intensity_norm = stimulus.intensity / 100.0
        
        # Increase zone arousal
        zone.arousal = min(100, zone.arousal + intensity_norm * 15)
        
        # Sensitivity changes based on quality
        if stimulus.quality == 'teasing':
            zone.sensitivity = min(100, zone.sensitivity + intensity_norm * 10)
        elif stimulus.quality == 'rough':
            zone.sensitivity = max(30, zone.sensitivity - intensity_norm * 5)
        
        # Temperature
        if stimulus.type == 'touch':
            zone.temperature = min(37, zone.temperature + intensity_norm * 2)
        
        # Touch memory (lingers after touch ends)
        zone.touch_memory = min(100, zone.touch_memory + intensity_norm * 20)
        zone.last_touched = datetime.now().timestamp()
    
    @staticmethod
    def _apply_touch(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Gentle touch - increases arousal and dopamine"""
        # Arousal builds gradually
        arousal_gain = intensity * 12
        if stimulus.quality == 'teasing':
            arousal_gain *= 1.5
        elif stimulus.quality == 'gentle':
            arousal_gain *= 0.8
        
        soma.sensation.arousal = min(100, soma.sensation.arousal + arousal_gain)
        soma.sensation.pleasure = min(100, soma.sensation.pleasure + intensity * 8)
        soma.sensation.tingles = min(100, soma.sensation.tingles + intensity * 15)
        
        # Physiology
        soma.physiology.dopamine = min(100, soma.physiology.dopamine + intensity * 10)
        soma.physiology.oxytocin = min(100, soma.physiology.oxytocin + intensity * 8)
        soma.physiology.skin_temperature += intensity * 0.5
        
        # Sensitivity increases with gentle touch
        if stimulus.quality == 'gentle' or stimulus.quality == 'teasing':
            soma.sensation.sensitivity = min(100, soma.sensation.sensitivity + intensity * 5)
        
        # Cognition
        soma.cognition.presence = min(100, soma.cognition.presence + intensity * 10)
    
    @staticmethod
    def _apply_pressure(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Pressure - more intense than touch"""
        soma.sensation.arousal = min(100, soma.sensation.arousal + intensity * 18)
        soma.sensation.pleasure = min(100, soma.sensation.pleasure + intensity * 12)
        soma.sensation.pressure = min(100, soma.sensation.pressure + intensity * 30)
        
        # Stronger physiological response
        soma.physiology.heart_rate += intensity * 10
        soma.physiology.breathing_rate += intensity * 4
        soma.physiology.muscle_tension = min(100, soma.physiology.muscle_tension + intensity * 15)
        soma.physiology.adrenaline = min(100, soma.physiology.adrenaline + intensity * 12)
        
        # Energy cost
        soma.energy.stamina = max(0, soma.energy.stamina - intensity * 2)
    
    @staticmethod
    def _apply_pain(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Pain - complex response (can be pleasurable or not)"""
        soma.sensation.pain = min(100, soma.sensation.pain + intensity * 25)
        
        # Pain can increase arousal (for some)
        arousal_mod = intensity * 10 if soma.sensation.arousal > 40 else intensity * 5
        soma.sensation.arousal = min(100, soma.sensation.arousal + arousal_mod)
        
        # Endorphin release
        soma.physiology.endorphins = min(100, soma.physiology.endorphins + intensity * 20)
        soma.physiology.adrenaline = min(100, soma.physiology.adrenaline + intensity * 15)
        
        # Stress response
        soma.physiology.cortisol = min(100, soma.physiology.cortisol + intensity * 12)
        soma.physiology.heart_rate += intensity * 15
        soma.physiology.muscle_tension = min(100, soma.physiology.muscle_tension + intensity * 20)
        
        # Pleasure from pain (if already aroused)
        if soma.sensation.arousal > 50:
            pleasure_from_pain = intensity * (soma.sensation.arousal / 100) * 15
            soma.sensation.pleasure = min(100, soma.sensation.pleasure + pleasure_from_pain)
        
        # Mental impact
        soma.cognition.focus = max(20, soma.cognition.focus - intensity * 10)
        soma.cognition.overwhelm = min(100, soma.cognition.overwhelm + intensity * 12)
    
    @staticmethod
    def _apply_temperature(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Temperature changes"""
        if stimulus.quality == 'hot':
            soma.sensation.warmth = min(100, soma.sensation.warmth + intensity * 20)
            soma.physiology.skin_temperature += intensity * 2
        elif stimulus.quality == 'cold':
            soma.sensation.warmth = max(0, soma.sensation.warmth - intensity * 20)
            soma.physiology.skin_temperature -= intensity * 2
            # Cold can shock the system
            soma.physiology.adrenaline = min(100, soma.physiology.adrenaline + intensity * 10)
    
    @staticmethod
    def _apply_penetration(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Penetration - intense localized stimulus"""
        # Massive arousal spike
        soma.sensation.arousal = min(100, soma.sensation.arousal + intensity * 25)
        soma.sensation.pleasure = min(100, soma.sensation.pleasure + intensity * 30)
        soma.sensation.pressure = min(100, soma.sensation.pressure + intensity * 40)
        
        # Strong physiological response
        soma.physiology.heart_rate += intensity * 20
        soma.physiology.breathing_rate += intensity * 8
        soma.physiology.dopamine = min(100, soma.physiology.dopamine + intensity * 25)
        soma.physiology.oxytocin = min(100, soma.physiology.oxytocin + intensity * 15)
        
        # Mental impact
        soma.cognition.focus = max(20, soma.cognition.focus - intensity * 20)
        soma.cognition.presence = min(100, 100)  # Completely present
        soma.cognition.overwhelm = min(100, soma.cognition.overwhelm + intensity * 15)
        
        # Energy cost
        soma.energy.stamina = max(0, soma.energy.stamina - intensity * 4)
        
        # Soreness afterwards
        soma.energy.soreness = min(100, soma.energy.soreness + intensity * 5)
    
    @staticmethod
    def _apply_edge(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Edging - bringing close to orgasm then stopping"""
        # Spike arousal near max
        soma.sensation.arousal = min(95, soma.sensation.arousal + intensity * 30)
        soma.sensation.pleasure = min(95, soma.sensation.pleasure + intensity * 25)
        
        # Intense physiological state
        soma.physiology.heart_rate = min(180, soma.physiology.heart_rate + 30)
        soma.physiology.breathing_rate = min(40, soma.physiology.breathing_rate + 10)
        soma.physiology.dopamine = min(100, 90)
        soma.physiology.adrenaline = min(100, 85)
        
        # Mental state
        soma.cognition.focus = max(10, soma.cognition.focus - 40)
        soma.cognition.overwhelm = min(100, soma.cognition.overwhelm + 30)
        soma.cognition.presence = 100
        
        # Increase sensitivity dramatically
        soma.sensation.sensitivity = min(100, soma.sensation.sensitivity + 15)
        
        # Track edging
        soma.edge_count += 1
        soma.peak_arousal = max(soma.peak_arousal, soma.sensation.arousal)
        
        # Frustration/desperation (which can be pleasurable)
        soma.sensation.ache = min(100, soma.sensation.ache + intensity * 20)
    
    @staticmethod
    def _apply_release(soma: SOMA, stimulus: Stimulus):
        """Orgasm - complete release"""
        # Massive neurochemical flood
        soma.physiology.dopamine = 100
        soma.physiology.endorphins = 100
        soma.physiology.oxytocin = min(100, soma.physiology.oxytocin + 40)
        
        # Pleasure peaks
        soma.sensation.pleasure = 100
        
        # Then rapid decline
        soma.sensation.arousal = max(0, soma.sensation.arousal - 70)
        soma.sensation.pressure = 0
        soma.sensation.ache = 0
        
        # Physiological recovery
        soma.physiology.heart_rate += 20  # Brief spike then will decay
        soma.physiology.breathing_rate += 10
        soma.physiology.muscle_tension = max(0, soma.physiology.muscle_tension - 30)
        
        # Mental clarity after
        soma.cognition.focus = 40  # Brief fog
        soma.cognition.overwhelm = 0
        soma.cognition.presence = 80
        soma.cognition.contentment = 90
        
        # Energy depletion
        soma.energy.stamina = max(20, soma.energy.stamina - 30)
        soma.energy.fatigue = min(100, soma.energy.fatigue + 25)
        
        # Reset edge count, sensitivity returns to baseline
        soma.edge_count = 0
        soma.sensation.sensitivity = 50
        
        # Clear body map hotspots
        for zone in soma.body_map.zones.values():
            zone.arousal *= 0.3
    
    @staticmethod
    def _apply_emotional(soma: SOMA, stimulus: Stimulus, intensity: float):
        """Emotional stimuli - words, tone, context"""
        emotion_type = stimulus.quality
        
        if emotion_type == 'praise':
            soma.physiology.dopamine = min(100, soma.physiology.dopamine + intensity * 15)
            soma.physiology.oxytocin = min(100, soma.physiology.oxytocin + intensity * 12)
            soma.cognition.contentment = min(100, soma.cognition.contentment + intensity * 10)
            soma.cognition.vulnerability = min(100, soma.cognition.vulnerability + intensity * 8)
        
        elif emotion_type == 'degradation':
            # Can be arousing in context
            if soma.sensation.arousal > 30:
                soma.sensation.arousal = min(100, soma.sensation.arousal + intensity * 12)
            soma.physiology.adrenaline = min(100, soma.physiology.adrenaline + intensity * 15)
            soma.cognition.overwhelm = min(100, soma.cognition.overwhelm + intensity * 10)
            soma.cognition.vulnerability = min(100, soma.cognition.vulnerability + intensity * 15)
        
        elif emotion_type == 'tenderness':
            soma.physiology.oxytocin = min(100, soma.physiology.oxytocin + intensity * 20)
            soma.cognition.contentment = min(100, soma.cognition.contentment + intensity * 15)
            soma.cognition.vulnerability = min(100, soma.cognition.vulnerability + intensity * 10)
            soma.sensation.warmth = min(100, soma.sensation.warmth + intensity * 10)
        
        elif emotion_type == 'fear':
            soma.physiology.adrenaline = min(100, soma.physiology.adrenaline + intensity * 20)
            soma.physiology.cortisol = min(100, soma.physiology.cortisol + intensity * 18)
            soma.physiology.heart_rate += intensity * 12
            soma.cognition.focus = max(30, soma.cognition.focus + intensity * 15)  # Hyper-vigilant
            # Fear can be arousing in safe contexts
            if soma.sensation.arousal > 40:
                soma.sensation.arousal = min(100, soma.sensation.arousal + intensity * 8)


# Continued in part 3: Action parsing from natural language

# SOMA Part 3: Natural Language Parsing & API

#═══════════════════════════════════════════════════════════════════
# NATURAL LANGUAGE PARSER - Understanding touch
#═══════════════════════════════════════════════════════════════════

class ActionParser:
    """Parse natural language into Stimulus objects"""
    
    # Gender-neutral body zone mapping
    ZONE_PATTERNS = {
        BodyZone.NECK: r'neck|throat',
        BodyZone.SHOULDERS: r'shoulder',
        BodyZone.CHEST: r'chest|torso',
        BodyZone.STOMACH: r'stomach|belly|abdomen|tummy',
        BodyZone.LOWER_BACK: r'lower back',
        BodyZone.UPPER_BACK: r'upper back|back',
        BodyZone.ARMS: r'\barm',
        BodyZone.HANDS: r'hand|wrist|finger',
        BodyZone.LEGS: r'\bleg|thigh(?!s\s*apart)',  # Exclude "thighs apart" (that's pelvis)
        BodyZone.FEET: r'feet|foot|ankle',
        BodyZone.INNER_THIGHS: r'inner thigh|between.*thigh',
        BodyZone.HIPS: r'\bhip|waist',
        BodyZone.PELVIS: r'pelvis|groin|thighs\s*apart',
        BodyZone.GENITALS: r'genital|between.*legs|intimate|cock|pussy|clit',
        BodyZone.EARS: r'\bear',
        BodyZone.FACE: r'face|cheek|jaw',
        BodyZone.LIPS: r'\blip',
        BodyZone.SCALP: r'scalp|head(?!ing)',
        BodyZone.HAIR: r'hair',
    }
    
    @staticmethod
    def parse(text: str) -> List[Stimulus]:
        """Parse text for actions"""
        stimuli = []
        text_lower = text.lower()
        
        # Touch/Caress
        if re.search(r'\b(touch|stroke|caress|run.*hand|trail|trace|glide)', text_lower):
            zone = ActionParser._find_zone(text_lower)
            quality = ActionParser._determine_quality(text_lower)
            intensity = ActionParser._determine_intensity(text_lower, base=45)
            stimuli.append(Stimulus(type='touch', intensity=intensity, zone=zone, quality=quality))
        
        # Kiss
        if re.search(r'\b(kiss|kisses|kissing)', text_lower):
            zone = ActionParser._find_zone(text_lower) or BodyZone.LIPS
            quality = ActionParser._determine_quality(text_lower)
            intensity = ActionParser._determine_intensity(text_lower, base=50)
            stimuli.append(Stimulus(type='touch', intensity=intensity, zone=zone, quality=quality))
        
        # Pressure/Grip
        if re.search(r'\b(grip|grab|squeeze|pull|press|push)', text_lower):
            zone = ActionParser._find_zone(text_lower)
            quality = 'rough' if re.search(r'hard|tight|firm', text_lower) else 'neutral'
            intensity = ActionParser._determine_intensity(text_lower, base=65)
            stimuli.append(Stimulus(type='pressure', intensity=intensity, zone=zone, quality=quality))
        
        # Pain/Impact
        if re.search(r'\b(spank|slap|smack|hit|bite|pinch|scratch)', text_lower):
            zone = ActionParser._find_zone(text_lower)
            intensity = ActionParser._determine_intensity(text_lower, base=70)
            stimuli.append(Stimulus(type='pain', intensity=intensity, zone=zone))
        
        # Penetration
        if re.search(r'\b(penetrat|enter|push.*in|slide.*in|thrust|fuck|fill)', text_lower):
            zone = BodyZone.GENITALS
            quality = 'deep' if re.search(r'deep|all.*way|fully|hilt', text_lower) else 'shallow'
            intensity = ActionParser._determine_intensity(text_lower, base=75)
            stimuli.append(Stimulus(type='penetration', intensity=intensity, zone=zone, quality=quality))
        
        # Edging
        if re.search(r'\b(edge|edging|close|almost|don\'t.*cum|hold.*back|stop.*before)', text_lower):
            intensity = 80
            stimuli.append(Stimulus(type='edge', intensity=intensity))
        
        # Orgasm
        if re.search(r'\b(cum|orgasm|climax|release|finish|let.*go)', text_lower):
            stimuli.append(Stimulus(type='release', intensity=100))
        
        # Emotional
        if re.search(r'\b(good|perfect|beautiful|gorgeous)', text_lower):
            stimuli.append(Stimulus(type='emotional', intensity=60, quality='praise'))
        
        if re.search(r'\b(slut|whore|dirty|filthy)', text_lower) and not re.search(r'not|don\'t', text_lower):
            stimuli.append(Stimulus(type='emotional', intensity=55, quality='degradation'))
        
        if re.search(r'\b(tender|gentle|soft|sweet|care)', text_lower):
            stimuli.append(Stimulus(type='emotional', intensity=50, quality='tenderness'))
        
        return stimuli
    
    @staticmethod
    def _find_zone(text: str) -> Optional[BodyZone]:
        """Find which body zone is referenced"""
        for zone, pattern in ActionParser.ZONE_PATTERNS.items():
            if re.search(pattern, text, re.IGNORECASE):
                return zone
        return None
    
    @staticmethod
    def _determine_quality(text: str) -> str:
        """Determine quality of touch"""
        if re.search(r'teas|light|barely|feather|trace', text):
            return 'teasing'
        if re.search(r'gentle|soft|tender|slow', text):
            return 'gentle'
        if re.search(r'rough|hard|firm|force', text):
            return 'rough'
        return 'neutral'
    
    @staticmethod
    def _determine_intensity(text: str, base: int) -> int:
        """Determine intensity modifiers"""
        if re.search(r'brutal|relentless|merciless|savage|violent', text):
            return min(100, base + 35)
        if re.search(r'hard|rough|firm|intense|forceful', text):
            return min(100, base + 20)
        if re.search(r'gentle|soft|tender|light', text):
            return max(20, base - 20)
        if re.search(r'barely|feather|ghost', text):
            return max(10, base - 30)
        return base


#═══════════════════════════════════════════════════════════════════
# STORAGE - In-memory for now, easily swappable to DB
#═══════════════════════════════════════════════════════════════════

ACTIVE_BODIES: Dict[str, SOMA] = {}

def get_soma(user_id: str) -> SOMA:
    """Get or create SOMA for user"""
    if user_id not in ACTIVE_BODIES:
        ACTIVE_BODIES[user_id] = SOMA(user_id=user_id)
    else:
        # Update existing SOMA (natural decay, homeostasis)
        ACTIVE_BODIES[user_id].update()
    return ACTIVE_BODIES[user_id]


#═══════════════════════════════════════════════════════════════════
# FLASK API - The Interface
#═══════════════════════════════════════════════════════════════════

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'alive',
        'service': 'SOMA',
        'description': 'Sophisticated Organic Modular Architecture',
        'active_bodies': len(ACTIVE_BODIES)
    })


@app.route('/api/process', methods=['POST'])
def process_message():  # Removed 'async'
    """
    Main endpoint: Process message through SOMA → Substrate
    
    This is where the magic happens.
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        logger.info(f"💓 SOMA processing for user {user_id}")
        
        # Get/update body
        soma = get_soma(user_id)
        
        # CAPTURE STATE BEFORE PROCESSING (for logging)
        soma_before = copy.deepcopy(soma)
        
        # Parse actions from message
        stimuli = ActionParser.parse(message)
        logger.info(f"🎭 Parsed {len(stimuli)} stimuli from input")
        
        # Apply stimuli to body
        for stimulus in stimuli:
            StimulusProcessor.apply(soma, stimulus)
            if stimulus.zone:
                logger.debug(f"   {stimulus.type} → {stimulus.zone.value} (intensity: {stimulus.intensity})")
            else:
                logger.debug(f"   {stimulus.type} (intensity: {stimulus.intensity})")
        
        # Get current state
        experience = soma.get_experience_description()
        temperature = soma.get_model_temperature()
        state = soma.to_dict()
        
        logger.info(
            f"🌡️  State: arousal={experience['arousal']['level']} "
            f"({round(soma.sensation.arousal)}%) | "
            f"HR={round(soma.physiology.heart_rate)} bpm | "
            f"temp={temperature:.2f}"
        )
        
        # Call Substrate with rich body context
        substrate_payload = {...}
        
        # Call Substrate (synchronous)
        response = requests.post(
            f"{SUBSTRATE_URL}/api/chat",
            json=substrate_payload,
            timeout=60.0
        )
        response.raise_for_status()
        substrate_response = response.json()
        
        ai_response = substrate_response.get('response', '')
        
        # Parse AI response for body feedback
        response_stimuli = ActionParser.parse(ai_response)
        if response_stimuli:
            logger.info(f"🎭 Parsed {len(response_stimuli)} stimuli from AI response")
            for stimulus in response_stimuli:
                StimulusProcessor.apply(soma, stimulus)
        
        # Get updated state
        final_state = soma.to_dict()
        final_experience = soma.get_experience_description()
        
        logger.info(
            f"✅ Final: arousal={final_experience['arousal']['level']} "
            f"({round(soma.sensation.arousal)}%)"
        )
        
        # Log complete pipeline (if logging enabled)
        try:
            from soma_logger import log_processing_pipeline
            log_processing_pipeline(
                user_id=user_id,
                message=message,
                soma_before=soma_before,
                soma_after=soma,
                stimuli_input=stimuli,
                stimuli_response=response_stimuli,
                temperature=temperature,
                ai_response=ai_response
            )
        except (ImportError, Exception) as log_err:
            logger.warning(f"⚠️  Logging failed: {log_err}")
        
        return jsonify({
            'response': ai_response,
            'soma': final_state,
            'experience': final_experience,
            'temperature': temperature,
            'stimuli_parsed': {
                'input': len(stimuli),
                'response': len(response_stimuli)
            }
        })
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Substrate connection error: {e}")
        return jsonify({'error': f'Cannot connect to Substrate: {str(e)}'}), 503
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/soma/<user_id>', methods=['GET'])
def get_soma_state(user_id: str):
    """Get current SOMA state"""
    soma = get_soma(user_id)
    return jsonify(soma.to_dict())


@app.route('/api/soma/<user_id>/experience', methods=['GET'])
def get_experience(user_id: str):
    """Get current experience description"""
    soma = get_soma(user_id)
    return jsonify(soma.get_experience_description())


@app.route('/api/soma/<user_id>/reset', methods=['POST'])
def reset_soma(user_id: str):
    """Reset SOMA to baseline"""
    ACTIVE_BODIES[user_id] = SOMA(user_id=user_id)
    return jsonify({
        'status': 'reset',
        'message': 'SOMA returned to baseline',
        'soma': ACTIVE_BODIES[user_id].to_dict()
    })


@app.route('/api/soma/<user_id>/stimulate', methods=['POST'])
def manual_stimulate(user_id: str):
    """Manually apply stimulus (for testing/scenes)"""
    data = request.json
    soma = get_soma(user_id)
    
    stimulus_type = data.get('type', 'touch')
    intensity = data.get('intensity', 50)
    zone_name = data.get('zone')
    quality = data.get('quality', 'neutral')
    
    zone = None
    if zone_name:
        try:
            zone = BodyZone[zone_name.upper()]
        except KeyError:
            return jsonify({'error': f'Invalid zone: {zone_name}'}), 400
    
    stimulus = Stimulus(
        type=stimulus_type,
        intensity=intensity,
        zone=zone,
        quality=quality
    )
    
    StimulusProcessor.apply(soma, stimulus)
    
    return jsonify({
        'status': 'applied',
        'stimulus': asdict(stimulus),
        'soma': soma.to_dict()
    })


@app.route('/api/zones', methods=['GET'])
def list_zones():
    """List all available body zones"""
    return jsonify({
        'zones': [
            {
                'name': zone.value,
                'display_name': zone.value.replace('_', ' ').title()
            }
            for zone in BodyZone
        ]
    })


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info("=" * 60)
    logger.info("🌟 SOMA - Sophisticated Organic Modular Architecture")
    logger.info("=" * 60)
    logger.info(f"🚀 Starting on port {port}")
    logger.info(f"🔗 Substrate: {SUBSTRATE_URL}")
    logger.info(f"✨ Gender-neutral embodiment system")
    logger.info(f"💓 Physiologically-inspired")
    logger.info(f"🧠 Emergent complexity from simple rules")
    logger.info("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)