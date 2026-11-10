import tkinter as tk
from tkinter import ttk, messagebox
import sound_player
from sound_player import sound_system
from neural_brain import neural_brain
from window_sensor import window_sensor
import sprites

class ControlPanelWindow:
    def __init__(self, root, tracker, pet_window):
        self.root = root
        self.tracker = tracker
        self.pet_window = pet_window

        self.win = tk.Toplevel(self.root)
        self.win.title("Pixel Pet - Companion & Neural Brain App")
        self.win.geometry("560x740")
        self.win.configure(bg="#0f172a")

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()
        self.update_stats_loop()

    def build_ui(self):
        title_frame = tk.Frame(self.win, bg="#1e293b", pady=12)
        title_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            title_frame,
            text="🐱 Pixel Pet Companion & Neural Brain",
            font=("Helvetica", 15, "bold"),
            bg="#1e293b",
            fg="#f8fafc"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            title_frame,
            text="Desktop Health, Adaptive Cognitive Brain & Screen Guardian",
            font=("Helvetica", 9),
            bg="#1e293b",
            fg="#94a3b8"
        )
        subtitle_lbl.pack()

        content_canvas = tk.Canvas(self.win, bg="#0f172a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.win, orient="vertical", command=content_canvas.yview)
        scroll_frame = tk.Frame(content_canvas, bg="#0f172a")

        scroll_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )

        content_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=540)
        content_canvas.configure(yscrollcommand=scrollbar.set)

        content_canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y")

        self.build_neural_brain_section(scroll_frame)
        self.build_timer_section(scroll_frame)
        self.build_customizer_section(scroll_frame)
        self.build_hydration_section(scroll_frame)
        self.build_sleep_alarm_section(scroll_frame)
        self.build_ai_watcher_section(scroll_frame)
        self.build_gesture_studio_section(scroll_frame)
        self.build_parkour_section(scroll_frame)
        self.build_soundboard_section(scroll_frame)
        self.build_stats_section(scroll_frame)

    def build_neural_brain_section(self, parent):
        box = tk.LabelFrame(parent, text="🧠 Neural Cognitive Brain (Adaptive AI)", bg="#1e293b", fg="#a855f7", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        self.brain_var = tk.BooleanVar(value=self.tracker.neural_enabled)
        chk = tk.Checkbutton(
            box,
            text="Enable Autonomous Neural Brain (predicts behavior via app, habit & idle)",
            variable=self.brain_var,
            bg="#1e293b",
            fg="#cbd5e1",
            selectcolor="#0f172a",
            activebackground="#1e293b",
            activeforeground="#c084fc",
            command=self.toggle_neural_brain
        )
        chk.pack(anchor="w", pady=2)

        self.brain_stats_lbl = tk.Label(
            box,
            text="Brain Status: Initializing...",
            bg="#1e293b",
            fg="#e2e8f0",
            font=("Monospace", 9),
            justify=tk.LEFT
        )
        self.brain_stats_lbl.pack(anchor="w", pady=4)

        rethink_btn = tk.Button(box, text="⚡ Force Neural Brain Evaluation", bg="#7e22ce", fg="#ffffff", font=("Helvetica", 9, "bold"), command=self.force_neural_eval)
        rethink_btn.pack(anchor="w", pady=4)

    def build_customizer_section(self, parent):
        box = tk.LabelFrame(parent, text="🎨 Cat Customizer (Breed, Eyes & Coat)", bg="#1e293b", fg="#ec4899", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        row_breed = tk.Frame(box, bg="#1e293b")
        row_breed.pack(fill=tk.X, pady=3)

        tk.Label(row_breed, text="Cat Breed:", bg="#1e293b", fg="#cbd5e1", width=12, anchor="w").pack(side=tk.LEFT)

        breeds = [
            ("Midnight", "black", "#1e1b4b"),
            ("Orange", "orange", "#ea580c"),
            ("Snow", "white", "#64748b"),
            ("Siamese", "siamese", "#78350f"),
            ("Calico", "calico", "#0d9488")
        ]
        for label, b_key, b_color in breeds:
            btn = tk.Button(
                row_breed,
                text=label,
                bg=b_color,
                fg="#ffffff",
                font=("Helvetica", 8, "bold"),
                command=lambda k=b_key: self.change_cat_breed(k)
            )
            btn.pack(side=tk.LEFT, padx=2)

        row = tk.Frame(box, bg="#1e293b")
        row.pack(fill=tk.X, pady=3)

        tk.Label(row, text="Eye Color:", bg="#1e293b", fg="#cbd5e1", width=12, anchor="w").pack(side=tk.LEFT)

        btn_green = tk.Button(row, text="Jiji Green", bg="#16a34a", fg="#ffffff", font=("Helvetica", 8, "bold"), command=lambda: self.change_eye_color("green"))
        btn_green.pack(side=tk.LEFT, padx=3)

        btn_blue = tk.Button(row, text="Fluffy Blue", bg="#0284c7", fg="#ffffff", font=("Helvetica", 8, "bold"), command=lambda: self.change_eye_color("blue"))
        btn_blue.pack(side=tk.LEFT, padx=3)

        btn_amber = tk.Button(row, text="Golden Amber", bg="#d97706", fg="#ffffff", font=("Helvetica", 8, "bold"), command=lambda: self.change_eye_color("amber"))
        btn_amber.pack(side=tk.LEFT, padx=3)

        btn_purple = tk.Button(row, text="Amethyst", bg="#9333ea", fg="#ffffff", font=("Helvetica", 8, "bold"), command=lambda: self.change_eye_color("purple"))
        btn_purple.pack(side=tk.LEFT, padx=3)

    def change_cat_breed(self, breed_name):
        sprites.set_cat_breed(breed_name)
        self.pet_window.show_bubble(f"Cat breed changed to {breed_name.capitalize()}! *purr*", 2500)
        sound_system.cute(dynamic=True)

    def change_eye_color(self, color_name):
        pal = sprites.PALETTE
        if color_name == "blue":
            pal["eye_color_top"] = (56, 189, 248, 255)
            pal["eye_color_bot"] = (2, 132, 199, 255)
        elif color_name == "amber":
            pal["eye_color_top"] = (251, 191, 36, 255)
            pal["eye_color_bot"] = (217, 119, 6, 255)
        elif color_name == "purple":
            pal["eye_color_top"] = (192, 132, 252, 255)
            pal["eye_color_bot"] = (147, 51, 234, 255)
        else:
            pal["eye_color_top"] = (34, 197, 94, 255)
            pal["eye_color_bot"] = (250, 204, 21, 255)

        sprites.sprite_manager.cache.clear()
        self.pet_window.show_bubble(f"Eye color changed to {color_name}! *meow*", 2500)
        sound_system.cute(dynamic=True)

    def build_timer_section(self, parent):
        box = tk.LabelFrame(parent, text="⏱ Pomodoro & Screen Break Timers", bg="#1e293b", fg="#38bdf8", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        row1 = tk.Frame(box, bg="#1e293b")
        row1.pack(fill=tk.X, pady=4)
        tk.Label(row1, text="Work Session (min):", bg="#1e293b", fg="#cbd5e1", width=18, anchor="w").pack(side=tk.LEFT)
        self.work_entry = tk.Entry(row1, width=8, bg="#334155", fg="#ffffff", insertbackground="#ffffff")
        self.work_entry.insert(0, str(self.tracker.config.get("work_duration_minutes", 25)))
        self.work_entry.pack(side=tk.LEFT, padx=6)

        row2 = tk.Frame(box, bg="#1e293b")
        row2.pack(fill=tk.X, pady=4)
        tk.Label(row2, text="Short Break (min):", bg="#1e293b", fg="#cbd5e1", width=18, anchor="w").pack(side=tk.LEFT)
        self.break_entry = tk.Entry(row2, width=8, bg="#334155", fg="#ffffff", insertbackground="#ffffff")
        self.break_entry.insert(0, str(self.tracker.config.get("short_break_minutes", 5)))
        self.break_entry.pack(side=tk.LEFT, padx=6)

        btn_row = tk.Frame(box, bg="#1e293b")
        btn_row.pack(fill=tk.X, pady=8)

        save_btn = tk.Button(btn_row, text="Update Timers", bg="#2563eb", fg="#ffffff", activebackground="#1d4ed8", font=("Helvetica", 9, "bold"), command=self.save_timers)
        save_btn.pack(side=tk.LEFT, padx=4)

        take_break_btn = tk.Button(btn_row, text="Take Break Now", bg="#16a34a", fg="#ffffff", activebackground="#15803d", font=("Helvetica", 9, "bold"), command=self.take_break_now)
        take_break_btn.pack(side=tk.LEFT, padx=4)

        resume_btn = tk.Button(btn_row, text="Resume Work", bg="#d97706", fg="#ffffff", activebackground="#b45309", font=("Helvetica", 9, "bold"), command=self.resume_work_now)
        resume_btn.pack(side=tk.LEFT, padx=4)

    def build_hydration_section(self, parent):
        box = tk.LabelFrame(parent, text="💧 Water Reminder & Hydration", bg="#1e293b", fg="#60a5fa", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        row = tk.Frame(box, bg="#1e293b")
        row.pack(fill=tk.X, pady=4)
        tk.Label(row, text="Remind every (min):", bg="#1e293b", fg="#cbd5e1", width=18, anchor="w").pack(side=tk.LEFT)
        self.water_entry = tk.Entry(row, width=8, bg="#334155", fg="#ffffff", insertbackground="#ffffff")
        self.water_entry.insert(0, str(self.tracker.config.get("water_interval_minutes", 30)))
        self.water_entry.pack(side=tk.LEFT, padx=6)

        drink_btn = tk.Button(row, text="I Drank Water (+1) 🥛", bg="#0284c7", fg="#ffffff", font=("Helvetica", 9, "bold"), command=self.log_water)
        drink_btn.pack(side=tk.LEFT, padx=12)

    def build_sleep_alarm_section(self, parent):
        box = tk.LabelFrame(parent, text="🌙 Sleep Schedule & Morning Alarm", bg="#1e293b", fg="#c084fc", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        row1 = tk.Frame(box, bg="#1e293b")
        row1.pack(fill=tk.X, pady=3)
        tk.Label(row1, text="Bedtime (HH:MM):", bg="#1e293b", fg="#cbd5e1", width=18, anchor="w").pack(side=tk.LEFT)
        self.bed_entry = tk.Entry(row1, width=8, bg="#334155", fg="#ffffff", insertbackground="#ffffff")
        self.bed_entry.insert(0, str(self.tracker.config.get("bedtime", "23:00")))
        self.bed_entry.pack(side=tk.LEFT, padx=6)

        sleep_now_btn = tk.Button(row1, text="Sleep Pet Now", bg="#7c3aed", fg="#ffffff", font=("Helvetica", 9), command=self.pet_sleep_now)
        sleep_now_btn.pack(side=tk.LEFT, padx=12)

        row2 = tk.Frame(box, bg="#1e293b")
        row2.pack(fill=tk.X, pady=3)
        tk.Label(row2, text="Wake Time (HH:MM):", bg="#1e293b", fg="#cbd5e1", width=18, anchor="w").pack(side=tk.LEFT)
        self.wake_entry = tk.Entry(row2, width=8, bg="#334155", fg="#ffffff", insertbackground="#ffffff")
        self.wake_entry.insert(0, str(self.tracker.config.get("wake_time", "07:00")))
        self.wake_entry.pack(side=tk.LEFT, padx=6)

        test_alarm_btn = tk.Button(row2, text="Test Alarm", bg="#e11d48", fg="#ffffff", font=("Helvetica", 9), command=self.test_alarm_sound)
        test_alarm_btn.pack(side=tk.LEFT, padx=12)

    def build_ai_watcher_section(self, parent):
        box = tk.LabelFrame(parent, text="🤖 AI Response Watcher ('You're Up!')", bg="#1e293b", fg="#34d399", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        self.ai_var = tk.BooleanVar(value=self.tracker.ai_watching)
        chk = tk.Checkbutton(
            box,
            text="Monitor Clipboard for AI responses (ChatGPT, Claude, Gemini, etc.)",
            variable=self.ai_var,
            bg="#1e293b",
            fg="#cbd5e1",
            selectcolor="#0f172a",
            activebackground="#1e293b",
            activeforeground="#34d399",
            command=self.toggle_ai_watch
        )
        chk.pack(anchor="w")

        test_ai_btn = tk.Button(box, text="Simulate 'AI Response Ready!' Alert", bg="#059669", fg="#ffffff", font=("Helvetica", 9, "bold"), command=self.test_ai_alert)
        test_ai_btn.pack(anchor="w", pady=6)

    def build_gesture_studio_section(self, parent):
        box = tk.LabelFrame(parent, text="🎭 12 Gestures & Dramatic Tantrum", bg="#1e293b", fg="#f472b6", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        gestures = [
            ("Happy", "happy"),
            ("Petted", "petted"),
            ("Sad", "sad"),
            ("Turned", "turned"),
            ("Scratching", "scratching"),
            ("Peeking", "peeking"),
            ("Sleeping", "sleeping"),
            ("Falling", "falling"),
            ("Idle", "idle"),
            ("Empathy", "empathy"),
            ("Walking", "walking"),
            ("Eating", "eating")
        ]

        grid_frame = tk.Frame(box, bg="#1e293b")
        grid_frame.pack(fill=tk.X, pady=4)

        for i, (label, g_name) in enumerate(gestures):
            r = i // 6
            c = i % 6
            btn = tk.Button(
                grid_frame,
                text=label,
                bg="#334155",
                fg="#f1f5f9",
                width=8,
                font=("Helvetica", 8, "bold"),
                command=lambda g=g_name: self.trigger_gesture(g)
            )
            btn.grid(row=r, column=c, padx=2, pady=3)

        dramatic_btn = tk.Button(
            box,
            text="⚡ Trigger Dramatic Tantrum (Scratch & Big Tail Wipe) ⚡",
            bg="#dc2626",
            fg="#ffffff",
            font=("Helvetica", 10, "bold"),
            pady=4,
            command=self.trigger_dramatic_tantrum
        )
        dramatic_btn.pack(fill=tk.X, pady=8)

    def build_parkour_section(self, parent):
        box = tk.LabelFrame(parent, text="🎪 Talking Tom Gravity & Window Tiles Parkour", bg="#1e293b", fg="#38bdf8", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        desc = tk.Label(
            box,
            text="Interactive gravity physics! Pick up & toss her, drop from heights, or hop across tiles.",
            bg="#1e293b",
            fg="#94a3b8",
            font=("Helvetica", 8)
        )
        desc.pack(anchor="w", pady=(0, 6))

        btn_row = tk.Frame(box, bg="#1e293b")
        btn_row.pack(fill=tk.X, pady=2)

        toss_btn = tk.Button(
            btn_row,
            text="🚀 Toss in Air\n(Talking Tom Fall)",
            bg="#0284c7",
            fg="#ffffff",
            font=("Helvetica", 8, "bold"),
            command=self.toss_cat_action
        )
        toss_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        hop_btn = tk.Button(
            btn_row,
            text="🪜 Hop Window Tiles\n(Platformer Jumper)",
            bg="#10b981",
            fg="#ffffff",
            font=("Helvetica", 8, "bold"),
            command=self.hop_tiles_action
        )
        hop_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        hide_btn = tk.Button(
            btn_row,
            text="🙈 Hide Behind Edge\n(Peek-a-boo)",
            bg="#8b5cf6",
            fg="#ffffff",
            font=("Helvetica", 8, "bold"),
            command=self.hide_behind_action
        )
        hide_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        treat_btn = tk.Button(
            btn_row,
            text="🐟 Feed Fish Treat\n(Nom Nom)",
            bg="#f59e0b",
            fg="#ffffff",
            font=("Helvetica", 8, "bold"),
            command=self.feed_treat_action
        )
        treat_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

    def build_soundboard_section(self, parent):
        box = tk.LabelFrame(parent, text="🔊 6 Dynamic Cat Sounds Board", bg="#1e293b", fg="#fbbf24", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        sounds = [
            ("Happy Meow", lambda: sound_system.happy(dynamic=True)),
            ("Cute Meow", lambda: sound_system.cute(dynamic=True)),
            ("Sad Meow", lambda: sound_system.sad(dynamic=True)),
            ("Angry Hiss", sound_system.angry),
            ("Frightened Yowl", sound_system.frightened),
            ("Morning Alarm", sound_system.alarm)
        ]

        s_grid = tk.Frame(box, bg="#1e293b")
        s_grid.pack(fill=tk.X, pady=4)

        for i, (label, fn) in enumerate(sounds):
            r = i // 3
            c = i % 3
            btn = tk.Button(
                s_grid,
                text=label,
                bg="#475569",
                fg="#fef08a",
                width=14,
                font=("Helvetica", 8, "bold"),
                command=fn
            )
            btn.grid(row=r, column=c, padx=4, pady=3)

    def build_stats_section(self, parent):
        box = tk.LabelFrame(parent, text="📊 Productivity & Pet Stats", bg="#1e293b", fg="#94a3b8", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        self.stats_lbl = tk.Label(
            box,
            text="Loading stats...",
            bg="#1e293b",
            fg="#e2e8f0",
            font=("Monospace", 9),
            justify=tk.LEFT
        )
        self.stats_lbl.pack(anchor="w")

    def toggle_neural_brain(self):
        self.tracker.neural_enabled = self.brain_var.get()
        self.tracker.config["neural_brain_enabled"] = self.tracker.neural_enabled
        self.tracker.save_config()

    def force_neural_eval(self):
        self.tracker.evaluate_neural_brain()
        sound_system.cute(dynamic=True)

    def save_timers(self):
        try:
            w = int(self.work_entry.get())
            b = int(self.break_entry.get())
            water = int(self.water_entry.get())
            self.tracker.config["work_duration_minutes"] = max(1, w)
            self.tracker.config["short_break_minutes"] = max(1, b)
            self.tracker.config["water_interval_minutes"] = max(1, water)
            self.tracker.config["bedtime"] = self.bed_entry.get().strip()
            self.tracker.config["wake_time"] = self.wake_entry.get().strip()
            self.tracker.save_config()
            self.pet_window.show_bubble("Timers updated! I've got your back! :3", 3000)
            sound_system.cute(dynamic=True)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid whole numbers for minutes!")

    def take_break_now(self):
        self.tracker.take_break()
        self.pet_window.set_gesture("happy", 3000)
        sound_system.happy(dynamic=True)

    def resume_work_now(self):
        self.tracker.resume_work()
        self.pet_window.set_gesture("idle")
        sound_system.cute(dynamic=True)

    def log_water(self):
        self.tracker.log_water_drink()
        self.pet_window.set_gesture("petted", 2500)
        sound_system.purr()

    def pet_sleep_now(self):
        self.tracker.is_sleeping = True
        self.pet_window.set_gesture("sleeping")
        self.pet_window.show_bubble("Goodnight! Going to sleep now... Zzz", 3500)

    def test_alarm_sound(self):
        self.tracker.alarm_ringing = True
        sound_system.alarm()
        self.pet_window.set_gesture("happy")
        self.pet_window.show_bubble("ALARM! Wake up! Morning stretch! *meow*", 4000)

    def toggle_ai_watch(self):
        self.tracker.ai_watching = self.ai_var.get()
        self.tracker.config["ai_watcher_enabled"] = self.tracker.ai_watching
        self.tracker.save_config()

    def test_ai_alert(self):
        sound_system.happy(dynamic=True)
        self.pet_window.set_gesture("happy", 4000)
        self.pet_window.show_bubble("You're up! AI has finished generating your answer! 🐱✨", 4000)

    def trigger_gesture(self, g_name):
        self.pet_window.set_gesture(g_name, 3500)
        if g_name == "happy":
            sound_system.happy(dynamic=True)
        elif g_name == "petted":
            sound_system.purr()
        elif g_name == "sad":
            sound_system.sad(dynamic=True)
        elif g_name == "angry":
            sound_system.angry()
        elif g_name == "frightened":
            sound_system.frightened()
        elif g_name == "sleeping":
            sound_system.purr()
        else:
            sound_system.cute(dynamic=True)

    def trigger_dramatic_tantrum(self):
        self.pet_window.trigger_dramatic_scratch_event()

    def toss_cat_action(self):
        if self.pet_window:
            self.pet_window.toss_in_air()

    def hop_tiles_action(self):
        if self.pet_window:
            self.pet_window.hop_tiles()

    def hide_behind_action(self):
        if self.pet_window:
            self.pet_window.hide_behind_taskbar()

    def feed_treat_action(self):
        if self.pet_window:
            self.pet_window.feed_fish_treat()

    def update_stats_loop(self):
        rem_sec = self.tracker.get_remaining_work_seconds()
        mins = rem_sec // 60
        secs = rem_sec % 60
        tot_mins = self.tracker.total_seconds // 60

        text = (
            f"State: {self.tracker.current_state.upper()}\n"
            f"Next Break In: {mins:02d}:{secs:02d}\n"
            f"Total Active Time: {tot_mins} mins\n"
            f"Breaks Taken: {self.tracker.config.get('breaks_taken', 0)}\n"
            f"Water Glasses Drank: {self.tracker.config.get('water_glasses_logged', 0)} 🥛\n"
            f"AI Watcher: {'Active' if self.tracker.ai_watching else 'Off'}"
        )
        self.stats_lbl.config(text=text)

        title = window_sensor.cached_window_title
        if len(title) > 28:
            title = title[:25] + "..."

        idle_sec = int(window_sensor.get_idle_seconds())
        brain_text = (
            f"Active Window: [{self.tracker.last_window_category.upper()}] {title}\n"
            f"Inactivity: {idle_sec}s | Mode: {'Autonomous Neural' if self.tracker.neural_enabled else 'Pomodoro'}\n"
            f"Current Brain Action: {self.tracker.current_neural_action}\n"
            f"Affection: {int(neural_brain.affection * 100)}% ❤️ | Patience: {int(neural_brain.patience * 100)}% ⏳\n"
            f"Total Pettings: {neural_brain.total_pets} | Bond Streak: {neural_brain.streak_days} days"
        )
        self.brain_stats_lbl.config(text=brain_text)

        self.win.after(1000, self.update_stats_loop)

    def on_close(self):
        self.win.withdraw()
