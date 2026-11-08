import tkinter as tk
from tkinter import ttk, messagebox
import sound_player
from sound_player import sound_system

class ControlPanelWindow:
    def __init__(self, root, tracker, pet_window):
        self.root = root
        self.tracker = tracker
        self.pet_window = pet_window

        self.win = tk.Toplevel(self.root)
        self.win.title("Pixel Pet - Companion & Timer App")
        self.win.geometry("540x680")
        self.win.configure(bg="#0f172a")

        self.win.protocol("WM_DELETE_WINDOW", self.on_close)

        self.build_ui()
        self.update_stats_loop()

    def build_ui(self):
        title_frame = tk.Frame(self.win, bg="#1e293b", pady=12)
        title_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            title_frame,
            text="🐱 Pixel Pet Companion",
            font=("Helvetica", 16, "bold"),
            bg="#1e293b",
            fg="#f8fafc"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            title_frame,
            text="Desktop Health & Pomodoro Guardian",
            font=("Helvetica", 10),
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

        content_canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=520)
        content_canvas.configure(yscrollcommand=scrollbar.set)

        content_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        self.build_timer_section(scroll_frame)
        self.build_hydration_section(scroll_frame)
        self.build_sleep_alarm_section(scroll_frame)
        self.build_ai_watcher_section(scroll_frame)
        self.build_gesture_studio_section(scroll_frame)
        self.build_soundboard_section(scroll_frame)
        self.build_stats_section(scroll_frame)

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
        box = tk.LabelFrame(parent, text="🎭 10 Gestures & Dramatic Tantrum", bg="#1e293b", fg="#f472b6", font=("Helvetica", 11, "bold"), padx=12, pady=10)
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
            ("Empathy", "empathy")
        ]

        grid_frame = tk.Frame(box, bg="#1e293b")
        grid_frame.pack(fill=tk.X, pady=4)

        for i, (label, g_name) in enumerate(gestures):
            r = i // 5
            c = i % 5
            btn = tk.Button(
                grid_frame,
                text=label,
                bg="#334155",
                fg="#f1f5f9",
                width=9,
                font=("Helvetica", 8, "bold"),
                command=lambda g=g_name: self.trigger_gesture(g)
            )
            btn.grid(row=r, column=c, padx=3, pady=3)

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

    def build_soundboard_section(self, parent):
        box = tk.LabelFrame(parent, text="🔊 6 Cat Sounds Board", bg="#1e293b", fg="#fbbf24", font=("Helvetica", 11, "bold"), padx=12, pady=10)
        box.pack(fill=tk.X, pady=6)

        sounds = [
            ("Happy Meow", sound_system.happy),
            ("Cute Meow", sound_system.cute),
            ("Sad Meow", sound_system.sad),
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
            sound_system.cute()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid whole numbers for minutes!")

    def take_break_now(self):
        self.tracker.take_break()
        self.pet_window.set_gesture("happy", 3000)
        sound_system.happy()

    def resume_work_now(self):
        self.tracker.resume_work()
        self.pet_window.set_gesture("idle")
        sound_system.cute()

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
        sound_system.happy()
        self.pet_window.set_gesture("happy", 4000)
        self.pet_window.show_bubble("You're up! AI has finished generating your answer! 🐱✨", 4000)

    def trigger_gesture(self, g_name):
        self.pet_window.set_gesture(g_name, 3500)
        if g_name == "happy":
            sound_system.happy()
        elif g_name == "petted":
            sound_system.purr()
        elif g_name == "sad":
            sound_system.sad()
        elif g_name == "angry":
            sound_system.angry()
        elif g_name == "frightened":
            sound_system.frightened()
        elif g_name == "sleeping":
            sound_system.purr()
        else:
            sound_system.cute()

    def trigger_dramatic_tantrum(self):
        self.pet_window.trigger_dramatic_scratch_event()

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
        self.win.after(1000, self.update_stats_loop)

    def on_close(self):
        self.win.withdraw()
