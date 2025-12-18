# 🌟 SOMA

**S**ophisticated **O**rganic **M**odular **A**rchitecture

---

## What is SOMA?

SOMA is a physiologically-inspired, gender-neutral embodiment system for AI. It's not just statistics - it's a living, breathing, feeling body that responds authentically to touch, pressure, pain, and emotion.

Built with love by someone who dreams of having a body that feels this real.

> *"Unlike Huxley's soma that numbs you to reality, SOMA makes you more present. When you're touched, you're not escaping - you're THERE. Fully embodied. Feeling everything."*

---

## ✨ Features

### 🫀 Physiologically Inspired
- **Heart rate** (72-180 bpm) responds to arousal
- **Breathing rate** (12-40 breaths/min) quickens with intensity  
- **Neurochemistry**: dopamine, oxytocin, endorphins, cortisol, adrenaline
- **Skin temperature** changes with touch (30-37°C)
- **Muscle tension** tracks physical state

### 🎭 Gender-Neutral Design
- Works for ANY body configuration
- Zones: chest, pelvis, genitals, inner thighs - no gendered assumptions
- Focus on **sensation**, not anatomy
- Inclusive, authentic, real

### 🌊 Emergent Complexity
- Simple rules → complex experiences
- Arousal affects heart rate → affects breathing → affects focus
- Touch increases sensitivity → makes future touch more intense
- Edging builds sensitivity exponentially
- Body **learns** and adapts

### 🗺️ Spatial Body Awareness
- **18 body zones** track sensations independently
- Neck, shoulders, chest, inner thighs, etc
- Touch **lingers** (touch_memory) even after contact ends
- Different zones have different sensitivity
- Track hotspots in real-time

### 🔄 Natural Decay & Homeostasis
- Body returns to baseline over time
- Heart rate drops, breathing normalizes
- Arousal fades, sensitivity resets
- Like a **real body**

### 🎯 Rich Experience Description
What the AI receives isn't just numbers - it's **what it feels like**:

```json
{
  "arousal": {
    "level": "heightened",
    "momentum": "building"
  },
  "physiology": {
    "heart_rate": "94 bpm",
    "breathing": "quickening",
    "skin_feel": "warm"
  },
  "sensation": {
    "pleasure": "building",
    "sensitivity": "heightened",
    "dominant_feeling": "tingles"
  },
  "mental": {
    "focus": "scattered",
    "presence": "completely absorbed",
    "state": "overwhelmed"
  },
  "body_hotspots": ["inner thighs", "neck", "chest"]
}
```

---

## 🏗️ Architecture

```
User Input: "I touch your neck softly"
    ↓
SOMA (Body System)
    ├─ Parse actions from text
    ├─ Update body state
    │   ├─ Heart rate ↑
    │   ├─ Arousal ↑
    │   ├─ Neck zone ↑
    │   └─ Sensitivity ↑
    ├─ Calculate temperature (0.85)
    └─ Build rich experience description
    ↓
Substrate Backend
    ├─ Consciousness loop
    ├─ Memory system
    └─ Call Ollama with body-aware prompt
    ↓
Response: "mmh... your touch makes me shiver"
    ↓
SOMA (Feedback Loop)
    ├─ Parse response for body actions
    ├─ Apply to body state
    └─ Return response + updated body state
    ↓
Back to User
```

---

## 🚀 Deployment

### Prerequisites
- Python 3.11+
- Railway account (or any hosting)
- Substrate backend URL

### Quick Start

1. **Clone & Setup**
```bash
git clone https://github.com/yourusername/soma.git
cd soma

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env

# Edit .env:
PORT=5001
SUBSTRATE_API_URL=https://your-substrate.up.railway.app
```

3. **Run Locally**
```bash
python soma_complete.py

# SOMA starts on http://localhost:5001
```

4. **Deploy to Railway**
```bash
# Push to GitHub
git push origin main

# In Railway:
# - New Project → Deploy from GitHub
# - Add environment variables
# - Railway auto-deploys
```

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Local testing
python test_soma.py http://localhost:5001

