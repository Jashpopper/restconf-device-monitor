from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/restconf/data/Cisco-IOS-XE-native:native/hostname')
def hostname():
    return jsonify({"Cisco-IOS-XE-native:hostname": "MockRouter"})

@app.route('/restconf/data/ietf-interfaces:interfaces')
def interfaces():
    return jsonify({
        "ietf-interfaces:interfaces": {
            "interface": [
                {"name": "GigabitEthernet1", "ietf-ip:ipv4": {"address": [{"ip": "192.168.1.1"}]}},
                {"name": "GigabitEthernet2", "ietf-ip:ipv4": {"address": [{"ip": "10.0.0.1"}]}}
            ]
        }
    })

@app.route('/restconf/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-system-data')
def uptime():
    return jsonify({"device-system-data": {"system-uptime": "5 days, 3 hours"}})

if __name__ == '__main__':
    app.run(port=5001)
