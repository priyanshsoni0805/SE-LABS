"""Smart home device controller.

Adds devices to rooms, toggles them, sets the thermostat within a safe range,
lists devices by room, reports power use and saves state to home_state.json.

Author: Priyansh Soni (PES1UG24CS344)
"""
import json
import os
import subprocess  # nosec B404
from pathlib import Path

# Bandit B104: bind to loopback only, not every network interface
HUB_HOST = "127.0.0.1"
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
MIN_TEMP = 16
MAX_TEMP = 30
# Bandit B105: secret comes from the environment, never from source code
HUB_PASSWORD = os.environ.get("HUB_PASSWORD", "")
SCENES_DIR = Path(__file__).resolve().parent / "scenes"
DEVICES = {}


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device. Each device gets its own settings dictionary."""
    DEVICES[device_name] = {"kind": kind, "room": room, "on": False,
                            "settings": dict(settings) if settings else {}}


def toggle_device(device_name):
    """Flip a device on/off and return its new state (None if unknown)."""
    if device_name in DEVICES:
        DEVICES[device_name]["on"] = not DEVICES[device_name]["on"]
        return DEVICES[device_name]["on"]
    print("Device not found:", device_name)
    return None


def set_temperature(device_name, value):
    """Set a thermostat's temperature, clamped to MIN_TEMP..MAX_TEMP."""
    device = DEVICES.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(max(value, MIN_TEMP), MAX_TEMP)
    return True


def devices_in_room(room):
    """Return the names of all devices in the given room."""
    return [name for name, info in DEVICES.items() if info["room"] == room]


def power_usage():
    """Return the total power draw (W) of all devices that are on."""
    active = [info for info in DEVICES.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)


def save_state(file_name="home_state.json"):
    """Write the current home state to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as state_file:
        json.dump(DEVICES, state_file, indent=2)


def hub_address():
    """Return the hub address as host:port."""
    return HUB_HOST + ":" + str(HUB_PORT)


def run_scene(scene_script):
    """Run a *.sh scene script from the scenes folder (no shell involved)."""
    # Bandit B602: only plain *.sh files inside SCENES_DIR may run, so a name
    # like "x; rm -rf ~" or "../evil.sh" is rejected, not executed.
    script = SCENES_DIR / scene_script
    if (Path(scene_script).name != scene_script or script.suffix != ".sh"
            or not script.is_file()):
        raise ValueError("Invalid scene script: " + scene_script)
    # Arguments are a list and the script name is validated above, so this
    # call cannot be used for command injection.
    subprocess.run(["/bin/bash", str(script)], check=True)  # nosec B603


def main():
    """Run a short demonstration."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", DEVICES["Ceiling Light"]["settings"])
    devices_on = [name for name, info in DEVICES.items() if info["on"]]
    print("Devices on:", devices_on)
    save_state()


if __name__ == "__main__":
    main()
