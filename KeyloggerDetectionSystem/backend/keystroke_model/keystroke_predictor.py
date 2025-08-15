import keyboard
import time
import joblib
import numpy as np

# Load trained model
model = joblib.load("keystroke_model/keystroke_model.joblib")

print("👉 Start typing freely. Press Enter to run prediction.")

typed_keys = []
keydown_times = {}
keyup_times = []
press_release = []  # (key, down_time, up_time)
import numpy as np

def extract_timing_features(events, target_length=81):
    """
    Extracts 81 timing features (hold, UD, DD) from a free-typed keystroke sequence.

    Parameters:
    - events: List of ('down', key, time) and ('up', key, time, hold) tuples
    - target_length: Desired length of feature vector (pads with zeros)

    Returns:
    - Numpy array of shape (target_length,) or None if not enough data
    """

    hold_times = []
    dd_times = []
    ud_times = []

    key_down_times = []
    key_up_times = []

    for e in events:
        if e[0] == 'down':
            key_down_times.append((e[1], e[2]))
        elif e[0] == 'up':
            hold_times.append(e[3])
            key_up_times.append((e[1], e[2]))

    # DD: time between consecutive key downs
    for i in range(1, len(key_down_times)):
        dd = key_down_times[i][1] - key_down_times[i - 1][1]
        dd_times.append(dd)

    # UD: time between key up and next key down
    i = 0
    j = 0
    while i < len(key_up_times) and j < len(key_down_times):
        up_key, up_time = key_up_times[i]
        down_key, down_time = key_down_times[j]

        if down_time > up_time:
            ud_times.append(down_time - up_time)
            i += 1
            j += 1
        else:
            j += 1

    # Combine all features
    all_features = hold_times + dd_times + ud_times

    if len(all_features) < 5:
        return None  # Not enough keystrokes captured

    # Pad or truncate to target length
    if len(all_features) < target_length:
        all_features += [0.0] * (target_length - len(all_features))
    else:
        all_features = all_features[:target_length]

    return np.array(all_features)