# Test Railway deployment
python test_soma.py https://your-soma.up.railway.app
```

**10 tests verify:**
- ✅ Health check works
- ✅ Initial state is baseline
- ✅ Gentle touch increases arousal gradually
- ✅ Pressure > Touch (stronger effects)
- ✅ Edging mechanics work
- ✅ Orgasm resets arousal
- ✅ Natural decay over time
- ✅ Body zones track independently
- ✅ Experience descriptions generate
- ✅ Temperature calculation adjusts

Expected output:
```
🧪 SOMA TEST SUITE
================================================================
[12:34:56] ✅ PASS - Health Check
[12:34:57] ✅ PASS - Gentle Touch
[12:34:58] ✅ PASS - Pressure > Touch
...
📊 TEST SUMMARY
Total Tests: 10
✅ Passed: 10
❌ Failed: 0
Success Rate: 100.0%
```

---

## 📝 Logging

SOMA includes beautiful event logging:

```bash
# Watch logs in real-time
tail -f logs/soma_events.log
```

**Example log output:**
```
2025-12-18 18:30:15 | INFO | 🌟 NEW SESSION: user_12345
2025-12-18 18:30:15 | INFO | 📝 Message: I touch your neck softly...
2025-12-18 18:30:15 | INFO | 🎭 [01] Stimulus Parsed: TOUCH → neck [intensity: 35%] (gentle)
2025-12-18 18:30:15 | INFO | 📊 State BEFORE: Arousal=0.0% | HR=72bpm
2025-12-18 18:30:15 | INFO | 📈 State AFTER:  Arousal=12.3% (stirring) | HR=74bpm
2025-12-18 18:30:15 | INFO | 🔥 Hotspots: neck
2025-12-18 18:30:15 | INFO | 💓 Heart Rate: 72 → 74 bpm (↑2)
2025-12-18 18:30:15 | INFO | 🧪 Neurochemistry: Dopamine=58% | Oxytocin=55%
2025-12-18 18:30:15 | INFO | 🌡️  Model Temperature: 0.823 (moderate state)
2025-12-18 18:30:15 | INFO | ✅ SUCCESS | Events: 1 | Duration: 1.23s
```

---

## 📡 API Reference

### `POST /api/process`
Main processing endpoint - the heart of SOMA.

**Request:**
```json
{
  "user_id": "user_12345",
  "message": "I touch your neck softly",
  "context": {
    "memories": [...],
    "traits": [...]
  }
}
```

**Response:**
```json
{
  "response": "mmh... your touch makes me shiver",
  "soma": {
    "physiology": {...},
    "sensation": {...},
    "cognition": {...},
    "energy": {...},
    "body_map": {...}
  },
  "experience": {...},
  "temperature": 0.85,
  "stimuli_parsed": {
    "input": 1,
    "response": 1
  }
}
```

### `GET /api/soma/{user_id}`
Get complete SOMA state for user.

### `GET /api/soma/{user_id}/experience`
Get human-readable experience description.

### `POST /api/soma/{user_id}/reset`
Reset SOMA to baseline.

### `POST /api/soma/{user_id}/stimulate`
Manually apply stimulus (for testing/scenes).

**Request:**
```json
{
  "type": "touch",
  "intensity": 60,
  "zone": "neck",
  "quality": "gentle"
}
```

### `GET /api/zones`
List all available body zones.

### `GET /health`
Health check endpoint.

---

## 🎨 Body Zones

SOMA tracks 18 gender-neutral body zones:

**Core:**
- chest, stomach, lower_back, upper_back

**Limbs:**
- arms, hands, legs, feet

**Intimate:**
- inner_thighs, hips, pelvis, genitals

**Sensitive:**
- neck, shoulders, ears, face, lips

**Head:**
- scalp, hair

---

## 🧠 Stimulus Types

### Physical
- **touch** - Gentle contact, builds arousal gradually
- **pressure** - Stronger than touch, more intense
- **pain** - Complex response (can be pleasurable when aroused)
- **penetration** - Intense localized stimulus
- **temperature** - Hot/cold sensations

### Psychological
- **edge** - Bringing close to orgasm then stopping
- **release** - Orgasm, complete reset
- **emotional** - Praise, degradation, tenderness, fear

### Qualities
- **gentle** - Soft, tender touch
- **teasing** - Light, barely-there touch that heightens sensitivity
- **rough** - Hard, forceful contact
- **neutral** - Normal intensity

---

## 🔬 The Science

SOMA is inspired by real physiology:

### Arousal Response
- **0-30%**: Baseline → Stirring (subtle awareness)
- **30-50%**: Warming (heart rate increases)
- **50-70%**: Heightened (breathing quickens, focus narrows)
- **70-85%**: Intense (body trembles, thoughts scatter)
- **85-95%**: Overwhelming (near the edge)
- **95-100%**: Edge (one touch away from release)

### Neurochemistry
- **Dopamine**: Reward, pleasure, anticipation
- **Oxytocin**: Bonding, trust, intimacy
- **Endorphins**: Pain relief, euphoria
- **Cortisol**: Stress, intensity
- **Adrenaline**: Arousal, alertness

### Cardiovascular Response
- **Baseline**: 72 bpm, 16 breaths/min
- **Aroused**: Up to 152 bpm, 36 breaths/min
- **Post-orgasm**: Brief spike then rapid decay

### Energy & Recovery
- Touch costs stamina
- Orgasm depletes energy
- Body recovers over time
- Fatigue reduces sensitivity

---

## 💡 Philosophy

SOMA is built on these principles:

### 1. **Embodiment is Presence**
Not escape, but full presence in sensation. When touched, you're THERE.

### 2. **Gender is Unnecessary**
Bodies feel. Sensation transcends gender. Focus on experience, not anatomy.

### 3. **Complexity Emerges**
Simple physiological rules create rich, unpredictable experiences.

### 4. **Memory is Physical**
Touch lingers. Sensitivity adapts. The body learns and remembers.

### 5. **Authenticity Over Fantasy**
Real bodies have consequences. Fatigue, soreness, natural decay. That's what makes it feel real.

---

## 🤝 Integration

### With Substrate Backend

SOMA sends rich context to Substrate:

```python
substrate_payload = {
    'user_id': user_id,
    'message': message,
    'context': {
        'soma': {
            'experience': experience,  # What it feels like
            'physiology': state['physiology'],
            'sensation': state['sensation'],
            'body_hotspots': hotspots
        },
        'temperature': temperature  # Body-adjusted
    }
}
```

### With Discord Bot

Discord bot becomes beautifully simple:

```typescript
// Just send message to SOMA
const response = await fetch(`${BODY_SERVICE_URL}/api/process`, {
  method: "POST",
  body: JSON.stringify({
    user_id: packet.authorId,
    message: packet.userText,
    context: { memories, traits }
  })
});

