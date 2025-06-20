from core.loop_model import create_loop, assign_modulus, assign_voltage_gate, compute_voltage
import json

LEDGER_PATH = "ledger/ledger.json"
CHAOS_PATH = "chaos_tracker.json"

def load_ledger():
    try:
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_ledger(data):
    with open(LEDGER_PATH, "w") as f:
        json.dump(data, f, indent=2)

def load_chaos():
    try:
        with open(CHAOS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_chaos(data):
    with open(CHAOS_PATH, "w") as f:
        json.dump(data, f, indent=2)

def validate_loop(loop, expected_modulus, node_id):
    chaos = load_chaos()
    key = f"node_{node_id}"
    if loop["modulus"] != expected_modulus or abs(loop["semantic_current"]) > 0.1:
        chaos[key] = chaos.get(key, 0) + 1
        save_chaos(chaos)
        print(f"❌ Node {node_id} rejected loop: invalid modulus or ΔV too high.")
    else:
        ledger = load_ledger()
        ledger.append(loop)
        save_ledger(ledger)
        chaos[key] = 0
        save_chaos(chaos)
        print(f"✅ Node {node_id} accepted loop {loop['id']}.")

label = "node_1"
modulus = assign_modulus(label)
distance = modulus
prev_voltage = compute_voltage(distance + 1)
loop = create_loop("loop_node1", label, distance, prev_voltage)
validate_loop(loop, modulus, 1)
