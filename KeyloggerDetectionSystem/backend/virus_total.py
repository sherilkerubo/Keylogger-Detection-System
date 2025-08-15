import requests
import hashlib
import os

API_KEY = "ab15fc21c72e70f5e21dd1df8254b597926a8c797a864a88d47aa215c1d06805"
BASE_URL = "https://www.virustotal.com/api/v3/files/"


def file_to_sha256(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_virustotal(filename):
    file_hash = file_to_sha256(filename)
    if not file_hash:
        return False

    headers = {
        "x-apikey": API_KEY
    }

    response = requests.get(BASE_URL + file_hash, headers=headers)
    if response.status_code == 200:
        data = response.json()
        malicious_votes = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
        return malicious_votes > 0
    return False



