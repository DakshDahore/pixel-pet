import time
import json
import os
import sys
import threading
from datetime import datetime
from window_sensor import window_sensor
from neural_brain import neural_brain

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pet_config.json")

DEFAULT_CONFIG = {
    "work_duration_minutes": 25,
    "short_break_minutes": 5,
    "water_interval_minutes": 30,
    "bedtime": "23:00",
    "wake_time": "07:00",
    "alarm_enabled": True,
    "ai_watcher_enabled": True,
    "neural_brain_enabled": True,
    "battery_guard_enabled": True,
    "eye_strain_20_20_enabled": True,
    "sound_enabled": True,
    "cat_name": "Kuro",
    "eye_color": "green",
    "total_work_seconds": 0,
    "water_glasses_logged": 0,
    "breaks_taken": 0
}

def get_battery_info():
    try:
        if sys.platform.startswith("linux"):
            bat_path = "/sys/class/power_supply/BAT0"
            if os.path.exists(bat_path):
                cap_file = os.path.join(bat_path, "capacity")
                stat_file = os.path.join(bat_path, "status")
                with open(cap_file, "r") as f:
                    capacity = int(f.read().strip())
                with open(stat_file, "r") as f:
                    status = f.read().strip()
                return capacity, status
        elif sys.platform.startswith("win"):
            import ctypes
            class SYSTEM_POWER_STATUS(ctypes.Structure):
                _fields_ = [
                    ('ACLineStatus', ctypes.c_byte),
                    ('BatteryFlag', ctypes.c_byte),
                    ('BatteryLifePercent', ctypes.c_byte),
                    ('Reserved1', ctypes.c_byte),
                    ('BatteryLifeTime', ctypes.c_ulong),
                    ('BatteryFullLifeTime', ctypes.c_ulong)
                ]
            sps = SYSTEM_POWER_STATUS()
            if ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sps)):
                pct = int(sps.BatteryLifePercent)
                stat = "Charging" if sps.ACLineStatus == 1 else "Discharging"
                return pct, stat
    except Exception:
        pass
    return None, None

