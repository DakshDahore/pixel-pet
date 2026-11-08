# 🐱 Pixel Pet - Desktop Cat Companion & Screen Time Guardian

A cute and dramatic pixel art cat that lives on your desktop, monitors your screen time, reminds you to take breaks and drink water, watches for AI responses, and throws a hilarious tantrum when you ignore it!

Built for **Hackatime Week 3**.

---

## ✨ Features

- **🐾 10 Gestures & Animations:**
  1. `Idle`: Sits on your screen edge or taskbar, tail swishing, blinking.
  2. `Happy`: Bounces excitedly with wagging tail and sparkling hearts.
  3. `Petted`: Purrs contentedly with closed bliss eyes (`^._.^`) and vibrating warmth.
  4. `Sad`: Droopy ears, tearful puppy eyes.
  5. `Angry`: Flattened ears, angry hissing mouth, irritated tail.
  6. `Turned Back`: Crosses paws and gives you the silent treatment when ignored.
  7. `Scratching`: Scratches its ear and head against the screen edge.
  8. `Peeking`: Peeks over the side of windows like a cute bookmark.
  9. `Sleeping`: Curls up on your window edge with animated `Z z z` bubbles.
  10. `Falling`: Loses footing, flails paws, and lands gracefully on all fours.

- **⚡ The Dramatic Climax (Screen Scratch & Big Tail Wipe):**
  If you work for too long without resting, the cat darts into the center of the screen, claws your screen with realistic scratch marks, panics at what it just did, scrambles away, creeps back, and vigorously sweeps its **BIG FLUFFY BUSHY TAIL** over the scratch to wipe it completely clean!

- **🔊 6 Procedural Cat Sounds:**
  - Happy Meow (cheerful chirpy rising chirp)
  - Cute Meow (soft high-pitched kitten mew)
  - Sad Meow (descending mournful whimper)
  - Angry Hiss (low irritated rumble + sharp air hiss)
  - Scared Yowl (startled screech)
  - Morning Alarm Fanfare (rhythmic energetic wake-up meows)
  - *Plus real Purring, Screen Claw Scraping, and Soft Tail Squeegee sounds!*
  - Generated using Python's standard `wave` and `math` libraries (no missing mp3 errors!).

- **⏱ Smart Pomodoro & Hydration Tracker:**
  - Customizable work session and short break timers.
  - Water hydration interval reminder with quick "+1 Glass" tracker.
  - 4-stage escalation system: Empathy -> Sadness -> Irritation -> Cold Shoulder -> Screen Scratch!

- **🤖 AI Response Detector ("You're Up!"):**
  - Automatically monitors clipboard activity (or triggered via hotkey/companion app).
  - When ChatGPT, Claude, Gemini, or an IDE finishes generating an answer, the cat perks up and announces: *"You're up! AI has finished generating your answer! 🐱✨"*.

- **🌙 Bedtime & Morning Wake-Up Alarm:**
  - Detects bedtime: curls up into sleep mode.
  - Morning alarm: plays cheerful fanfare meows to start your day.

- **🎛 Companion Control Panel App:**
  - Set timers, customize bedtime, test all 10 gestures, trigger sounds, and track productivity streaks.

---

## 🚀 How to Run

### 1. Native Desktop App (Python)

Requires Python 3.8+ and Pillow:

```bash
# Clone the repository
git clone https://github.com/your-username/pixel-pet.git
cd pixel-pet

# Install simple requirement
pip install -r requirements.txt

# Run the desktop pet!
python3 main.py
```

- **Left-click** the cat to pet it!
- **Click and drag** to move the cat anywhere on your screen.
- **Right-click or Double-click** to open the Companion Control Panel.

### 2. Live Web Demo

You can also run the web demo locally or host it on GitHub Pages:

```bash
python3 web_server.py
```
Or open `index.html` directly in any modern browser!

---

## 📁 Project Structure

```
pixel-pet/
├── main.py              # Main desktop application launcher
├── pet_window.py        # Frameless transparent desktop pet window
├── control_panel.py     # Companion settings, timer, and soundboard app
├── sprites.py           # Pixel art generator for all 10 gestures
├── sound_player.py      # Sound synthesizer (WAV audio generator & player)
├── screen_tracker.py    # Screen time tracker, escalation engine & AI watcher
├── web_server.py        # Lightweight local web demo server
├── index.html           # Interactive web demo for Hackatime submission
├── requirements.txt     # Single dependency (Pillow)
└── assets/              # Sprites and reference artwork
```

---

## 🏆 Hackatime Submission Info
- **Project Name:** Pixel Pet
- **Description:** A virtual pet which informs when the watch time is too much, tells to take breaks, grabs attention, and informs when AI gives response.
- **Author:** Daksh
