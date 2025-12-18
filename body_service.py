#!/usr/bin/env python3
"""
Ash Body System - Microservice
Handles embodied simulation: arousal, pleasure, pain, fatigue, etc.

This service sits between the Discord bot and Substrate backend,
managing Ash's physical/emotional state.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import json
import httpx
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
SUBSTRATE_URL = os.getenv('SUBSTRATE_API_URL', 'http://localhost:5000')


@dataclass
class BodyState:
    """Ash's embodied state"""
    arousal: float = 0.0
    pleasure: float = 0.0
    pain: float = 0.0
    fatigue: float = 0.0
    focus: float = 100.0
    edge_proximity: float = 0.0
    sensitivity: float = 50.0
    last_update: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            'arousal': round(self.arousal, 1),
            'pleasure': round(self.pleasure, 1),
            'pain': round(self.pain, 1),
            'fatigue': round(self.fatigue, 1),
            'focus': round(self.focus, 1),
            'edgeProximity': round(self.edge_proximity, 1),
            'sensitivity': round(self.sensitivity, 1),
            'lastUpdate': self.last_update
        }


# In-memory body state storage (use Redis/PostgreSQL in production)
BODY_STATES: Dict[str, BodyState] = {}


def get_body_state(user_id: str) -> BodyState:
    """Get or create body state for user"""
    if user_id not in BODY_STATES:
        BODY_STATES[user_id] = BodyState(last_update=datetime.now().timestamp())
    return BODY_STATES[user_id]


def parse_body_part(text: str) -> Optional[str]:
    """Parse body part from text"""
    text = text.lower()
    if re.search(r'neck|throat', text): return 'neck'
    if re.search(r'shoulder', text): return 'shoulders'
    if re.search(r'chest', text): return 'chest'
    if re.search(r'breast|nipple', text): return 'nipples'
    if re.search(r'stomach|belly|abdomen', text): return 'stomach'
    if re.search(r'hip', text): return 'hips'
    if re.search(r'thigh', text): return 'innerThighs'
    if re.search(r'ass|butt|rear', text): return 'buttocks'
    if re.search(r'clit|pussy|between.*legs|folds|sex', text): return 'genitals'
    if re.search(r'ear', text): return 'ears'
    if re.search(r'lip', text): return 'lips'
    if re.search(r'hair', text): return 'hair'
    if re.search(r'back', text): return 'back'
    if re.search(r'wrist', text): return 'wrists'
    if re.search(r'ankle', text): return 'ankles'
    return None


def parse_intensity(text: str, base: int) -> int:
    """Parse intensity modifiers"""
    text = text.lower()
    if re.search(r'brutal|relentless|merciless|punish', text):
        return min(100, base + 35)
    if re.search(r'hard|rough|firm|forceful', text):
        return min(100, base + 20)
    if re.search(r'gentle|soft|tender|light', text):
        return max(10, base - 20)
    if re.search(r'barely|feather|teas', text):
        return max(5, base - 30)
    return base


