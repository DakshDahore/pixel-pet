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
        self.drag_history = []
        self.is_falling = False
        self.is_peeking_behind = False

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

    def get_floor_y(self):
        return self.screen_h - self.pet_h - 60

    def on_mouse_down(self, event):
        self.is_dragging = True
        self.is_falling = False
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.drag_history = [(time.time(), self.pos_x, self.pos_y)]
        abs_x = self.pos_x + event.x
        abs_y = self.pos_y + event.y
        window_sensor.update_mouse_activity(abs_x, abs_y)

    def on_mouse_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.pos_x += dx
        self.pos_y += dy
        self.pos_x = max(5, min(self.screen_w - self.pet_w - 5, self.pos_x))
        self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")

        now = time.time()
        self.drag_history.append((now, self.pos_x, self.pos_y))
        if len(self.drag_history) > 6:
            self.drag_history.pop(0)

        # Show held / dangling pose if moved more than a little
        if abs(dx) > 10 or abs(dy) > 10:
            if self.current_gesture not in ("peeking", "falling"):
                self.set_gesture("peeking")

        abs_x = self.pos_x + event.x
        abs_y = self.pos_y + event.y
        window_sensor.update_mouse_activity(abs_x, abs_y)

    def on_mouse_up(self, event):
        self.is_dragging = False
        abs_move = abs(event.x - self.drag_start_x) + abs(event.y - self.drag_start_y)

        # Quick click without significant movement
        if abs_move < 8:
            if self.is_peeking_behind:
                self.pop_out_from_hiding()
            else:
                self.on_pet_click()
            return

        # Calculate throw / fling velocity
        vx, vy = 0.0, 0.0
        if len(self.drag_history) >= 2:
            dt = self.drag_history[-1][0] - self.drag_history[0][0]
            if dt > 0.02:
                vx = (self.drag_history[-1][1] - self.drag_history[0][1]) / dt * 0.015
                vy = (self.drag_history[-1][2] - self.drag_history[0][2]) / dt * 0.015

        floor_y = self.get_floor_y()

        # If dropped very low at the taskbar, hide behind it
        if self.pos_y >= floor_y + 35:
            self.hide_behind_taskbar()
        # If released high up in midair, trigger Talking Tom gravity fall
        elif self.pos_y < floor_y - 25:
            self.start_falling_physics(vx=vx, vy=vy)
        else:
            self.pos_y = floor_y
            self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
            self.set_gesture("idle")

    def start_falling_physics(self, vx=0.0, vy=0.0):
        if self.is_tantrum_running:
            return
        self.is_falling = True
        self.set_gesture("falling")
        sound_system.frightened()
        self.show_bubble("Waaaaah!! Falling!! 🙀🐾", 2000)

        vx = max(-22.0, min(22.0, vx))
        vy = max(-15.0, min(25.0, vy))

        def _step(cur_vx, cur_vy):
            if not self.is_falling or self.is_dragging:
                return

            cur_vy += 2.8  # Gravity acceleration
            cur_vx *= 0.96 # Air drag
            cur_vy = min(cur_vy, 32.0) # Terminal velocity

            self.pos_x += int(cur_vx)
            self.pos_y += int(cur_vy)

            floor_y = self.get_floor_y()

            # Bounce off left / right screen edges
            if self.pos_x < 10:
                self.pos_x = 10
                cur_vx = -cur_vx * 0.6
            elif self.pos_x > self.screen_w - self.pet_w - 10:
                self.pos_x = self.screen_w - self.pet_w - 10
                cur_vx = -cur_vx * 0.6

            # Floor impact
            if self.pos_y >= floor_y:
                self.pos_y = floor_y
                self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
                self.is_falling = False
                self.trigger_landing_bounce()
                return

            self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
            self.root.after(20, lambda: _step(cur_vx, cur_vy))

        _step(vx, vy)

    def trigger_landing_bounce(self):
        sound_system.thud()
        sound_system.cute(dynamic=True)
        self.show_bubble("Oof! Cat landed on all 4 paws! 🐾", 2500)
        self.set_gesture("happy")

        # Squash and stretch impact
        orig_w, orig_h = self.pet_w, self.pet_h
        sw, sh = orig_w + 24, orig_h - 16
        tw, th = orig_w - 12, orig_h + 10

        self.root.geometry(f"{sw}x{sh}+{self.pos_x - 12}+{self.pos_y + 16}")

        def _stretch():
            self.root.geometry(f"{tw}x{th}+{self.pos_x + 6}+{self.pos_y - 10}")
            self.root.after(90, _restore)

        def _restore():
            self.root.geometry(f"{orig_w}x{orig_h}+{self.pos_x}+{self.pos_y}")
            self.set_gesture("idle")

        self.root.after(110, _stretch)

    def hide_behind_taskbar(self):
        self.is_falling = False
        self.is_peeking_behind = True
        floor_y = self.get_floor_y()
        self.pos_y = floor_y + 90
        self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
        self.set_gesture("peeking")
        self.show_bubble("*whisper* Shh! Hiding behind taskbar! Click me! 🐱", 4000)
        sound_system.cute(dynamic=True)

    def pop_out_from_hiding(self):
        self.is_peeking_behind = False
        floor_y = self.get_floor_y()
        self.pos_y = floor_y
        self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
        self.set_gesture("happy", 2500)
        sound_system.happy(dynamic=True)
        self.show_bubble("Peek-a-boo!! Found me! ^._.^", 2500)

    def toss_in_air(self):
        if self.is_tantrum_running or self.is_falling:
            return
        if self.is_peeking_behind:
            self.pop_out_from_hiding()
        self.start_falling_physics(vx=random.uniform(-4.0, 4.0), vy=-20.0)

    def hop_tiles(self):
        if self.is_tantrum_running or self.is_falling:
            return
        if self.is_peeking_behind:
            self.pop_out_from_hiding()

        floor_y = self.get_floor_y()
        self.set_gesture("happy")
        sound_system.cute(dynamic=True)
        self.show_bubble("Hopping across window tiles! 🐾", 3000)

        # 3 sequential jumps simulating hopping between window tiles
        hops = [
            (self.screen_w // 4, floor_y - 180),
            (self.screen_w // 2, floor_y - 120),
            (3 * self.screen_w // 4, floor_y)
        ]

        def _do_hop(hop_idx=0):
            if hop_idx >= len(hops):
                self.trigger_landing_bounce()
                return

            target_x, target_y = hops[hop_idx]
            start_x, start_y = self.pos_x, self.pos_y

            def _arc(step=0):
                if step <= 12:
                    t = step / 12.0
                    nx = int(start_x + (target_x - start_x) * t)
                    ny = int(start_y + (target_y - start_y) * t - math.sin(math.pi * t) * 70)
                    self.pos_x, self.pos_y = nx, ny
                    self.root.geometry(f"{self.pet_w}x{self.pet_h}+{nx}+{ny}")
                    self.root.after(30, lambda: _arc(step + 1))
                else:
                    sound_system.thud()
                    self.set_gesture("happy")
                    self.root.after(400, lambda: _do_hop(hop_idx + 1))

            _arc()

        _do_hop()

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

    def feed_fish_treat(self):
        if self.is_tantrum_running:
            return
        self.set_gesture("eating", 3500)
        sound_system.cute(dynamic=True)
        self.show_bubble("Nom nom nom! Crunchy fish treat! 🐟✨", 3500)
        if self.tracker:
            self.tracker.record_petting()

    def patrol_walk(self, distance=70):
        if self.is_tantrum_running or self.is_dragging or (self.tracker and self.tracker.is_sleeping):
            return

        direction = -1 if (self.pos_x > self.screen_w // 2) else 1
        self.set_gesture("walking")

        def _step(step_count=0):
            if step_count < 14:
                self.pos_x += direction * 5
                self.pos_x = max(10, min(self.screen_w - self.pet_w - 10, self.pos_x))
                self.root.geometry(f"{self.pet_w}x{self.pet_h}+{self.pos_x}+{self.pos_y}")
                self.root.after(90, lambda: _step(step_count + 1))
            else:
                self.set_gesture("idle")
                self.show_bubble("Stretch stretch! Paws feel good. :3", 2500)

        _step()

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
