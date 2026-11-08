import sys
import os
import subprocess
import time

class WindowSensor:
    def __init__(self):
        self.last_mouse_pos = (0, 0)
        self.last_activity_time = time.time()
        self.cached_window_title = "Desktop"
        self.last_check_time = 0

    def get_active_window_title(self):
        now = time.time()
        if now - self.last_check_time < 1.0:
            return self.cached_window_title

        self.last_check_time = now
        title = ""

        try:
            if sys.platform.startswith("win"):
                import ctypes
                user32 = ctypes.windll.user32
                hwnd = user32.GetForegroundWindow()
                length = user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
            elif sys.platform == "darwin":
                cmd = "osascript -e 'tell application \"System Events\" to get name of first application process whose frontmost is true'"
                proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1.0)
                title = proc.stdout.strip()
            else:
                proc = subprocess.run(["xdotool", "getwindowfocus", "getwindowname"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1.0)
                title = proc.stdout.strip()
        except Exception:
            title = ""

        if not title:
            title = "Desktop"

        self.cached_window_title = title
        return title

    def classify_window(self, title):
        t = title.lower()

        if any(k in t for k in ["chatgpt", "claude", "gemini", "copilot", "perplexity", "deepseek"]):
            return "ai_tool"

        if any(k in t for k in ["code", "visual studio", "sublime", "vim", "nvim", "pycharm", "intellij", "terminal", "bash", "zsh", "powershell"]):
            return "coding"

        if any(k in t for k in ["youtube", "netflix", "twitch", "reddit", "twitter", "instagram", "tiktok", "gaming", "steam"]):
            return "entertainment"

        if any(k in t for k in ["discord", "slack", "telegram", "whatsapp", "teams", "messenger"]):
            return "chat"

        if any(k in t for k in ["docs", "doc", "documentation", "notion", "github", "stackoverflow", "wikipedia", "pdf", "learn", "tutorial", "book"]):
            return "study_docs"

        return "general"

    def update_mouse_activity(self, current_x, current_y):
        now = time.time()
        if (current_x, current_y) != self.last_mouse_pos:
            self.last_mouse_pos = (current_x, current_y)
            self.last_activity_time = now

    def get_idle_seconds(self):
        return max(0.0, time.time() - self.last_activity_time)

window_sensor = WindowSensor()

if __name__ == "__main__":
    print("Testing Window Sensor...")
    title = window_sensor.get_active_window_title()
    category = window_sensor.classify_window(title)
    print("Active Window Title:", title)
    print("Classified Category:", category)
    print("Idle Seconds:", window_sensor.get_idle_seconds())
