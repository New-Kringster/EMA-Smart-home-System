# EMA Smart Home System

A Wi-Fi connected smart home system built on four BeagleBone Black Wireless (BBBW) boards, designed around sustainable living — real-time energy monitoring, environmental control, and security, all talking to a central web dashboard over Socket.IO.

This was a school group project. Our team was awarded an **A**.

[Live Demo](https://csdpdemo.chiambucket.com) · [Promotional Video](https://www.youtube.com/watch?v=PFhsRaakJAs) · [Project Write-up](https://www.chiambucket.com/csdp.html)

---

## What it does

Four nodes, each running on its own BBBW, handle a different part of the home. They all connect to a central Flask + Socket.IO server that serves the dashboard and coordinates alarms across every node simultaneously.

### Climate Node — `BBBW_Climate.py`
Reads temperature and humidity from a BME680 sensor. Presence detection via a PIR sensor tells the system whether anyone's actually in the room. The fan only kicks on when someone is there *and* conditions are warm and humid. An 8×8 LED matrix gives local visual feedback on the fan state.

### Bathroom Node — `BBBW_Shower.py`
Lets you set a shower timer using physical buttons, with the current temperature and duration shown on an OLED display. The timer auto-starts when the PIR detects motion, and the buzzer sounds a three-tone alert when time's up. Good for water conservation.

### Kitchen Node — `BBBW_kitchen.py`
Monitors fridge energy usage via an analog current sensor and reports a power reading to the dashboard. A Flame Click sensor watches for uncontrolled fire — if it trips, an alarm fires across every node in the system, not just the kitchen.

### Intrusion Node — `BBBW_Intrusion.py`
Watches a reed switch (door open/close) and a vibration sensor (knocking). Either event triggers a system-wide alarm through the server.

---

## Architecture

Every BBBW node runs a Socket.IO client. The server polls each node on a schedule, receives status data back, and pushes relevant events out to the web dashboard and to other nodes.

```
[Climate BBBW] ──┐
[Bathroom BBBW] ──┤── Socket.IO ──► [Flask Web Server] ──► [Browser Dashboard]
[Kitchen BBBW] ──┤                        │
[Intrusion BBBW] ─┘                       └──► Broadcast alarms to all nodes
```

The dashboard displays live temperature, humidity, energy readings, and alarm states. Threshold breaches (temperature > 30°C, humidity > 85%) visually flag on the UI.

---

## Files

| File | Role |
|---|---|
| `WebServer.py` | Flask + Socket.IO server. Serves the dashboard and routes events between nodes and the browser. |
| `project.html` | The dashboard front-end. Connects via Socket.IO, updates live readings, shows alarm states. |
| `style.css` | Dashboard styles. |
| `BBBW_Climate.py` | Climate node — BME680 sensor, PIR presence, LED matrix, buzzer. |
| `BBBW_Shower.py` | Bathroom node — PIR, OLED display, capacitive buttons, buzzer, shower timer. |
| `BBBW_kitchen.py` | Kitchen node — analog current sensing, Flame Click sensor, OLED display, buzzer. |
| `BBBW_Light.py` | Lighting node — relay control, LED matrix, light power reporting. |
| `BBBW_Intrusion.py` | Intrusion node — reed switch, vibration sensor, buzzer. |
| `fakeclient.py` | PC-side simulator. Mimics all five BBBW nodes with randomised data so you can develop and test without the hardware. |

---

## Running the fake client (no hardware needed)

`fakeclient.py` lets you test the full system from any PC. It simulates all nodes — random energy readings, occasional fire events, knock detections — so the dashboard behaves as if real hardware is connected.

```bash
pip install "python-socketio[client]"
python fakeclient.py
```

Start the server first, then run the fake client. It will keep retrying the connection until the server is up.

```bash
pip install flask flask-socketio
python WebServer.py
```

Then open `http://192.168.72.221:5000` in a browser (or whatever IP you set in `WebServer.py`).

---

## Hardware (per node, varies)

- BeagleBone Black Wireless
- BME680 (I2C) — temperature, humidity, pressure, gas
- PIR motion sensor
- Adafruit SSD1306 OLED (I2C)
- MikroBUS 8×8 LED Matrix Click (SPI)
- Flame Click (analog)
- Reed switch
- Vibration / knock sensor
- Buzzer (PWM)
- Capacitive button array (analog voltage divider)

---

## Team

| Name | Role |
|---|---|
| Tan Yong Rui | Team Lead, Docs, Code |
| Braven | Art, Code, Design |
| Ong Zheng Xian | Docs, Code |
| Joycelyn Wong | Docs, Code |
| Benjamin Lee | Team Member |