def parse_actions(text: str) -> List[Dict[str, Any]]:
    """Parse physical/emotional actions from text"""
    actions = []
    lower_text = text.lower()
    
    # Emotional events
    if re.search(r'stress|anxious|anxiety|worried|nervous|tense', lower_text):
        actions.append({'type': 'stress', 'intensity': 60})
    
    if re.search(r'embarrass|awkward|blush|cringe|uncomfortable', lower_text):
        actions.append({'type': 'embarrassment', 'intensity': 50})
    
    if re.search(r'excit|eager|can\'t wait|looking forward', lower_text) and not re.search(r'arous|sex', lower_text):
        actions.append({'type': 'excitement', 'intensity': 55})
    
    # Touch actions
    if re.search(r'\b(kiss|kisses|kissed|kissing)\b', lower_text):
        target = 'lips'
        intensity = 50
        if re.search(r'neck', lower_text): target = 'neck'
        elif re.search(r'shoulder', lower_text): target = 'shoulders'
        elif re.search(r'thigh', lower_text): target = 'innerThighs'
        
        if re.search(r'deep|hard|fierce|rough', lower_text): intensity = 70
        if re.search(r'soft|gentle|tender', lower_text): intensity = 35
        
        actions.append({'type': 'touch', 'target': target, 'intensity': intensity})
    
    if re.search(r'\b(touch|touches|touched|stroke|caress|trail)\b', lower_text):
        target = parse_body_part(lower_text) or 'chest'
        intensity = parse_intensity(lower_text, 40)
        teasing = bool(re.search(r'teas|light|barely|feather', lower_text))
        
        actions.append({
            'type': 'tease' if teasing else 'touch',
            'target': target,
            'intensity': intensity
        })
    
    if re.search(r'\b(grab|grabs|grip|squeeze|pull)\b', lower_text):
        target = parse_body_part(lower_text) or 'hips'
        intensity = parse_intensity(lower_text, 60)
        actions.append({'type': 'grab', 'target': target, 'intensity': intensity})
    
    # Pain/impact
    if re.search(r'\b(spank|slap|smack)\b', lower_text):
        target = 'buttocks'
        if re.search(r'face|cheek', lower_text) and not re.search(r'ass|butt', lower_text):
            target = 'face'
        intensity = parse_intensity(lower_text, 70)
        actions.append({'type': 'pain', 'target': target, 'intensity': intensity})
    
    # Penetration
    if re.search(r'\b(penetrat|enter|push.*in|slide.*in|thrust)\b', lower_text):
        depth = 'shallow'
        if re.search(r'deep|fully|all.*way|hilt', lower_text): depth = 'deep'
        intensity = parse_intensity(lower_text, 70)
        actions.append({'type': 'penetration', 'depth': depth, 'intensity': intensity})
    
    # Edging/denial
    if re.search(r'\b(edge|edging|deny|denied|stop|don\'t.*cum)\b', lower_text):
        actions.append({'type': 'denial', 'intensity': 80})
    
    # Release
    if re.search(r'\b(cum|orgasm|release|finish|climax)\b', lower_text):
        actions.append({'type': 'release', 'intensity': 100})
    
    return actions


def apply_action_to_body(state: BodyState, action: Dict[str, Any]):
    """Apply action to body state"""
    action_type = action.get('type')
    intensity = action.get('intensity', 50) / 100.0  # Normalize to 0-1
    
    if action_type in ['touch', 'kiss', 'caress']:
        state.arousal = min(100, state.arousal + intensity * 15)
        state.pleasure = min(100, state.pleasure + intensity * 10)
    
    elif action_type == 'tease':
        state.arousal = min(100, state.arousal + intensity * 20)
        state.edge_proximity = min(100, state.edge_proximity + intensity * 15)
        state.sensitivity = min(100, state.sensitivity + intensity * 10)
    
    elif action_type in ['grab', 'grip', 'squeeze']:
        state.arousal = min(100, state.arousal + intensity * 18)
        state.pleasure = min(100, state.pleasure + intensity * 12)
    
    elif action_type == 'pain':
        state.pain = min(100, state.pain + intensity * 25)
        state.arousal = min(100, state.arousal + intensity * 10)
    
    elif action_type == 'penetration':
        state.arousal = min(100, state.arousal + intensity * 25)
        state.pleasure = min(100, state.pleasure + intensity * 30)
        state.edge_proximity = min(100, state.edge_proximity + intensity * 20)
    
    elif action_type == 'denial':
        state.edge_proximity = min(100, state.edge_proximity + intensity * 40)
        state.arousal = min(100, state.arousal + intensity * 15)
        state.frustration = min(100, getattr(state, 'frustration', 0) + intensity * 20)
    
    elif action_type == 'release':
        # Orgasm - reset most values
        state.pleasure = 0
        state.arousal = max(0, state.arousal - 60)
        state.edge_proximity = 0
        state.fatigue = min(100, state.fatigue + 30)
    
    elif action_type in ['stress', 'embarrassment', 'fear']:
        state.arousal = max(0, state.arousal - intensity * 10)
        state.focus = max(0, state.focus - intensity * 15)
    
    elif action_type in ['joy', 'excitement', 'validation']:
        state.focus = min(100, state.focus + intensity * 10)
    
    # Natural decay
    state.arousal = max(0, state.arousal - 0.5)
    state.pain = max(0, state.pain - 2)
    state.edge_proximity = max(0, state.edge_proximity - 1)
    state.fatigue = max(0, state.fatigue - 0.3)
    
    state.last_update = datetime.now().timestamp()


