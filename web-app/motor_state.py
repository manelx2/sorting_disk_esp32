import json
import os

MOTOR_STATE_FILE = "motor_state.json"

DEFAULT_STATE = {
    "servo_angle": 45,
    "conveyor_speed": 100
}

def load_motor_state():
    if not os.path.exists(MOTOR_STATE_FILE):
        save_motor_state(DEFAULT_STATE)
    with open(MOTOR_STATE_FILE, 'r') as f:
        return json.load(f)

def save_motor_state(state):
    with open(MOTOR_STATE_FILE, 'w') as f:
        json.dump(state, f)
