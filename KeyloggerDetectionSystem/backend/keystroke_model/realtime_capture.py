import keyboard
import time

# For real-time hold, DD, and UD timing
def capture_keystroke_sequence(timeout=5):
    print("⌨️ Start typing (press Enter to finish):")
    sequence = []
    press_times = {}
    start_time = time.time()

    while True:
        event = keyboard.read_event(suppress=True)
        now = time.time()

        if now - start_time > timeout:
            break

        if event.event_type == keyboard.KEY_DOWN:
            press_times[event.name] = now
            sequence.append(('down', event.name, now))

        elif event.event_type == keyboard.KEY_UP:
            if event.name in press_times:
                hold_time = now - press_times[event.name]
                sequence.append(('up', event.name, now, hold_time))

            if event.name == 'enter':
                break

    return sequence
