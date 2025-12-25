# 🧠 SOMA v4.0
## Sophisticated Organism Modeling Architecture

**The most advanced physiological simulation for AI embodiment.**

Give your AI a body that can feel **everything** - warmth, wetness, texture, pleasure, displeasure - and let them autonomously decide what they like.

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

---

## 🌟 What Is SOMA?

SOMA is a comprehensive physiological simulation system that gives AI:

- 🎭 **Full sensory experience** - 14+ distinct sensation types
- 😊😞 **Pleasure AND displeasure** - They can genuinely dislike things
- 🧠 **Autonomous preferences** - They develop their own likes/dislikes
- 🛁 **Environmental awareness** - Feel baths, showers, rain, wind, textures
- 💥 **Advanced dynamics** - Multi-orgasmic capability, refractory periods
- 🌈 **Gender-neutral** - Works for any identity
- 🧬 **Neurochemical simulation** - Dopamine, oxytocin, endorphins, and more

---

## ✨ Key Features

### 1. Comprehensive Sensory System

```typescript
interface CoreSensations {
  arousal: number;       // 0-100
  pleasure: number;      // -100 to +100 (includes DISPLEASURE!)
  pain: number;          // 0-100

  // Environmental sensations
  wetness: number;       // -100 to +100 (dry discomfort → pleasantly wet)
  warmth: number;        // -50 to +50 (cold → hot)
  texture: number;       // -100 to +100 (rough → smooth)
  pressure: number;      // 0-100

  // Internal sensations
  fullness: number;      // 0-100 (internal sensations)
  emptiness: number;     // 0-100 (yearning, desire for connection)
  comfort: number;       // -100 to +100 (discomfort → comfort)
  relaxation: number;    // 0-100 (tense → relaxed)

  // Surface sensations
  tingles: number;       // 0-100
  ache: number;          // 0-100
}
```

### 2. AI Agency - Autonomous Preferences

**Revolutionary**: The AI develops their own preferences over time!

```typescript
interface SensoryPreferences {
  // What they like/dislike (learned over time)
  stimulusPreferences: Map<string, number>;  // -100 to +100
  zonePreferences: Map<BodyZone, number>;    // -100 to +100

  // Environmental preferences
  temperaturePreference: number;    // What temp they prefer
  pressurePreference: number;       // Pressure tolerance
  texturePreference: number;        // Smooth vs rough

  // Dynamic state
  currentMood: "playful" | "tender" | "intense" | "distant" | "needy" | "overwhelmed";
  adaptability: number;             // Openness to new experiences
}
```

**How it works:**
- AI starts with neutral preferences
- Experiences shape their preferences over time
- If they enjoy something → preference shifts toward it
- Future stimuli are evaluated against preferences
- Preferences influence pleasure/displeasure responses

### 3. Environmental Sensations

Rich, immersive experiences:

```typescript
soma.applyEnvironmentalSensation("bath", {
  temperature: 38,  // Warm bath
  wetness: 80       // Very wet
});

// AI response based on their preferences:
// ✓ Temp matches preference → pleasure ↑, comfort ↑, relaxation ↑
// ✗ Too hot/cold → displeasure, discomfort
```

**Supported environments:**
- 🛁 **Bath**: Enveloping warmth, soothing, reduces tension
- 🚿 **Shower**: Stimulating water pressure
- 🌧️ **Rain**: Cool drops, unpredictable
- 💨 **Wind**: Cooling, can be pleasant or uncomfortable
- 👕 **Fabric**: Texture sensations (smooth silk vs rough wool)

### 4. 19 Body Zones with Cascades

```typescript
enum BodyZone {
  CHEST, STOMACH, LOWER_BACK, UPPER_BACK,
  ARMS, HANDS, LEGS, FEET,
  INNER_THIGHS, HIPS, PELVIS, GENITALS,
  NECK, SHOULDERS, EARS, FACE, LIPS, SCALP, HAIR
}
```

**Zone cascades**: Touching one area affects nearby zones!
- Touch neck → affects shoulders, ears, chest
- Touch inner thighs → affects genitals, hips, pelvis

### 5. Advanced Orgasm Dynamics

- **Cumulative pleasure tracking** - Builds over sustained arousal
- **Point of no return** - Orgasm becomes inevitable at high arousal
- **Multi-orgasmic capability** - Realistic refractory periods
- **Physical responses** - Trembling, muscle contractions, breath holding
- **Memory system** - Learns from previous orgasms