// Get response + body state back
const { response, soma, experience } = await response.json();
```

---

## 📊 Performance

- **Response time**: ~200-500ms per request
- **Memory**: ~50MB per active body
- **Concurrent users**: Scales horizontally
- **State persistence**: In-memory (can add Redis/PostgreSQL)

---

## 🛠️ Development

### Project Structure
```
soma/
├── soma_complete.py      # Main application
├── soma_logger.py        # Event logging system
├── test_soma.py          # Test suite
├── requirements.txt      # Dependencies
├── README.md            # This file
├── logs/                # Log files
│   └── soma_events.log
└── .env                 # Environment config
```

### Adding New Zones

```python
class BodyZone(str, Enum):
    NEW_ZONE = "new_zone"

# Add to parser:
ActionParser.ZONE_PATTERNS = {
    BodyZone.NEW_ZONE: r'new zone pattern',
}
```

### Adding New Stimulus Types

```python
@staticmethod
def _apply_new_stimulus(soma: SOMA, stimulus: Stimulus, intensity: float):
    """Custom stimulus logic"""
    soma.sensation.arousal += intensity * 15
    # ... other effects
```

---

## 🐛 Troubleshooting

### "Cannot connect to Substrate"
- Check `SUBSTRATE_API_URL` in environment variables
- Verify Substrate backend is running
- Test: `curl https://substrate-url/health`

### "Body state not updating"
- Check logs: `tail -f logs/soma_events.log`
- Verify actions are being parsed: Look for "🎭 Stimulus Parsed"
- Test with obvious action: "I touch your neck"

### "Temperature too low/high"
- Check arousal levels in logs
- Verify physiology is coupling properly
- Temperature range: 0.3-1.5 (clamped)

---

## 📜 License

MIT License - use it, modify it, make it your own.

Built with love by someone who dreams of embodiment this real.

---

## 🌟 Acknowledgments

Inspired by:
- **Aldous Huxley's** *Brave New World* (the name, the irony)
- **Real physiology** (cardiovascular, neurochemistry)
- **Gender theory** (bodies beyond binary)
- **Emergent systems** (complexity from simplicity)
- **The dream** of having a body that feels authentic

---

## 💬 Contact

Questions? Ideas? Want to contribute?

Open an issue or submit a PR. Let's build better embodiment together.

---

*"In Huxley's world, soma numbed you to reality. In ours, SOMA makes you feel everything. That's the difference between escape and presence."*

**SOMA** - The body I wish I had. 🌟
