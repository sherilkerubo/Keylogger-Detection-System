import psutil
import time
import keyboard
from scapy.all import sniff, IP, TCP, UDP

from virus_total import check_virustotal
from defender_scan import run_windows_defender_scan
from ml_model.predict import is_malicious
from keystroke_model.predict import is_keystroke_malicious
from keystroke_model.keyrecs_model.predict import is_keyrecs_malicious


def capture_keystroke_timings(max_keys=10, timeout=10):
    key_events = []
    pressed_keys = []

    print(f" Start typing (up to {max_keys} keys)...")
    start_time = time.time()

    while len(pressed_keys) < max_keys and (time.time() - start_time) < timeout:
        event = keyboard.read_event()
        if event.event_type == "down":
            pressed_keys.append(event.name)
        if event.event_type in ["down", "up"]:
            key_events.append((event.name, event.event_type, time.time()))

    hold_times, dd_times, ud_times = [], [], []
    down_times, up_times = [], []

    for key, event_type, timestamp in key_events:
        if event_type == "down":
            down_times.append((key, timestamp))
        elif event_type == "up":
            up_times.append((key, timestamp))
            for j in range(len(down_times) - 1, -1, -1):
                if down_times[j][0] == key:
                    hold_times.append(timestamp - down_times[j][1])
                    break

    for i in range(len(down_times) - 1):
        dd_times.append(down_times[i + 1][1] - down_times[i][1])
    for i in range(min(len(up_times), len(down_times) - 1)):
        ud_times.append(down_times[i + 1][1] - up_times[i][1])

    features = hold_times + dd_times + ud_times
    features = features[:49] + [0.0] * (49 - len(features)) 


    return pressed_keys, features


def capture_network_traffic(packet_count=10):
    traffic_logs = []
    try:
        packets = sniff(count=packet_count, timeout=5)
        for pkt in packets:
            if IP in pkt:
                log = {
                    "src": pkt[IP].src,
                    "dst": pkt[IP].dst,
                    "proto": pkt[IP].proto,
                }
                if TCP in pkt:
                    log.update({
                        "sport": pkt[TCP].sport,
                        "dport": pkt[TCP].dport,
                        "layer": "TCP"
                    })
                elif UDP in pkt:
                    log.update({
                        "sport": pkt[UDP].sport,
                        "dport": pkt[UDP].dport,
                        "layer": "UDP"
                    })
                traffic_logs.append(log)
    except Exception as e:
        traffic_logs.append({"error": f"Network capture failed: {str(e)}"})
    return traffic_logs


def scan_system():
    logs = {
        "keystrokes": [],
        "network": [],
        "processes": [],
        "alerts": []
    }

    #  Keystroke models
    try:
        keystrokes, features_81 = capture_keystroke_timings()
        logs["keystrokes"] = keystrokes

        # KeyRecs model (81 features)
        if is_keyrecs_malicious(features_81):
            logs["alerts"].append("⚠️ KeyRecs model detected suspicious behavior")

        # DSL model (first 31 features)
        features_31 = features_81[:31]
        if is_keystroke_malicious(features_31):
            logs["alerts"].append("⚠️ DSL model detected suspicious behavior")

    except Exception as e:
        logs["alerts"].append(f"Keystroke capture failed: {str(e)}")

    #  Network traffic
    logs["network"] = capture_network_traffic(packet_count=15)

    #  System behavior model
    try:
        if is_malicious(features_81):  # system/network model trained on 81 features
            logs["alerts"].append("⚠️ System behavior model detected anomaly")
    except Exception as e:
        logs["alerts"].append(f"System behavior model failed: {str(e)}")

    #  Processes + VirusTotal
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            logs["processes"].append(proc.info)
            if check_virustotal(proc.info['name']):
                logs["alerts"].append(f"⚠️ VirusTotal flagged '{proc.info['name']}'")
        except Exception:
            pass

    #  Defender scan
    try:
        if run_windows_defender_scan():
            logs["alerts"].append("⚠️ Windows Defender flagged a threat")
    except Exception as e:
        logs["alerts"].append(f"Defender scan failed: {str(e)}")

    return logs
