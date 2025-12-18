#!/usr/bin/env python3
"""
SOMA Event Logger
Beautiful, detailed logging of everything happening in the body system
"""

import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class SOMALogger:
    """
    Comprehensive logging system for SOMA.
    Logs everything happening to the body in a beautiful, readable format.
    """
    
    def __init__(self, log_file: str = "logs/soma_events.log"):
        """Initialize logger"""
        # Create logs directory
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Configure file logger
        self.file_logger = logging.getLogger('soma_events')
        self.file_logger.setLevel(logging.INFO)
        
        # File handler with detailed formatting
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler with colored output
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Format: timestamp | level | message
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.file_logger.addHandler(file_handler)
        self.file_logger.addHandler(console_handler)
        
        # Session tracking
        self.current_session = None
        self.event_count = 0
    
    def start_session(self, user_id: str, message: str):
        """Log start of a processing session"""
        self.current_session = {
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'message': message[:100]  # First 100 chars
        }
        self.event_count = 0
        
        self.file_logger.info("="*80)
        self.file_logger.info(f"🌟 NEW SESSION: {user_id}")
        self.file_logger.info(f"📝 Message: {message[:100]}...")
        self.file_logger.info("="*80)
    
    def log_stimulus_parsed(self, stimulus: Any):
        """Log when a stimulus is parsed from text"""
        self.event_count += 1
        
        zone_info = f" → {stimulus.zone.value}" if stimulus.zone else ""
        quality_info = f" ({stimulus.quality})" if hasattr(stimulus, 'quality') and stimulus.quality != 'neutral' else ""
        
        self.file_logger.info(
            f"🎭 [{self.event_count:02d}] Stimulus Parsed: "
            f"{stimulus.type.upper()}{zone_info} "
            f"[intensity: {stimulus.intensity:.0f}%]{quality_info}"
        )
    
    def log_state_before(self, soma: Any):
        """Log body state before stimulus application"""
        self.file_logger.info(
            f"📊 State BEFORE: "
            f"Arousal={soma.sensation.arousal:.1f}% | "
            f"HR={soma.physiology.heart_rate:.0f}bpm | "
            f"Pleasure={soma.sensation.pleasure:.1f}% | "
            f"Sensitivity={soma.sensation.sensitivity:.1f}%"
        )
    
    def log_state_after(self, soma: Any):
        """Log body state after stimulus application"""
        exp = soma.get_experience_description()
        
        self.file_logger.info(
            f"📈 State AFTER:  "
            f"Arousal={soma.sensation.arousal:.1f}% ({exp['arousal']['level']}) | "
            f"HR={soma.physiology.heart_rate:.0f}bpm | "
            f"Pleasure={soma.sensation.pleasure:.1f}% | "
            f"Breath={exp['physiology']['breathing']}"
        )
        
        # Log hotspots if any
        if exp.get('body_hotspots'):
            hotspots = ", ".join(exp['body_hotspots'])
            self.file_logger.info(f"🔥 Hotspots: {hotspots}")
    
    def log_zone_change(self, zone_name: str, before_arousal: float, after_arousal: float):
        """Log changes to specific body zone"""
        change = after_arousal - before_arousal
        arrow = "↑" if change > 0 else "↓"
        
        self.file_logger.info(
            f"   └─ {zone_name}: {before_arousal:.1f}% → {after_arousal:.1f}% "
            f"({arrow}{abs(change):.1f}%)"
        )
    
    def log_physiology_change(self, soma: Any, before: Dict):
        """Log significant physiological changes"""
        hr_change = soma.physiology.heart_rate - before['heart_rate']
        br_change = soma.physiology.breathing_rate - before['breathing_rate']
        
        if abs(hr_change) > 5:
            arrow = "↑" if hr_change > 0 else "↓"
            self.file_logger.info(
                f"💓 Heart Rate: {before['heart_rate']:.0f} → {soma.physiology.heart_rate:.0f} bpm "
                f"({arrow}{abs(hr_change):.0f})"
            )
        
        if abs(br_change) > 2:
            arrow = "↑" if br_change > 0 else "↓"
            self.file_logger.info(
                f"🫁 Breathing: {before['breathing_rate']:.0f} → {soma.physiology.breathing_rate:.0f} breaths/min "
                f"({arrow}{abs(br_change):.0f})"
            )
    
    def log_neurochemistry(self, soma: Any):
        """Log neurochemistry state"""
        self.file_logger.info(
            f"🧪 Neurochemistry: "
            f"Dopamine={soma.physiology.dopamine:.0f}% | "
            f"Oxytocin={soma.physiology.oxytocin:.0f}% | "
            f"Endorphins={soma.physiology.endorphins:.0f}% | "
            f"Adrenaline={soma.physiology.adrenaline:.0f}%"
        )
    
    def log_temperature(self, temp: float, reason: str = ""):
        """Log model temperature calculation"""
        temp_emoji = "🌡️" if temp < 1.0 else "🔥" if temp > 1.2 else "🌡️"
        reason_text = f" ({reason})" if reason else ""
        
        self.file_logger.info(
            f"{temp_emoji} Model Temperature: {temp:.3f}{reason_text}"
        )
    
    def log_experience_summary(self, experience: Dict):
        """Log human-readable experience summary"""
        self.file_logger.info("─"*80)
        self.file_logger.info("💭 EXPERIENCE SUMMARY:")
        self.file_logger.info(f"   Arousal: {experience['arousal']['level']} ({experience['arousal']['momentum']})")
        self.file_logger.info(f"   Mental: {experience['mental']['focus']} focus, {experience['mental']['state']}")
        self.file_logger.info(f"   Sensation: {experience['sensation']['dominant_feeling']} (dominant)")
        self.file_logger.info(f"   Energy: {experience['energy']['stamina']:.0f}% stamina, {experience['energy']['fatigue']:.0f}% fatigue")
        
        if experience.get('body_hotspots'):
            self.file_logger.info(f"   Hotspots: {', '.join(experience['body_hotspots'])}")
        
        self.file_logger.info("─"*80)
    
    def log_ai_response_stimuli(self, count: int, stimuli: list):
        """Log stimuli parsed from AI response"""
        if count > 0:
            self.file_logger.info(f"🤖 AI Response contained {count} stimulus/stimuli:")
            for i, stim in enumerate(stimuli, 1):
                zone_info = f" → {stim.zone.value}" if stim.zone else ""
                self.file_logger.info(
                    f"   {i}. {stim.type}{zone_info} (intensity: {stim.intensity:.0f}%)"
                )
        else:
            self.file_logger.info("🤖 AI Response: No physical stimuli detected")
    
    def log_edge_event(self, edge_count: int, peak_arousal: float):
        """Log edging event"""
        self.file_logger.info("⚡"*40)
        self.file_logger.info(
            f"⚡ EDGE EVENT #{edge_count}: "
            f"Peak arousal: {peak_arousal:.1f}% | "
            f"Sensitivity heightened | "
            f"Body trembling at the edge"
        )
        self.file_logger.info("⚡"*40)
    
    def log_release_event(self, final_arousal: float, final_pleasure: float):
        """Log orgasm/release event"""
        self.file_logger.info("✨"*40)
        self.file_logger.info(
            f"✨ RELEASE EVENT: "
            f"Final arousal: {final_arousal:.1f}% | "
            f"Peak pleasure: {final_pleasure:.1f}% | "
            f"Neurochemical flood | "
            f"Complete release"
        )
        self.file_logger.info("✨"*40)
    
    def log_error(self, error: str, context: Optional[Dict] = None):
        """Log error"""
        self.file_logger.error(f"❌ ERROR: {error}")
        if context:
            self.file_logger.error(f"   Context: {json.dumps(context, indent=2)}")
    
    def end_session(self, success: bool = True):
        """Log end of session"""
        if self.current_session:
            duration = (
                datetime.now() - 
                datetime.fromisoformat(self.current_session['start_time'])
            ).total_seconds()
            
            status = "✅ SUCCESS" if success else "❌ FAILED"
            
            self.file_logger.info("─"*80)
            self.file_logger.info(
                f"{status} | "
                f"User: {self.current_session['user_id']} | "
                f"Events: {self.event_count} | "
                f"Duration: {duration:.2f}s"
            )
            self.file_logger.info("="*80 + "\n")
            
            self.current_session = None
            self.event_count = 0


