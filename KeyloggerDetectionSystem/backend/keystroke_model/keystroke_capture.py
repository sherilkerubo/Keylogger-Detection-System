# keystroke_model/keystroke_capture.py
import keyboard
import time
from collections import deque

# These are the 10 characters in the password `.tie5Roanl`
EXPECTED_KEYS = [".", "t", "i", "e", "5", "R", "o", "a", "n", "l"]

def capture_keystroke_timing():
    key_down_times = {}
    key_up_times = {}
    pressed_keys = []
    
    print("Type the password: `.tie5Roanl`")
    while len(pressed_keys) < len(EXPECTED_KEYS):
        event = keyboard.read_event()
        key = event.name

        if key == "space":
            key = " "

        if event.event_type == "down" and key in EXPECTED_KEYS:
            key_down_times[key + str(len(pressed_keys))] = time.time()
            pressed_keys.append(key)
        elif event.event_type == "up" and key in pressed_keys:
            index = pressed_keys.index(key)
            key_up_times[key + str(index)] = time.time()

    # Extract features
    features = []

    # H: Hold time
    for i, key in enumerate(EXPECTED_KEYS):
        k = key + str(i)
        hold = key_up_times.get(k, 0) - key_down_times.get(k, 0)
        features.append(hold)

    # DD: keydown to keydown
    for i in range(len(EXPECTED_KEYS) - 1):
        k1 = EXPECTED_KEYS[i] + str(i)
        k2 = EXPECTED_KEYS[i + 1] + str(i + 1)
        dd = key_down_times.get(k2, 0) - key_down_times.get(k1, 0)
        features.append(dd)

    # UD: keyup to next keydown
    for i in range(len(EXPECTED_KEYS) - 1):
        k1 = EXPECTED_KEYS[i] + str(i)
        k2 = EXPECTED_KEYS[i + 1] + str(i + 1)
        ud = key_down_times.get(k2, 0) - key_up_times.get(k1, 0)
        features.append(ud)

    return features
