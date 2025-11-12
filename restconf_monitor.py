import requests
import json

BASE_URL = "http://127.0.0.1:5001"
HEADERS = {"Accept": "application/json"}

def get_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"🔐 HTTP Error: {errh}")
        return {"error": "Authentication failed or invalid endpoint"}
    except requests.exceptions.ConnectionError as errc:
        print(f"🌐 Connection Error: {errc}")
        return {"error": "Device unreachable or server not running"}
    except requests.exceptions.Timeout as errt:
        print(f"⏱️ Timeout Error: {errt}")
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as err:
        print(f"🧨 Request Error: {err}")
        return {"error": "Unexpected error occurred"}

# Use exact paths from Flask
hostname_data = get_data("/restconf/data/Cisco-IOS-XE-native:native/hostname")
interfaces_data = get_data("/restconf/data/ietf-interfaces:interfaces")
uptime_data = get_data("/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-system-data")

# Format output
output = {
    "hostname": hostname_data.get("Cisco-IOS-XE-native:hostname", "N/A"),
    "interfaces": [],
    "uptime": uptime_data.get("device-system-data", {}).get("system-uptime", "N/A")
}

for iface in interfaces_data.get("ietf-interfaces:interfaces", {}).get("interface", []):
    name = iface.get("name")
    ip = iface.get("ietf-ip:ipv4", {}).get("address", [{}])[0].get("ip", "N/A")
    output["interfaces"].append({"name": name, "ip": ip})

print(json.dumps(output, indent=2))