# Global logger instance
soma_logger = SOMALogger()


def log_processing_pipeline(user_id: str, message: str, soma_before, soma_after, 
                           stimuli_input, stimuli_response, temperature: float, 
                           ai_response: str):
    """
    Log complete processing pipeline in one beautiful summary.
    Call this at the end of /api/process
    """
    logger = soma_logger
    
    logger.start_session(user_id, message)
    
    # Input stimuli
    logger.file_logger.info(f"📥 INPUT: {len(stimuli_input)} stimuli parsed from user message")
    for stim in stimuli_input:
        logger.log_stimulus_parsed(stim)
    
    # Before state
    logger.file_logger.info("")
    logger.log_state_before(soma_before)
    
    # Physiology before
    before_phys = {
        'heart_rate': soma_before.physiology.heart_rate,
        'breathing_rate': soma_before.physiology.breathing_rate
    }
    
    logger.file_logger.info("")
    
    # After state
    logger.log_state_after(soma_after)
    logger.log_physiology_change(soma_after, before_phys)
    
    # Neurochemistry
    logger.file_logger.info("")
    logger.log_neurochemistry(soma_after)
    
    # Temperature
    logger.file_logger.info("")
    temp_reason = "high arousal" if soma_after.sensation.arousal > 70 else "moderate state"
    logger.log_temperature(temperature, temp_reason)
    
    # Experience summary
    logger.file_logger.info("")
    logger.log_experience_summary(soma_after.get_experience_description())
    
    # AI response stimuli
    logger.file_logger.info("")
    logger.log_ai_response_stimuli(len(stimuli_response), stimuli_response)
    
    # Special events
    if soma_after.edge_count > soma_before.edge_count:
        logger.log_edge_event(soma_after.edge_count, soma_after.peak_arousal)
    
    # Check for release in response
    release_in_response = any(s.type == 'release' for s in stimuli_response)
    if release_in_response:
        logger.log_release_event(soma_after.sensation.arousal, soma_after.sensation.pleasure)
    
    logger.end_session(success=True)


# Usage example in soma_complete.py:
"""
# At the end of /api/process endpoint, add:

from soma_logger import log_processing_pipeline, soma_logger

# ... existing code ...

# Before final return, log everything:
try:
    log_processing_pipeline(
        user_id=user_id,
        message=message,
        soma_before=get_soma(user_id),  # Get copy before processing
        soma_after=soma,  # Current state after processing
        stimuli_input=stimuli,
        stimuli_response=response_stimuli,
        temperature=temperature,
        ai_response=ai_response
    )
except Exception as e:
    soma_logger.log_error(f"Logging failed: {e}")

return jsonify({...})
"""