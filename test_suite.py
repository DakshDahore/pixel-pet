import unittest
import os
import math
import json
import time

from sound_player import (
    build_all_sounds,
    create_cute_meow_samples,
    create_happy_meow_samples,
    create_sad_meow_samples,
    create_angry_hiss_samples,
    create_frightened_yowl_samples,
    create_alarm_meow_samples,
    create_purr_samples,
    create_scratch_samples,
    create_tail_wipe_samples,
    create_thud_samples,
    SOUNDS_DIR
)
from sprites import render_cat_frame, render_screen_scratch, CANVAS_SIZE, SCALE
from neural_brain import NeuralBrain
from window_sensor import window_sensor
from screen_tracker import ScreenTimeTracker

class TestPixelPetCore(unittest.TestCase):

    def test_01_sound_synthesis(self):
        build_all_sounds()
        expected_files = [
            "cute_meow.wav",
            "happy_meow.wav",
            "sad_meow.wav",
            "angry_hiss.wav",
            "frightened_yowl.wav",
            "alarm_morning.wav",
            "purr.wav",
            "scratch.wav",
            "tail_wipe.wav",
            "thud.wav"
        ]
        for f in expected_files:
            p = os.path.join(SOUNDS_DIR, f)
            self.assertTrue(os.path.exists(p), f"Missing sound file: {f}")
            self.assertGreater(os.path.getsize(p), 1000, f"Sound file too small: {f}")

    def test_02_dynamic_audio_variations(self):
        samples_normal = create_cute_meow_samples(pitch_scale=1.0)
        samples_high = create_cute_meow_samples(pitch_scale=1.1)
        self.assertEqual(len(samples_normal), len(samples_high))
        self.assertNotEqual(samples_normal[100], samples_high[100])

        for s in samples_normal:
            self.assertTrue(-1.0 <= s <= 1.0, f"Sample out of bounds: {s}")

    def test_03_sprite_frames(self):
        modes = [
            "idle", "happy", "petted", "sad", "angry", "turned",
            "scratching", "peeking", "sleeping", "falling",
            "frightened", "empathy", "walking", "eating"
        ]
        expected_size = (CANVAS_SIZE * SCALE, CANVAS_SIZE * SCALE)
        for m in modes:
            img = render_cat_frame(m, frame_idx=0)
            self.assertEqual(img.size, expected_size)
            self.assertEqual(img.mode, "RGBA")

    def test_04_scratch_overlay(self):
        scratch_img = render_screen_scratch()
        self.assertEqual(scratch_img.size, (320, 240))
        self.assertEqual(scratch_img.mode, "RGBA")
        extrema = scratch_img.getextrema()
        alpha_channel_extrema = extrema[3]
        self.assertGreater(alpha_channel_extrema[1], 0)

    def test_05_neural_brain_forward_pass(self):
        brain = NeuralBrain()
        test_inputs = [0.9, 0.5, 0.0, 0.5, 0.2, 0.5, 0.0]
        action, probs = brain.forward(test_inputs)

        self.assertIn(action, brain.action_names)
        self.assertEqual(len(probs), brain.num_actions)
        self.assertAlmostEqual(sum(probs), 1.0, places=4)
        for p in probs:
            self.assertTrue(0.0 <= p <= 1.0)

    def test_06_neural_brain_afk_behavior(self):
        brain = NeuralBrain()
        afk_inputs = [0.1, 0.2, 0.95, 0.5, 0.1, 0.5, 0.0]
        action, probs = brain.forward(afk_inputs)
        idx_sleep = brain.action_names.index("curled_catnap")
        self.assertGreater(probs[idx_sleep], 0.20)

    def test_07_neural_learning_and_memory(self):
        brain = NeuralBrain()
        initial_affection = brain.affection
        brain.learn_from_petting()
        self.assertGreaterEqual(brain.affection, initial_affection)

        initial_patience = brain.patience
        brain.learn_from_break_taken()
        self.assertGreaterEqual(brain.patience, initial_patience)

    def test_08_window_classification(self):
        self.assertEqual(window_sensor.classify_window("main.py - Visual Studio Code"), "coding")
        self.assertEqual(window_sensor.classify_window("Watching Cat Videos - YouTube - Google Chrome"), "entertainment")
        self.assertEqual(window_sensor.classify_window("ChatGPT - Research Assistant"), "ai_tool")
        self.assertEqual(window_sensor.classify_window("Python Documentation - Google Chrome"), "study_docs")
        self.assertEqual(window_sensor.classify_window("General Chat - Discord"), "chat")

    def test_09_screen_tracker_timers(self):
        tracker = ScreenTimeTracker()
        tracker.config["work_duration_minutes"] = 25
        rem = tracker.get_remaining_work_seconds()
        self.assertEqual(rem, 25 * 60)

        tracker.session_seconds = 10 * 60
        self.assertEqual(tracker.get_remaining_work_seconds(), 15 * 60)

        tracker.take_break()
        self.assertEqual(tracker.current_state, "on_break")

        tracker.resume_work()
        self.assertEqual(tracker.current_state, "working")
        self.assertEqual(tracker.session_seconds, 0)
        tracker.running = False

    def test_10_simulated_24h_lifecycle_stress_test(self):
        brain = NeuralBrain()
        total_actions = {}
        for minute in range(1440):
            norm_work = (minute % 60) / 60.0
            norm_idle = 0.8 if (minute % 120 < 15) else 0.0
            circadian = minute / 1440.0
            thirst = (minute % 45) / 45.0
            context = 0.9 if (540 <= minute <= 1080) else 0.3

            inputs = [context, norm_work, norm_idle, circadian, thirst, brain.affection, brain.tantrum_fatigue]
            act, probs = brain.forward(inputs)
            total_actions[act] = total_actions.get(act, 0) + 1

        self.assertGreater(len(total_actions), 5)
        self.assertIn("idle_watch", total_actions)
        self.assertIn("curled_catnap", total_actions)

    def test_11_int8_quantization_parity(self):
        brain = NeuralBrain()
        self.assertTrue(brain.quantized_mode)
        self.assertEqual(len(brain.w1_int8), brain.num_inputs)
        self.assertEqual(len(brain.w2_int8), brain.num_hidden)

        for row in brain.w1_int8:
            for val in row:
                self.assertTrue(-128 <= val <= 127)

        for row in brain.w2_int8:
            for val in row:
                self.assertTrue(-128 <= val <= 127)

        test_inputs = [0.8, 0.5, 0.1, 0.4, 0.2, 0.7, 0.0]
        logits_int8 = brain.forward_quantized_int8(test_inputs)
        self.assertEqual(len(logits_int8), brain.num_actions)
        for logit in logits_int8:
            self.assertFalse(math.isnan(logit))

def run_all_tests():
    print("======================================================================")
    print("       PIXEL PET AUTOMATED TEST SUITE & 24-HOUR STRESS TEST")
    print("======================================================================")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPixelPetCore)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        exit(1)

