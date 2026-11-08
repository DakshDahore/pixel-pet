import tkinter as tk
import sys
import os

from sound_player import sound_system, build_all_sounds
from sprites import sprite_manager
from screen_tracker import ScreenTimeTracker
from pet_window import DesktopPetWindow
from control_panel import ControlPanelWindow

def main():
    build_all_sounds()

    root = tk.Tk()

    control_panel_instance = [None]

    def on_tracker_state_change(new_state, message):
        if pet_win:
            if new_state == "dramatic_tantrum":
                pet_win.trigger_dramatic_scratch_event()
            else:
                pet_win.set_gesture(new_state)
                pet_win.show_bubble(message, 4000)

                if new_state == "empathy":
                    sound_system.cute()
                elif new_state == "sad":
                    sound_system.sad()
                elif new_state == "angry":
                    sound_system.angry()
                elif new_state == "happy":
                    sound_system.happy()
                elif new_state == "petted":
                    sound_system.purr()
                elif new_state == "alarm":
                    sound_system.alarm()

    def on_tracker_notification(notif_type, message):
        if pet_win:
            pet_win.show_bubble(message, 4500)
            if notif_type == "water":
                pet_win.set_gesture("peeking", 3500)
                sound_system.cute()
            elif notif_type == "ai_ready":
                pet_win.set_gesture("happy", 4000)
                sound_system.happy()

    tracker = ScreenTimeTracker(
        on_state_change=on_tracker_state_change,
        on_notification=on_tracker_notification
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
