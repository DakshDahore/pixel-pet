# 🐱 Pixel Pet — Desktop Cat Companion & Cognitive Neural Brain

[![Live Web Demo](https://img.shields.io/badge/Live_Demo-dakshdahore.github.io%2Fpixel--pet-00C7B7?style=for-the-badge&logo=github)](https://dakshdahore.github.io/pixel-pet/)
[![Tests](https://img.shields.io/badge/Automated_Tests-11%2F11_Passing-brightgreen?style=for-the-badge)](test_suite.py)
[![Python Version](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![Hackatime Week 3](https://img.shields.io/badge/Hackatime-Week_3_Submission-F59E0B?style=for-the-badge)](https://hackatime.hackclub.com)

**Pixel Pet** is an adorable, dramatic, and intelligent pixel art cat companion that lives on your desktop. It monitors your screen time, reminds you to hydrate, guards your sleep, detects when AI finishes generating answers, and throws a hilarious dramatic tantrum if you ignore it!

Equipped with an **unsupervised Cognitive Neural Brain (`neural_brain.py`)** that dynamically adapts its behavior based on your active window (VS Code, YouTube, ChatGPT, Docs), idle durations (>5 min AFK), circadian cycles, and bonding memory.

---

## ⚡ Try the Live Web Demo
**Experience it right now in your browser without installing anything:**  
👉 **[https://dakshdahore.github.io/pixel-pet/](https://dakshdahore.github.io/pixel-pet/)**

---

## ✨ Full Feature Overview

### 🧠 1. Adaptive Neural Cognitive Brain (`neural_brain.py`)
* **7-Feature Input Vector:**
  - `Context Score`: Detects active app (Coding IDE = 0.9, Learning Docs = 0.7, AI Tool = 0.85, YouTube/Distraction = 0.25).
  - `Work Strain`: Normalized continuous session duration.
  - `Inactivity / AFK`: Measures mouse/keyboard idle time (>5 min AFK activates catnap mode).
  - `Circadian Phase`: 24-hour day/night cycle.
  - `Thirst Metric`: Minutes elapsed since water logged.
  - `Affection Level`: Grows whenever you pet the cat or take breaks.
  - `Tantrum Fatigue`: Memory decay preventing spam tantrums.
* **11 Softmax Action Logits with Temperature Exploration:**
  The cat never acts like a rigid robot — each reaction is an organic, emergent behavior.
* **Habit Plasticity & Memory (`cat_memory.json`):**
  Remembers your habits across reboots, tracks bonding streak days, and preserves weight adjustments.

### 🐾 2. 12 Expressive Gestures & Animations
1. `Idle Watch`: Sits on screen edge or taskbar, tail gently swaying, periodic blinking.
2. `Happy Bounce`: Bounces with wagging tail and floating heart sparkles.
3. `Petted Purr`: Closed eyes in bliss (`^._.^`), vibration, purring hearts.
4. `Sad Pout`: Droopy ears, downward mouth, puppy tear droplet.
5. `Angry Hiss`: Flattened ears, furrowed brow, sharp hiss.
6. `Turned Cold`: Pouting silent treatment with its back turned to you.
7. `Curious Scratch`: Hind leg scratching behind the ear at the screen edge to grab attention.
8. `Peeking Bookmark`: Paws clutching the window edge like a cute bookmark.
9. `Curled Catnap`: Curls up on your window edge with animated `Z z z` bubbles when you are AFK.
10. `Falling`: Slipped off an edge, paws flailing, startled scream, landing on all fours.
11. `Empathy Beg`: Big glistening kitten eyes begging you to take a rest.
12. `Patrol Walk & Fish Treat`: Struts across window tiles and crunches delicious treats (`🐟`).

### 🎪 3. Talking Tom Gravity Physics & Tab Parkour
- **Interactive Grab & Toss**: Click/touch and drag the cat anywhere on your desktop. She dangles cute in your hand with dynamic tilt based on drag speed.
- **Talking Tom Gravity Fall**: Release her in midair and gravity takes over! She flails downwards with panic meows, accelerates to terminal velocity, and lands with an elastic squash-and-stretch bounce.
- **Window Tab Tile Platforms**: Window title bars act as solid platform tiles. Drop her above any window and she lands on the tab, ready to walk along the ledge!
- **Hop Tab to Tab (Tiles)**: Leaps across window headers like platformer tiles, hopping from one app to the next before dropping to the taskbar.
- **Hide Behind Tabs (Peek-a-boo)**: Drag her near a tab or trigger hide mode to tuck her behind the window, leaving only her cute fluffy ears and anime sparkle eyes peeking out. Click her to pop back out!

### ⚡ 4. The Dramatic Climax (Screen Scratch & Big Tail Wipe)
If you work too long without resting:
1. Cat darts to the center of your screen.
2. Claws your screen with realistic claw marks and scratch sound effects!
3. Panics at what it just did (`frightened` face with scared yowl) and scrambles away.
4. Sneaks back cautiously.
5. Vigorously sweeps its **BIG FLUFFY BUSHY TAIL** over the scratch like a feather duster until your screen is wiped clean!
6. Meows innocently, smiles (`:3`), and trots back to the corner like nothing happened!

### 🔊 4. 6 Dynamic Procedural Cat Sounds
Synthesized using pure Python standard library `wave` and `math` (zero external audio file dependencies):
- **Happy Meow:** Upbeat chirpy rising meow with dynamic micro-pitch jitter.
- **Cute Meow:** Soft high-pitched kitten mew.
- **Sad Meow:** Descending mournful whimper with tremolo.
- **Angry Hiss:** Low 120 Hz growl mixed with sharp air hiss.
- **Scared Yowl:** Startled screech with panic frequency modulation.
- **Morning Alarm Fanfare:** Joyful 3-chirp wake-up fanfare.
- *Plus continuous acoustic purring, claw scratching, and soft tail wipe swooshes!*

### 🤖 5. AI Response Watcher ("You're Up!")
- Automatically monitors your clipboard for completed responses from ChatGPT, Claude, Gemini, Copilot, or DeepSeek.
- Cat perks up, jumps, and announces: *"You're up! AI has finished generating your answer! 🐱✨"*.

### 🌙 6. Bedtime & Morning Wake-Up Alarm
- Bedtime detection: Curls up into sleeping mode at your bedtime.
- Morning alarm: Wakes you up with energetic wake-up meows.

---

## 🚀 One-Click Install & Run

### Linux & macOS
```bash
# Clone the repository
git clone https://github.com/DakshDahore/pixel-pet.git
cd pixel-pet

# One-click install dependencies
./install.sh

# Launch the desktop pet!
./run.sh
```

### Windows
- **Install:** Double-click `install.bat`
- **Run (Backgroundless):** Double-click `run.bat` or `main.pyw` (runs transparently with **no black terminal window**!)

---

## 🧪 Automated Test Suite (10/10 Passing)

Run the full automated test suite & 24-hour stress simulation:
```bash
python3 test_suite.py
```
```text
======================================================================
       PIXEL PET AUTOMATED TEST SUITE & 24-HOUR STRESS TEST
======================================================================
test_01_sound_synthesis (__main__.TestPixelPetCore.test_01_sound_synthesis) ... ok
test_02_dynamic_audio_variations (__main__.TestPixelPetCore.test_02_dynamic_audio_variations) ... ok
test_03_sprite_frames (__main__.TestPixelPetCore.test_03_sprite_frames) ... ok
test_04_scratch_overlay (__main__.TestPixelPetCore.test_04_scratch_overlay) ... ok
test_05_neural_brain_forward_pass (__main__.TestPixelPetCore.test_05_neural_brain_forward_pass) ... ok
test_06_neural_brain_afk_behavior (__main__.TestPixelPetCore.test_06_neural_brain_afk_behavior) ... ok
test_07_neural_learning_and_memory (__main__.TestPixelPetCore.test_07_neural_learning_and_memory) ... ok
test_08_window_classification (__main__.TestPixelPetCore.test_08_window_classification) ... ok
test_09_screen_tracker_timers (__main__.TestPixelPetCore.test_09_screen_tracker_timers) ... ok
test_10_simulated_24h_lifecycle_stress_test (__main__.TestPixelPetCore.test_10_simulated_24h_lifecycle_stress_test) ... ok

----------------------------------------------------------------------
Ran 10 tests in 0.204s

OK
```

---

## 📁 Repository Structure

```
pixel-pet/
├── main.py              # Main desktop application launcher
├── main.pyw             # Windows backgroundless launcher
├── pet_window.py        # Frameless transparent desktop pet window
├── control_panel.py     # Companion settings, timer, customizer & brain panel
├── neural_brain.py      # 16-neuron cognitive brain with Hebbian learning
├── window_sensor.py     # Cross-platform active window & AFK/idle sensor
├── sprites.py           # Pixel art generator for all 12 gestures
├── sound_player.py      # Procedural sound synthesizer with dynamic variation
├── screen_tracker.py    # Screen time tracker & AI response detector
├── test_suite.py        # Automated unit & 24-hr simulation test suite
├── web_server.py        # Lightweight local web demo server
├── index.html           # Interactive web demo for Hackatime submission
├── install.sh           # One-click Linux/Mac installer
├── run.sh               # One-click Linux/Mac launcher
├── install.bat          # One-click Windows installer
├── run.bat              # One-click Windows backgroundless launcher
├── requirements.txt     # Single lightweight requirement (pillow)
└── assets/              # Generated sprite frames & reference artwork
```

---

## 🏆 Hackatime Submission Info
- **Project Name:** Pixel Pet
- **Description:** A virtual pet which informs when the watch time is too much, tells to take breaks, grabs attention, and informs when AI gives response.
- **Repository:** https://github.com/DakshDahore/pixel-pet
- **Live Demo Link:** https://dakshdahore.github.io/pixel-pet/
- **Author:** Daksh Dahore
