import tkinter as tk
import sys
import os

from sound_player import sound_system, build_all_sounds
from sprites import sprite_manager
from screen_tracker import ScreenTimeTracker
from pet_window import DesktopPetWindow
from control_panel import ControlPanelWindow
from neural_brain import neural_brain

def main():
    build_all_sounds()

    root = tk.Tk()

    control_panel_instance = [None]

    def on_tracker_state_change(new_state, message):
        if pet_win:
            if new_state == "dramatic_tantrum":
                neural_brain.record_tantrum_occurred()
                pet_win.trigger_dramatic_scratch_event()
            else:
                pet_win.set_gesture(new_state)
                pet_win.show_bubble(message, 4000)

                if new_state == "empathy":
                    sound_system.cute(dynamic=True)
                elif new_state == "sad":
                    sound_system.sad(dynamic=True)
                elif new_state == "angry":
                    sound_system.angry()
                elif new_state == "happy":
                    sound_system.happy(dynamic=True)
                elif new_state == "petted":
                    sound_system.purr()
                elif new_state == "alarm":
                    sound_system.alarm()

    def on_tracker_notification(notif_type, message):
        if pet_win:
            pet_win.show_bubble(message, 4500)
            if notif_type == "water":
                pet_win.set_gesture("peeking", 3500)
                sound_system.cute(dynamic=True)
            elif notif_type == "ai_ready":
                pet_win.set_gesture("happy", 4000)
                sound_system.happy(dynamic=True)

    def on_neural_action(action, category, title, probabilities):
        if not pet_win or pet_win.is_tantrum_running or tracker.is_sleeping:
            return

        action_messages = {
            "idle_watch": "Watching you code diligently~ 🐱",
            "peeking_bookmark": "Peeking in... What are we working on? :3",
            "curious_scratch": "Scratch scratch... Pay attention to paws!",
            "happy_bounce": "Great focus streak today! Keep going!",
            "purr_cozy": "Purrrr... nice and cozy workspace.",
            "empathy_beg": "Pwease take a little break for your eyes? :3",
            "sad_pout": "You've been working so hard without resting...",
            "angry_hiss": "Hey! Time to look away from that screen!",
            "turned_cold": "Humph! You didn't listen to me!",
            "curled_catnap": "Zzz... taking a catnap while you're away.",
            "dramatic_scratch_wipe": "THAT'S IT! TIME FOR A BREAK!!"
        }

        gesture_map = {
            "idle_watch": "idle",
            "peeking_bookmark": "peeking",
            "curious_scratch": "scratching",
            "happy_bounce": "happy",
            "purr_cozy": "petted",
            "empathy_beg": "empathy",
            "sad_pout": "sad",
            "angry_hiss": "angry",
            "turned_cold": "turned",
            "curled_catnap": "sleeping",
            "dramatic_scratch_wipe": "scratching"
        }

        if action == "dramatic_scratch_wipe":
            neural_brain.record_tantrum_occurred()
            pet_win.trigger_dramatic_scratch_event()
            return

        g = gesture_map.get(action, "idle")
        msg = action_messages.get(action, "Meow~")

        if category == "entertainment" and action in ["peeking_bookmark", "curious_scratch"]:
            msg = "Caught you on a distraction tab! Back to work? :3"

        pet_win.set_gesture(g, 4000)
        pet_win.show_bubble(msg, 3500)

        if action in ["happy_bounce", "peeking_bookmark"]:
            sound_system.happy(dynamic=True)
        elif action in ["empathy_beg", "curious_scratch"]:
            sound_system.cute(dynamic=True)
        elif action == "sad_pout":
            sound_system.sad(dynamic=True)
        elif action == "angry_hiss":
            sound_system.angry()
        elif action in ["purr_cozy", "curled_catnap"]:
            sound_system.purr()

    tracker = ScreenTimeTracker(
        on_state_change=on_tracker_state_change,
        on_notification=on_tracker_notification,
        on_neural_action=on_neural_action
    )

    pet_win = DesktopPetWindow(root, tracker)

    def show_control_panel():
        if control_panel_instance[0] is None or not tk.Toplevel.winfo_exists(control_panel_instance[0].win):
            control_panel_instance[0] = ControlPanelWindow(root, tracker, pet_win)
        else:
            control_panel_instance[0].win.deiconify()
            control_panel_instance[0].win.lift()

    pet_win.set_control_panel_callback(show_control_panel)

    root.after(800, show_control_panel)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        tracker.running = False
        sys.exit(0)

if __name__ == "__main__":
    main()
