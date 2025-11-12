from flask import Flask, render_template
import requests

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:5001"

def get_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {}

@app.route('/')
def dashboard():
    hostname_data = get_data("/restconf/data/Cisco-IOS-XE-native:native/hostname")
    interfaces_data = get_data("/restconf/data/ietf-interfaces:interfaces")
    uptime_data = get_data("/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-system-data")

    hostname = hostname_data.get("Cisco-IOS-XE-native:hostname", "N/A")
    uptime = uptime_data.get("device-system-data", {}).get("system-uptime", "N/A")
    interfaces = interfaces_data.get("ietf-interfaces:interfaces", {}).get("interface", [])

    return render_template("dashboard.html", hostname=hostname, uptime=uptime, interfaces=interfaces)

if __name__ == '__main__':
    app.run(port=5002)
