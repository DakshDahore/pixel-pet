import tkinter as tk
import time
import math
import random
import sys
from sprites import sprite_manager
from sound_player import sound_system
from window_sensor import window_sensor

class DesktopPetWindow:
    def __init__(self, root, tracker=None):
        self.root = root
        self.tracker = tracker

        self.root.title("Pixel Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        self.bg_color = "#010101"
        if sys.platform.startswith("win"):
            self.root.attributes("-transparentcolor", self.bg_color)
        else:
            try:
                self.root.attributes("-alpha", 0.95)
            except Exception:
                pass

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.pet_w = 192
        self.pet_h = 240
        self.pos_x = self.screen_w - self.pet_w - 40
        self.pos_y = self.screen_h - self.pet_h - 60

        self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
        self.root.configure(bg=self.bg_color)

        self.canvas = tk.Canvas(
            self.root,
            width=self.pet_w,
            height=self.pet_h,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.current_gesture = "idle"
        self.frame_idx = 0
        self.speech_text = ""
        self.speech_timer = 0

        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.is_tantrum_running = False
        self.scratch_window = None

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Button-3>", self.open_control_panel)
        self.canvas.bind("<Double-Button-1>", self.open_control_panel)
        self.canvas.bind("<Motion>", self.on_mouse_hover)

        self.control_panel_callback = None

        self.show_bubble("Hello! I'm your Pixel Pet! *meow*", 4000)
        sound_system.happy(dynamic=True)

        self.animate_loop()

    def set_control_panel_callback(self, cb):
        self.control_panel_callback = cb

    def open_control_panel(self, event=None):
        if self.control_panel_callback:
            self.control_panel_callback()

    def on_mouse_hover(self, event):
        abs_x = self.pos_x + event.x
        abs_y = self.pos_y + event.y
        window_sensor.update_mouse_activity(abs_x, abs_y)

    def on_mouse_down(self, event):
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        abs_x = self.pos_x + event.x
        abs_y = self.pos_y + event.y
        window_sensor.update_mouse_activity(abs_x, abs_y)

    def on_mouse_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.pos_x += dx
        self.pos_y += dy
        self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
        abs_x = self.pos_x + event.x
        abs_y = self.pos_y + event.y
        window_sensor.update_mouse_activity(abs_x, abs_y)

    def on_mouse_up(self, event):
        self.is_dragging = False
        if abs(event.x - self.drag_start_x) < 4 and abs(event.y - self.drag_start_y) < 4:
            self.on_pet_click()

    def on_pet_click(self):
        if self.is_tantrum_running:
            return

        self.set_gesture("petted", 2500)
        sound_system.purr()
        sound_system.cute(dynamic=True)
        self.show_bubble("Purrrrr~ Love you! ^._.^", 2500)

        if self.tracker:
            self.tracker.record_petting()
            if self.tracker.alarm_ringing:
                self.tracker.dismiss_alarm()

    def set_gesture(self, gesture_name, duration_ms=0):
        self.current_gesture = gesture_name
        self.frame_idx = 0

        if duration_ms > 0:
            def _reset():
                if self.current_gesture == gesture_name and not self.is_tantrum_running:
                    self.current_gesture = "idle"
            self.root.after(duration_ms, _reset)

    def show_bubble(self, message, duration_ms=3500):
        self.speech_text = message
        self.speech_timer = duration_ms

    def draw_speech_bubble(self):
        if not self.speech_text or self.speech_timer <= 0:
            return

        text = self.speech_text
        bx, by = 16, 10
        bw, bh = self.pet_w - 32, 52

        self.canvas.create_rectangle(bx, by, bx + bw, by + bh, fill="#ffffff", outline="#1e1b4b", width=2)
        self.canvas.create_polygon([(bx + 30, by + bh), (bx + 40, by + bh), (bx + 32, by + bh + 10)], fill="#ffffff", outline="#1e1b4b")
        self.canvas.create_line(bx + 31, by + bh, bx + 39, by + bh, fill="#ffffff", width=2)

        self.canvas.create_text(
            bx + bw // 2,
            by + bh // 2,
            text=text,
            fill="#0f172a",
            font=("Helvetica", 9, "bold"),
            width=bw - 12
        )

    def trigger_dramatic_scratch_event(self):
        if self.is_tantrum_running:
            return
        self.is_tantrum_running = True

        center_x = (self.screen_w // 2) - (self.pet_w // 2)
        center_y = (self.screen_h // 2) - (self.pet_h // 2)
        start_x, start_y = self.pos_x, self.pos_y

        self.show_bubble("HEY! BREAK TIME NOW!!", 2000)
        self.set_gesture("angry")
        sound_system.angry()

        def move_to_center(step=0):
            if step <= 10:
                t = step / 10.0
                nx = int(start_x + (center_x - start_x) * t)
                ny = int(start_y + (center_y - start_y) * t)
                self.pos_x, self.pos_y = nx, ny
                self.root.geometry(f"{self.pet_w}x{self.pet_h}+{nx}+{ny}")
                self.root.after(40, lambda: move_to_center(step + 1))
            else:
                scratch_the_screen()

        def scratch_the_screen():
            self.set_gesture("scratching")
            sound_system.scratch()

            self.scratch_window = tk.Toplevel(self.root)
            self.scratch_window.overrideredirect(True)
            self.scratch_window.attributes("-topmost", True)
            if sys.platform.startswith("win"):
                self.scratch_window.attributes("-transparentcolor", "#010101")
            sw, sh = 340, 260
            sx = (self.screen_w // 2) - (sw // 2)
            sy = (self.screen_h // 2) - (sh // 2)
            self.scratch_window.geometry(f"{sw}x{sh}+{sx}+{sy}")
            self.scratch_window.configure(bg="#010101")

            scratch_canvas = tk.Canvas(self.scratch_window, width=sw, height=sh, bg="#010101", highlightthickness=0)
            scratch_canvas.pack(fill=tk.BOTH, expand=True)
            self.scratch_img = sprite_manager.get_scratch_tk_image()
            scratch_canvas.create_image(sw // 2, sh // 2, image=self.scratch_img)

            self.root.after(1000, cat_panics)

        def cat_panics():
            self.set_gesture("frightened")
            sound_system.frightened()
            self.show_bubble("O_O OH NO!! WHAT DID I DO?!", 1800)

            def scramble_away(step=0):
                if step <= 12:
                    self.pos_x -= 18
                    self.pos_y += 12
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
                    self.root.after(30, lambda: scramble_away(step + 1))
                else:
                    self.root.after(1000, cat_returns_with_tail)

            scramble_away()

        def cat_returns_with_tail():
            self.show_bubble("...wait, I can fix it!", 2000)
            self.set_gesture("peeking")

            def sneak_back(step=0):
                if step <= 10:
                    t = step / 10.0
                    target_x = center_x + 30
                    target_y = center_y
                    self.pos_x = int(self.pos_x + (target_x - self.pos_x) * 0.2)
                    self.pos_y = int(self.pos_y + (target_y - self.pos_y) * 0.2)
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
                    self.root.after(50, lambda: sneak_back(step + 1))
                else:
                    wipe_screen_with_big_tail()

            sneak_back()

        def wipe_screen_with_big_tail():
            self.set_gesture("happy")
            sound_system.tail_wipe()

            def tail_swish(swish_count=0):
                if swish_count < 6:
                    offset = 20 if (swish_count % 2 == 0) else -20
                    self.pos_x = center_x + offset
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
                    self.root.after(250, lambda: tail_swish(swish_count + 1))
                else:
                    clean_up()

            tail_swish()

        def clean_up():
            if self.scratch_window:
                self.scratch_window.destroy()
                self.scratch_window = None

            sound_system.cute(dynamic=True)
            self.set_gesture("petted")
            self.show_bubble("All clean! Like nothing happened :3", 3000)

            def return_to_corner(step=0):
                if step <= 14:
                    t = step / 14.0
                    nx = int(self.pos_x + (start_x - self.pos_x) * 0.2)
                    ny = int(self.pos_y + (start_y - self.pos_y) * 0.2)
                    self.pos_x, self.pos_y = nx, ny
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{nx}+{ny}")
                    self.root.after(40, lambda: return_to_corner(step + 1))
                else:
                    self.pos_x, self.pos_y = start_x, start_y
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{start_x}+{start_y}")
                    self.is_tantrum_running = False
                    self.set_gesture("idle")

            self.root.after(1500, return_to_corner)

        move_to_center()

    def animate_loop(self):
        self.canvas.delete("all")

        tk_img = sprite_manager.get_tk_image(self.current_gesture, self.frame_idx)
        cat_y = 120
        self.canvas.create_image(self.pet_w // 2, cat_y, image=tk_img)

        self.draw_speech_bubble()

        self.frame_idx = (self.frame_idx + 1) % 16
        if self.speech_timer > 0:
            self.speech_timer -= 150

        try:
            cur_x, cur_y = self.root.winfo_pointerxy()
            window_sensor.update_mouse_activity(cur_x, cur_y)
        except Exception:
            pass

        self.root.after(150, self.animate_loop)
