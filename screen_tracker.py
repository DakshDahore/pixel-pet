import time
import json
import os
import threading
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pet_config.json")

DEFAULT_CONFIG = {
    "work_duration_minutes": 25,
    "short_break_minutes": 5,
    "water_interval_minutes": 30,
    "bedtime": "23:00",
    "wake_time": "07:00",
    "alarm_enabled": True,
    "ai_watcher_enabled": True,
    "sound_enabled": True,
    "cat_name": "Kuro",
    "eye_color": "green",
    "total_work_seconds": 0,
    "water_glasses_logged": 0,
    "breaks_taken": 0
}

class ScreenTimeTracker:
    def __init__(self, on_state_change=None, on_notification=None):
        self.config = self.load_config()
        self.on_state_change = on_state_change
        self.on_notification = on_notification

        self.session_seconds = 0
        self.total_seconds = self.config.get("total_work_seconds", 0)
        self.water_timer_seconds = 0

        self.current_state = "working"
        self.escalation_level = 0
        self.break_overdue_seconds = 0

        self.is_sleeping = False
        self.alarm_ringing = False

        self.last_clipboard_text = ""
        self.ai_watching = self.config.get("ai_watcher_enabled", True)

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
        self.config["breaks_taken"] = self.config.get("breaks_taken", 0) + 1
        self.save_config()
        if self.on_state_change:
            self.on_state_change("happy", "Good job taking a break! Relax your eyes~")

    def resume_work(self):
        self.current_state = "working"
        self.session_seconds = 0
        self.escalation_level = 0
        self.break_overdue_seconds = 0
        if self.on_state_change:
            self.on_state_change("idle", "Back to work! I'll keep watch for you.")

    def log_water_drink(self):
        self.config["water_glasses_logged"] = self.config.get("water_glasses_logged", 0) + 1
        self.water_timer_seconds = 0
        self.save_config()
        if self.on_state_change:
            self.on_state_change("petted", "Gulp gulp! Stay hydrated! Good job! :3")

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

    def _tracker_loop(self):
        while self.running:
            time.sleep(1.0)
            self.check_time_schedules()

            if self.is_sleeping:
                continue

            self.session_seconds += 1
            self.total_seconds += 1
            self.water_timer_seconds += 1

            work_limit = self.config["work_duration_minutes"] * 60
            water_limit = self.config["water_interval_minutes"] * 60

            if self.water_timer_seconds >= water_limit:
                self.water_timer_seconds = 0
                if self.on_notification:
                    self.on_notification("water", "Time for a sip of water! Stay hydrated!")

            if self.current_state == "working":
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
        try:
            import tkinter as tk
            root = None
        except Exception:
            return

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
