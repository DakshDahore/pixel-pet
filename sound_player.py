import os
import sys
import math
import wave
import struct
import random
import threading
import time

SOUNDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")

def ensure_sounds_directory():
    if not os.path.exists(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR)

def write_wav(filepath, samples, sample_rate=44100):
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        packed_frames = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            int_val = int(clamped * 32767.0)
            packed_frames += struct.pack('<h', int_val)

        wav_file.writeframes(packed_frames)
    return filepath

def create_cute_meow_samples(pitch_scale=1.0, duration=0.4, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    base_f = 720.0 * pitch_scale
    for i in range(total_samples):
        t = i / duration / sample_rate
        f = base_f + (320.0 * pitch_scale) * math.sin(math.pi * t)
        env = math.sin(math.pi * t) ** 0.8
        val = math.sin(2 * math.pi * f * (i / sample_rate)) * env * 0.7
        samples.append(val)
    return samples

def create_happy_meow_samples(pitch_scale=1.0, duration=0.5, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    base_f = 550.0 * pitch_scale
    for i in range(total_samples):
        t = i / duration / sample_rate
        f = base_f + (450.0 * pitch_scale) * (t ** 1.3)
        vibrato = math.sin(2 * math.pi * 18 * (i / sample_rate)) * 25.0
        env = math.sin(math.pi * t)
        val = math.sin(2 * math.pi * (f + vibrato) * (i / sample_rate)) * env * 0.75
        samples.append(val)
    return samples

def create_sad_meow_samples(pitch_scale=1.0, duration=0.7, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    base_f = 650.0 * pitch_scale
    for i in range(total_samples):
        t = i / duration / sample_rate
        f = base_f - (280.0 * pitch_scale) * t
        tremolo = 1.0 + 0.15 * math.sin(2 * math.pi * 6.0 * (i / sample_rate))
        env = (1.0 - t) * (math.sin(math.pi * min(1.0, t * 4.0)))
        val = math.sin(2 * math.pi * f * (i / sample_rate)) * env * tremolo * 0.65
        samples.append(val)
    return samples

def create_angry_hiss_samples(duration=0.6, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / sample_rate
        noise = (random.random() * 2.0 - 1.0)
        env = math.sin(math.pi * t) ** 1.2
        growl = math.sin(2 * math.pi * 120.0 * (i / sample_rate)) * 0.3
        val = (noise * 0.7 + growl) * env * 0.65
        samples.append(val)
    return samples

def create_frightened_yowl_samples(duration=0.45, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / duration / sample_rate
        f = 1900.0 - 1100.0 * (t ** 0.5)
        tremble = math.sin(2 * math.pi * 30.0 * (i / sample_rate)) * 80.0
        env = math.sin(math.pi * t) ** 0.7
        val = math.sin(2 * math.pi * (f + tremble) * (i / sample_rate)) * env * 0.7
        samples.append(val)
    return samples

def create_alarm_meow_samples(sample_rate=44100):
    samples = []
    pattern = [(0.2, 700, 950), (0.22, 850, 1150), (0.5, 650, 1300)]
    for duration, f_start, f_peak in pattern:
        tot = int(sample_rate * duration)
        for i in range(tot):
            t = i / duration / sample_rate
            f = f_start + (f_peak - f_start) * math.sin(math.pi * t)
            env = math.sin(math.pi * t) * 0.7
            val = math.sin(2 * math.pi * f * (i / sample_rate)) * env
            samples.append(val)
        gap = int(sample_rate * 0.08)
        samples.extend([0.0] * gap)
    return samples

def create_purr_samples(duration=1.2, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    for i in range(total_samples):
        t = i / sample_rate
        carrier = math.sin(2 * math.pi * 28.0 * t) + 0.5 * math.sin(2 * math.pi * 56.0 * t)
        breath = 0.6 + 0.4 * math.sin(2 * math.pi * 1.5 * t)
        val = carrier * breath * 0.4
        samples.append(val)
    return samples

def create_scratch_samples(sample_rate=44100):
    samples = []
    for swipe in range(3):
        tot = int(sample_rate * 0.12)
        for i in range(tot):
            noise = (random.random() * 2.0 - 1.0)
            high_chirp = math.sin(2 * math.pi * (3200 + swipe * 400) * (i / sample_rate))
            env = (1.0 - (i / tot)) * 0.7
            samples.append((noise * 0.6 + high_chirp * 0.4) * env)
        samples.extend([0.0] * int(sample_rate * 0.04))
    return samples

def create_tail_wipe_samples(sample_rate=44100):
    samples = []
    for swish in range(4):
        tot = int(sample_rate * 0.22)
        for i in range(tot):
            t = i / tot
            noise = (random.random() * 2.0 - 1.0)
            env = math.sin(math.pi * t)
            samples.append(noise * env * 0.35)
        samples.extend([0.0] * int(sample_rate * 0.05))
    return samples

def create_thud_samples(pitch_scale=1.0, duration=0.18, sample_rate=44100):
    total_samples = int(sample_rate * duration)
    samples = []
    base_f = 145.0 * pitch_scale
    for i in range(total_samples):
        t = i / duration / sample_rate
        f = max(42.0, base_f * (1.0 - t * 0.75))
        env = (1.0 - t) ** 1.9
        pop = math.sin(2 * math.pi * f * (i / sample_rate))
        chirp = 0.25 * math.sin(2 * math.pi * 580.0 * (i / sample_rate)) * ((1.0 - t) ** 4.0)
        samples.append((pop * 0.85 + chirp) * env)
    return samples

def build_all_sounds():
    ensure_sounds_directory()
    write_wav(os.path.join(SOUNDS_DIR, "cute_meow.wav"), create_cute_meow_samples())
    write_wav(os.path.join(SOUNDS_DIR, "happy_meow.wav"), create_happy_meow_samples())
    write_wav(os.path.join(SOUNDS_DIR, "sad_meow.wav"), create_sad_meow_samples())
    write_wav(os.path.join(SOUNDS_DIR, "angry_hiss.wav"), create_angry_hiss_samples())
    write_wav(os.path.join(SOUNDS_DIR, "frightened_yowl.wav"), create_frightened_yowl_samples())
    write_wav(os.path.join(SOUNDS_DIR, "alarm_morning.wav"), create_alarm_meow_samples())
    write_wav(os.path.join(SOUNDS_DIR, "purr.wav"), create_purr_samples())
    write_wav(os.path.join(SOUNDS_DIR, "scratch.wav"), create_scratch_samples())
    write_wav(os.path.join(SOUNDS_DIR, "tail_wipe.wav"), create_tail_wipe_samples())
    write_wav(os.path.join(SOUNDS_DIR, "thud.wav"), create_thud_samples())

def play_audio_path(filepath):
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
        self.var_idx = 0

    def play_dynamic_variation(self, generator_fn):
        ensure_sounds_directory()
        pitch_scale = random.uniform(0.92, 1.08)
        samples = generator_fn(pitch_scale=pitch_scale)
        self.var_idx = (self.var_idx + 1) % 10
        var_path = os.path.join(SOUNDS_DIR, f"dynamic_var_{self.var_idx}.wav")
        write_wav(var_path, samples)
        play_audio_path(var_path)

    def happy(self, dynamic=True):
        if dynamic:
            self.play_dynamic_variation(create_happy_meow_samples)
        else:
            play_audio_path(os.path.join(SOUNDS_DIR, "happy_meow.wav"))

    def cute(self, dynamic=True):
        if dynamic:
            self.play_dynamic_variation(create_cute_meow_samples)
        else:
            play_audio_path(os.path.join(SOUNDS_DIR, "cute_meow.wav"))

    def sad(self, dynamic=True):
        if dynamic:
            self.play_dynamic_variation(create_sad_meow_samples)
        else:
            play_audio_path(os.path.join(SOUNDS_DIR, "sad_meow.wav"))

    def angry(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "angry_hiss.wav"))

    def frightened(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "frightened_yowl.wav"))

    def alarm(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "alarm_morning.wav"))

    def purr(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "purr.wav"))

    def scratch(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "scratch.wav"))

    def tail_wipe(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "tail_wipe.wav"))

    def thud(self):
        play_audio_path(os.path.join(SOUNDS_DIR, "thud.wav"))

sound_system = CatSoundSystem()

if __name__ == "__main__":
    print("Testing dynamic sound synthesis variations...")
    sound_system.cute(dynamic=True)
    time.sleep(0.5)
    sound_system.happy(dynamic=True)
    print("Sound system dynamic variations OK!")