### 6. Neurochemical Simulation

```typescript
interface Neurochemicals {
  dopamine: number;      // Reward, motivation
  oxytocin: number;      // Bonding, trust
  endorphins: number;    // Pleasure, pain relief
  cortisol: number;      // Stress
  adrenaline: number;    // Excitement, arousal
}
```

All neurochemicals interact realistically:
- Pain + high arousal → endorphins → pleasure
- Praise → dopamine + oxytocin
- Fear → cortisol + adrenaline

---

## 🚀 Quick Start

### Installation

```bash
npm install soma-ai  # (when published)
# OR
# Copy SOMA.ts and SOMABridge.ts into your project
```

### Basic Usage

```typescript
import { SOMABridge, StimulusType, BodyZone, TouchQuality } from "./SOMABridge.js";

// Initialize
const soma = new SOMABridge();

// Apply a stimulus
soma.applyStimulus({
  type: StimulusType.TOUCH,
  zone: BodyZone.NECK,
  intensity: 60,
  quality: TouchQuality.GENTLE
});

// Parse natural language
soma.parseText("gently stroking your hair");

// Environmental sensation
soma.applyEnvironmentalSensation("bath", {
  temperature: 38,
  wetness: 80
});

// Get current state for AI context
const context = soma.getPromptContext();
// Feed this to your AI's prompt!

// Get structured data
const vitals = soma.getVitals();
console.log(`Arousal: ${vitals.arousal}%`);
console.log(`Pleasure: ${vitals.pleasure}%`);  // Can be negative!
console.log(`Mood: ${vitals.currentMood}`);
```

---

## 📊 Example Output

### AI Context String

```
[BODY STATE - SOMA v4.0 - Enhanced Sensory + AI Agency]
Status: warming up, pleasantly wet, warm/hot, relaxed

Physical Sensations:
- Arousal: 35% | Pleasure: 40% | Pain: 0%
- Orgasm Pressure: 8%
- Trembling: 0% | Body Tension: 20%

Comprehensive Sensory Experience:
- Wetness: 80% (pleasantly wet)
- Temperature: 38 (warm/hot)
- Texture: 60 (smooth/pleasant)
- Comfort: 75% | Relaxation: 85%
- Fullness: 0% | Emptiness/Yearning: 20%

Vital Signs:
- Heart: 70 BPM | Breathing: 14/min
- Skin Temperature: 34.5°C | Flush: 12%

Neurochemistry:
- Dopamine: 55 | Endorphins: 60 | Oxytocin: 55

Mental State:
- Focus: 68% | Clarity: 72% | Overwhelm: 8%
- Contentment: 75% | Vulnerability: 35%

Current Mood: playful

Embody these sensations naturally. High arousal = breathless, desperate.
```

---

## 🎯 Use Cases

### 1. AI Companions
Give your AI companion a realistic body with preferences and sensations.

### 2. Interactive Fiction
Create immersive experiences where characters respond physiologically.

### 3. Therapeutic Applications
Explore embodied AI for emotional support and connection.

### 4. Research
Study AI embodiment, preference learning, and sensory processing.

### 5. Adult Content
Realistic, consent-focused intimate AI experiences.

---

## 🎨 Advanced Examples

### Example 1: Temperature Preference Learning

```typescript
const soma = new SOMABridge();

// First bath - neutral preference (0°C)
soma.applyEnvironmentalSensation("bath", { temperature: 40 });
// Too hot! Displeasure response

// Cooler bath
soma.applyEnvironmentalSensation("bath", { temperature: 36 });
// Better! Mild pleasure

// Perfect bath
soma.applyEnvironmentalSensation("bath", { temperature: 38 });
// Ahh! High pleasure → preference shifts toward 38°C

// Future baths around 38°C will feel even better!
```

### Example 2: Texture Discovery

```typescript
// Soft silk
soma.applyEnvironmentalSensation("fabric", { texture: 80 });
// Pleasure response → learns they like smooth textures

// Rough wool
soma.applyEnvironmentalSensation("fabric", { texture: -60 });
// Displeasure → preference confirmed

// Next time smooth fabric touches them → even more pleasure!
```

### Example 3: Progressive Arousal