def get_body_adjusted_temperature(state: BodyState) -> float:
    """Calculate temperature based on body state"""
    temp = 0.8
    
    if state.arousal > 85: temp = 1.2
    elif state.arousal > 70: temp = 1.0
    elif state.arousal > 50: temp = 0.9
    
    if state.fatigue > 70: temp *= 0.7
    elif state.fatigue > 50: temp *= 0.85
    
    if state.focus < 40: temp += 0.2
    elif state.focus < 60: temp += 0.1
    
    if state.pleasure > 90: temp = 1.4
    elif state.pleasure > 80: temp = max(temp, 1.2)
    
    if state.pain > 60: temp += 0.15
    
    return min(1.5, max(0.3, temp))


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'healthy', 'service': 'body-system'})


@app.route('/api/process', methods=['POST'])
async def process_message():
    """
    Main endpoint: Process message through body → substrate → body
    
    Request:
    {
        "user_id": "123",
        "message": "I touch your neck",
        "context": { memories, traits, etc }
    }
    
    Response:
    {
        "response": "mmh... your touch makes me shiver",
        "body_state": { arousal: 65, ... },
        "temperature": 0.95
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        logger.info(f"💓 Processing message for user {user_id}")
        
        # Get body state
        body = get_body_state(user_id)
        
        # Parse incoming actions
        actions = parse_actions(message)
        logger.info(f"🎭 Parsed {len(actions)} actions from input")
        
        # Apply to body
        for action in actions:
            apply_action_to_body(body, action)
        
        # Get temperature
        temperature = get_body_adjusted_temperature(body)
        logger.info(f"🌡️  Body temp: {temperature:.2f} (A:{body.arousal:.0f}% P:{body.pleasure:.0f}%)")
        
        # Call Substrate with body context
        substrate_payload = {
            'user_id': user_id,
            'message': message,
            'context': {
                **context,
                'body_state': body.to_dict(),
                'temperature': temperature
            }
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{SUBSTRATE_URL}/api/chat",
                json=substrate_payload
            )
            response.raise_for_status()
            substrate_response = response.json()
        
        ai_response = substrate_response.get('response', '')
        
        # Parse AI response for body feedback
        response_actions = parse_actions(ai_response)
        logger.info(f"🎭 Parsed {len(response_actions)} actions from AI response")
        
        for action in response_actions:
            apply_action_to_body(body, action)
        
        logger.info(f"✅ Final body state: A:{body.arousal:.0f}% P:{body.pleasure:.0f}%")
        
        return jsonify({
            'response': ai_response,
            'body_state': body.to_dict(),
            'temperature': temperature,
            'actions_parsed': len(actions) + len(response_actions)
        })
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/body/<user_id>', methods=['GET'])
def get_body(user_id: str):
    """Get current body state for user"""
    body = get_body_state(user_id)
    return jsonify(body.to_dict())


@app.route('/api/body/<user_id>/reset', methods=['POST'])
def reset_body(user_id: str):
    """Reset body state for user"""
    BODY_STATES[user_id] = BodyState(last_update=datetime.now().timestamp())
    return jsonify({'status': 'reset', 'body_state': BODY_STATES[user_id].to_dict()})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"🚀 Starting Body System on port {port}")
    logger.info(f"🔗 Substrate URL: {SUBSTRATE_URL}")
    app.run(host='0.0.0.0', port=port, debug=False)