class ScreenTimeTracker:
    def __init__(self, on_state_change=None, on_notification=None, on_neural_action=None):
        self.config = self.load_config()
        self.on_state_change = on_state_change
        self.on_notification = on_notification
        self.on_neural_action = on_neural_action

        self.session_seconds = 0
        self.total_seconds = self.config.get("total_work_seconds", 0)
        self.water_timer_seconds = 0
        self.eye_strain_timer_seconds = 0

        self.current_state = "working"
        self.escalation_level = 0
        self.break_overdue_seconds = 0

        self.is_sleeping = False
        self.alarm_ringing = False

        self.last_clipboard_text = ""
        self.ai_watching = self.config.get("ai_watcher_enabled", True)
        self.neural_enabled = self.config.get("neural_brain_enabled", True)
        self.last_battery_alert = 0
        self.last_battery_status = ""

        self.last_window_category = "general"
        self.last_neural_decision_time = time.time()
        self.current_neural_action = "idle_watch"

        self.running = True
        self.worker_thread = threading.Thread(target=self._tracker_loop, daemon=True)
        self.clipboard_thread = threading.Thread(target=self._clipboard_loop, daemon=True)

        self.worker_thread.start()
        self.clipboard_thread.start()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    cfg = dict(DEFAULT_CONFIG)
                    cfg.update(data)
                    return cfg
            except Exception:
                return dict(DEFAULT_CONFIG)
        return dict(DEFAULT_CONFIG)

    def save_config(self):
        try:
            self.config["total_work_seconds"] = self.total_seconds
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def get_remaining_work_seconds(self):
        limit = self.config["work_duration_minutes"] * 60
        return max(0, limit - self.session_seconds)

    def take_break(self):
        self.current_state = "on_break"
        self.escalation_level = 0
        self.break_overdue_seconds = 0
        self.eye_strain_timer_seconds = 0
        self.config["breaks_taken"] = self.config.get("breaks_taken", 0) + 1
        self.save_config()
        neural_brain.learn_from_break_taken()
        if self.on_state_change:
            self.on_state_change("happy", "Good job taking a break! Relax your eyes~")

    def resume_work(self):
        self.current_state = "working"
        self.session_seconds = 0
        self.escalation_level = 0
        self.break_overdue_seconds = 0
        self.eye_strain_timer_seconds = 0
        if self.on_state_change:
            self.on_state_change("idle", "Back to work! I'll keep watch for you.")

    def log_water_drink(self):
        self.config["water_glasses_logged"] = self.config.get("water_glasses_logged", 0) + 1
        self.water_timer_seconds = 0
        self.save_config()
        neural_brain.learn_from_break_taken()
        if self.on_state_change:
            self.on_state_change("petted", "Gulp gulp! Stay hydrated! Good job! :3")

    def record_petting(self):
        neural_brain.learn_from_petting()

    def check_time_schedules(self):
        now_str = datetime.now().strftime("%H:%M")
        bedtime = self.config.get("bedtime", "23:00")
        wake_time = self.config.get("wake_time", "07:00")

        if now_str == bedtime and not self.is_sleeping:
            self.is_sleeping = True
            if self.on_state_change:
                self.on_state_change("sleeping", "Bedtime! Time to rest your eyes... Zzz")

        if now_str == wake_time and self.is_sleeping and self.config.get("alarm_enabled", True):
            self.is_sleeping = False
            self.alarm_ringing = True
            if self.on_state_change:
                self.on_state_change("alarm", "Wake up! Good morning! Rise and shine! *meow*")

    def dismiss_alarm(self):
        self.alarm_ringing = False
        self.is_sleeping = False
        if self.on_state_change:
            self.on_state_change("happy", "Yay! Have a wonderful day today!")

    def check_battery_guard(self):
        if not self.config.get("battery_guard_enabled", True):
            return

        cap, stat = get_battery_info()
        if cap is None:
            return

        now = time.time()
        if stat == "Discharging" and cap <= 20 and (now - self.last_battery_alert > 300):
            self.last_battery_alert = now
            if self.on_notification:
                self.on_notification("battery_low", f"Battery low at {cap}%! Plug in charger! ⚡")
        elif stat == "Charging" and self.last_battery_status == "Discharging":
            if self.on_notification:
                self.on_notification("battery_charging", "Charger connected! Power restored! ⚡:3")

        self.last_battery_status = stat

    def evaluate_neural_brain(self):
        now = time.time()
        if now - self.last_neural_decision_time < 12.0:
            return

        self.last_neural_decision_time = now

        title = window_sensor.get_active_window_title()
        category = window_sensor.classify_window(title)
        self.last_window_category = category
        idle_sec = window_sensor.get_idle_seconds()

        cat_scores = {
            "coding": 0.9,
            "study_docs": 0.7,
            "ai_tool": 0.85,
            "entertainment": 0.25,
            "chat": 0.45,
            "general": 0.5
        }
        score_context = cat_scores.get(category, 0.5)

        work_limit = max(1, self.config["work_duration_minutes"] * 60)
        norm_work = self.session_seconds / float(work_limit)
        norm_idle = min(1.0, idle_sec / 300.0)

        current_hour = datetime.now().hour + datetime.now().minute / 60.0
        norm_circadian = current_hour / 24.0

        water_limit = max(1, self.config["water_interval_minutes"] * 60)
        norm_thirst = min(1.0, self.water_timer_seconds / float(water_limit))

        inputs = [
            score_context,
            norm_work,
            norm_idle,
            norm_circadian,
            norm_thirst,
            neural_brain.affection,
            neural_brain.tantrum_fatigue
        ]

        action, probs = neural_brain.forward(inputs)
        self.current_neural_action = action
        neural_brain.decay_tantrum_fatigue()

        if self.on_neural_action:
            self.on_neural_action(action, category, title, probs)

    def _tracker_loop(self):
        battery_tick_counter = 0

        while self.running:
            idle_sec = window_sensor.get_idle_seconds()
            sleep_interval = 2.0 if idle_sec > 300 or self.is_sleeping else 1.0
            time.sleep(sleep_interval)

            elapsed_step = int(sleep_interval)
            self.check_time_schedules()

            battery_tick_counter += elapsed_step
            if battery_tick_counter >= 30:
                battery_tick_counter = 0
                self.check_battery_guard()

            if self.is_sleeping:
                continue

            self.session_seconds += elapsed_step
            self.total_seconds += elapsed_step
            self.water_timer_seconds += elapsed_step
            self.eye_strain_timer_seconds += elapsed_step

            if self.config.get("eye_strain_20_20_enabled", True) and self.eye_strain_timer_seconds >= 1200:
                self.eye_strain_timer_seconds = 0
                if self.on_notification:
                    self.on_notification("eye_strain", "20-20-20 Rule: Look 20 feet away for 20s to rest your eyes! 👀")

            work_limit = self.config["work_duration_minutes"] * 60
            water_limit = self.config["water_interval_minutes"] * 60

            if self.water_timer_seconds >= water_limit:
                self.water_timer_seconds = 0
                if self.on_notification:
                    self.on_notification("water", "Time for a sip of water! Stay hydrated!")

            if self.neural_enabled:
                self.evaluate_neural_brain()
            elif self.current_state == "working":
                if self.session_seconds > work_limit:
                    self.break_overdue_seconds = self.session_seconds - work_limit
                    self._update_escalation()

    def _update_escalation(self):
        overdue_min = self.break_overdue_seconds / 60.0

        if overdue_min < 1.0 and self.escalation_level != 1:
            self.escalation_level = 1
            if self.on_state_change:
                self.on_state_change("empathy", "Time for a quick break! Please rest your eyes :3")
        elif 1.0 <= overdue_min < 2.5 and self.escalation_level != 2:
            self.escalation_level = 2
            if self.on_state_change:
                self.on_state_change("sad", "You've been staring at the screen for so long...")
        elif 2.5 <= overdue_min < 4.0 and self.escalation_level != 3:
            self.escalation_level = 3
            if self.on_state_change:
                self.on_state_change("angry", "Hey! Look away from the screen right now!")
        elif 4.0 <= overdue_min < 5.5 and self.escalation_level != 4:
            self.escalation_level = 4
            if self.on_state_change:
                self.on_state_change("turned", "Humph! I'm ignoring you since you won't listen!")
        elif overdue_min >= 5.5 and self.escalation_level != 5:
            self.escalation_level = 5
            if self.on_state_change:
                self.on_state_change("dramatic_tantrum", "THAT'S IT! TIME FOR A BREAK!!")

    def _clipboard_loop(self):
        while self.running:
            time.sleep(1.5)
            if not self.ai_watching:
                continue

            try:
                import tkinter as tk
                t_root = tk.Tk()
                t_root.withdraw()
                text = t_root.clipboard_get()
                t_root.destroy()

                if text and text != self.last_clipboard_text:
                    if len(text.strip()) > 30 and self.last_clipboard_text != "":
                        self.last_clipboard_text = text
                        if self.on_notification:
                            self.on_notification("ai_ready", "You're up! AI has finished generating your answer! 🐱✨")
                    else:
                        self.last_clipboard_text = text
            except Exception:
                pass