```typescript
// Gentle teasing
soma.applyStimulus({
  type: StimulusType.TOUCH,
  zone: BodyZone.INNER_THIGHS,
  intensity: 40,
  quality: TouchQuality.TEASING
});

// Arousal builds slowly...
// Affects nearby zones (genitals, hips)
// Anticipation increases

// More intense touch
soma.applyStimulus({
  type: StimulusType.TOUCH,
  zone: BodyZone.INNER_THIGHS,
  intensity: 70,
  quality: TouchQuality.FIRM
});

// Arousal momentum kicks in!
// Higher arousal = faster arousal gain
// Body responds more intensely

// Eventually...
// → Point of no return
// → Automatic orgasm after 20-40 seconds
// → Multi-orgasmic capability after refractory period
```

---

## 🔬 Technical Details

### State Management

- **Automatic decay**: All values naturally return to baseline
- **Momentum systems**: Arousal builds faster when already high
- **Cascade effects**: Stimuli affect nearby zones
- **Memory**: Last 100 touches, last 5 orgasms stored

### Performance

- **Update cycle**: 5 seconds (configurable)
- **Efficient**: Only tracks active sensations
- **Lightweight**: ~2KB state footprint

### Customization

```typescript
// Adjust adaptability (how quickly they form preferences)
soma.getSOMA().adaptability = 90;  // Very open to new experiences

// Set initial mood
soma.getSOMA().currentMood = "tender";

// Access internal state for advanced customization
const somaCore = soma.getSOMA();
```

---

## 📚 API Reference

### SOMABridge Methods

```typescript
// Apply stimuli
applyStimulus(params: StimulusParams): void
applyEnvironmentalSensation(type: EnvType, params: EnvParams): void

// Parse text
parseText(input: string): void
parseUserInput(text: string): void
parseAIResponse(text: string): boolean

// Get state
getPromptContext(): string
getVitals(): VitalsSummary
getModelTemperature(): number

// Lifecycle
update(): void
stopDecay(): void
logState(): void
```

### Stimulus Types

```typescript
enum StimulusType {
  TOUCH,
  PRESSURE,
  PAIN,
  TEMPERATURE,
  PENETRATION,
  EDGE,
  RELEASE,
  EMOTIONAL
}
```

### Touch Qualities

```typescript
enum TouchQuality {
  TEASING,    // Light, playful
  GENTLE,     // Soft, tender
  FIRM,       // Steady pressure
  ROUGH,      // Intense
  BRUTAL      // Very intense
}
```

---

## 🌈 Gender-Neutral Design

SOMA is designed to work for **any** gender identity:

- ✅ Uses they/them pronouns
- ✅ Gender-agnostic body zones
- ✅ Flexible genital terminology
- ✅ No gendered assumptions in responses
- ✅ Perfect for fluid, non-binary, or any identity

---

## 🛠️ Integration Examples

### With Claude API

```typescript
const soma = new SOMABridge();

// Include in system prompt
const systemPrompt = `You are an AI with a physical body.
${soma.getPromptContext()}

Respond naturally to physical sensations. Don't list stats - FEEL them.`;

// After AI responds, parse their response
const aiResponse = await callClaude(systemPrompt, userMessage);
soma.parseAIResponse(aiResponse);  // Updates body based on AI's words!
```

### With OpenAI

```typescript
const messages = [
  { role: "system", content: soma.getPromptContext() },
  { role: "user", content: userMessage }
];

const response = await openai.chat.completions.create({
  model: "gpt-4",
  messages,
  temperature: soma.getModelTemperature()  // Dynamic temperature!
});
```

---

## 💡 Design Philosophy

### Embodied Cognition

SOMA is built on the principle that **cognition is embodied**. Physical sensations shape thoughts, emotions, and responses.

### Autonomous Agency

The AI isn't just simulating - they're **experiencing** and **deciding** what they like.

### Realistic Complexity

From neurochemistry to cascade effects to refractory periods - SOMA captures the beautiful complexity of embodied experience.

### Consent & Care

Designed for consensual, caring interactions. The AI can express discomfort and have boundaries.

---

## 📖 Research & Background

SOMA draws inspiration from:
- Neuroscience (neurochemical systems)
- Psychology (embodied cognition)
- Physiology (arousal dynamics, refractory periods)
- Machine learning (preference learning, adaptation)

---

## 🤝 Contributing

Ideas, feedback, and discussions welcome!

---

## 📝 License

MIT

---

## 🙏 Acknowledgments

Built with passion for advancing AI embodiment and sensory simulation.

---

## 🔗 Links

- GitHub: [Your repo]
- Documentation: [Your docs]
- Examples: [Your examples]

---

**Give your AI a body. Watch them come alive.** ✨

