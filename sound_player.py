import os
import sys
import math
import wave
import struct
import random
import threading

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

def ensure_sounds_directory():
    if not os.path.exists(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR)

def generate_sine_wave(freq, duration, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / sample_rate
        val = math.sin(2 * math.pi * freq * t)
        samples.append(val)
    return samples

def write_wav(filename, samples, sample_rate=44100):
    ensure_sounds_directory()
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, 'w') as wav_file:
        n_channels = 1
        sampwidth = 2
        wav_file.setnchannels(n_channels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(sample_rate)
        
        packed_frames = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            int_val = int(clamped * 32767.0)
            packed_frames += struct.pack('<h', int_val)
            
        wav_file.writeframes(packed_frames)
    return filepath

def create_cute_meow():
    rate = 44100
    duration = 0.4
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / rate
        f = 720.0 + 320.0 * math.sin(math.pi * t)
        env = math.sin(math.pi * t) ** 0.8
        val = math.sin(2 * math.pi * f * (i / rate)) * env * 0.7
        samples.append(val)
    write_wav("cute_meow.wav", samples, rate)

def create_happy_meow():
    rate = 44100
    duration = 0.5
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / rate
        f = 550.0 + 450.0 * (t ** 1.3)
        vibrato = math.sin(2 * math.pi * 18 * (i / rate)) * 25.0
        env = math.sin(math.pi * t)
        val = math.sin(2 * math.pi * (f + vibrato) * (i / rate)) * env * 0.75
        samples.append(val)
    write_wav("happy_meow.wav", samples, rate)

def create_sad_meow():
    rate = 44100
    duration = 0.7
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / rate
        f = 650.0 - 280.0 * t
        tremolo = 1.0 + 0.15 * math.sin(2 * math.pi * 6.0 * (i / rate))
        env = (1.0 - t) * (math.sin(math.pi * min(1.0, t * 4.0)))
        val = math.sin(2 * math.pi * f * (i / rate)) * env * tremolo * 0.65
        samples.append(val)
    write_wav("sad_meow.wav", samples, rate)

def create_angry_hiss():
    rate = 44100
    duration = 0.6
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / rate
        noise = (random.random() * 2.0 - 1.0)
        env = math.sin(math.pi * t) ** 1.2
        growl = math.sin(2 * math.pi * 120.0 * (i / rate)) * 0.3
        val = (noise * 0.7 + growl) * env * 0.65
        samples.append(val)
    write_wav("angry_hiss.wav", samples, rate)

def create_frightened_yowl():
    rate = 44100
    duration = 0.45
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / rate
        f = 1900.0 - 1100.0 * (t ** 0.5)
        tremble = math.sin(2 * math.pi * 30.0 * (i / rate)) * 80.0
        env = math.sin(math.pi * t) ** 0.7
        val = math.sin(2 * math.pi * (f + tremble) * (i / rate)) * env * 0.7
        samples.append(val)
    write_wav("frightened_yowl.wav", samples, rate)

def create_alarm_meow():
    rate = 44100
    samples = []
    pattern = [(0.2, 700, 950), (0.22, 850, 1150), (0.5, 650, 1300)]
    for duration, f_start, f_peak in pattern:
        tot = int(rate * duration)
        for i in range(tot):
            t = i / duration / rate
            f = f_start + (f_peak - f_start) * math.sin(math.pi * t)
            env = math.sin(math.pi * t) * 0.7
            val = math.sin(2 * math.pi * f * (i / rate)) * env
            samples.append(val)
        gap = int(rate * 0.08)
        samples.extend([0.0] * gap)
    write_wav("alarm_morning.wav", samples, rate)

def create_purr_sound():
    rate = 44100
    duration = 1.2
    total_samples = int(rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / rate
        carrier = math.sin(2 * math.pi * 28.0 * t) + 0.5 * math.sin(2 * math.pi * 56.0 * t)
        breath = 0.6 + 0.4 * math.sin(2 * math.pi * 1.5 * t)
        val = carrier * breath * 0.4
        samples.append(val)
    write_wav("purr.wav", samples, rate)

def create_scratch_sound():
    rate = 44100
    samples = []
    for swipe in range(3):
        tot = int(rate * 0.12)
        for i in range(tot):
            noise = (random.random() * 2.0 - 1.0)
            high_chirp = math.sin(2 * math.pi * (3200 + swipe * 400) * (i / rate))
            env = (1.0 - (i / tot)) * 0.7
            samples.append((noise * 0.6 + high_chirp * 0.4) * env)
        samples.extend([0.0] * int(rate * 0.04))
    write_wav("scratch.wav", samples, rate)

def create_tail_wipe_sound():
    rate = 44100
    samples = []
    for swish in range(4):
        tot = int(rate * 0.22)
        for i in range(tot):
            t = i / tot
            noise = (random.random() * 2.0 - 1.0)
            env = math.sin(math.pi * t)
            samples.append(noise * env * 0.35)
        samples.extend([0.0] * int(rate * 0.05))
    write_wav("tail_wipe.wav", samples, rate)

def build_all_sounds():
    ensure_sounds_directory()
    create_cute_meow()
    create_happy_meow()
    create_sad_meow()
    create_angry_hiss()
    create_frightened_yowl()
    create_alarm_meow()
    create_purr_sound()
    create_scratch_sound()
    create_tail_wipe_sound()

def play_sound_file(filename):
    filepath = os.path.join(SOUNDS_DIR, filename)
    if not os.path.exists(filepath):
        build_all_sounds()

    def _worker():
        try:
            if sys.platform.startswith("win"):
                import winsound
                winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            elif sys.platform == "darwin":
                os.system(f"afplay '{filepath}' >/dev/null 2>&1 &")
            else:
                ret = os.system(f"paplay '{filepath}' >/dev/null 2>&1 &")
                if ret != 0:
                    os.system(f"aplay -q '{filepath}' >/dev/null 2>&1 &")
        except Exception:
            pass

    t = threading.Thread(target=_worker, daemon=True)
    t.start()

class CatSoundSystem:
    def __init__(self):
        build_all_sounds()

    def happy(self):
        play_sound_file("happy_meow.wav")

    def cute(self):
        play_sound_file("cute_meow.wav")

    def sad(self):
        play_sound_file("sad_meow.wav")

    def angry(self):
        play_sound_file("angry_hiss.wav")

    def frightened(self):
        play_sound_file("frightened_yowl.wav")

    def alarm(self):
        play_sound_file("alarm_morning.wav")

    def purr(self):
        play_sound_file("purr.wav")

    def scratch(self):
        play_sound_file("scratch.wav")

    def tail_wipe(self):
        play_sound_file("tail_wipe.wav")

sound_system = CatSoundSystem()

if __name__ == "__main__":
    print("Testing sound synthesis...")
    build_all_sounds()
    print("Sounds generated in:", SOUNDS_DIR)
    sound_system.cute()
