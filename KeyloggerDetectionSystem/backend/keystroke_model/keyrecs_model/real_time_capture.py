# backend/keystroke_model/real_time_capture.py
import keyboard
import time

def capture_keystroke_features(max_keys=10, timeout=10):
    events = []
    down_times = []
    up_times = []
    hold_times = []
    dd_times = []
    ud_times = []

    print(f"⏳ Start typing (up to {max_keys} keys)...")
    start_time = time.time()

    while len(events) < max_keys * 2 and (time.time() - start_time) < timeout:
        event = keyboard.read_event()
        if event.event_type in ["down", "up"]:
            events.append((event.name, event.event_type, time.time()))

    for i, (key, etype, tstamp) in enumerate(events):
        if etype == "down":
            down_times.append((key, tstamp))
        elif etype == "up":
            up_times.append((key, tstamp))
            for j in range(len(down_times)-1, -1, -1):
                if down_times[j][0] == key:
                    hold = tstamp - down_times[j][1]
                    hold_times.append(hold)
                    break

    for i in range(len(down_times) - 1):
        dd_times.append(down_times[i+1][1] - down_times[i][1])

    for i in range(len(up_times) - 1):
        ud_times.append(down_times[i+1][1] - up_times[i][1])

    features = hold_times + dd_times + ud_times
    features = features[:81] + [0.0] * (81 - len(features))
    return features
