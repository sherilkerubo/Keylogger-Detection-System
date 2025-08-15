import subprocess

def run_windows_defender_scan():
    try:
        output = subprocess.check_output([
            "powershell", "Start-MpScan", "-ScanType", "QuickScan"
        ])
        return "threat" in output.decode().lower()
    except Exception as e:
        return False
