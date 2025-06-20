import uuid
from datetime import datetime
import random
import math
import json

# 🎯 Strict RELA modulus values (powers of 10 only)
VALID_MODULI = [10**i for i in range(3, 11)]

# 🔋 Voltage gate (odd harmonics per phase)
PHASE_VOLTAGE = {
    10**3: 1,
    10**4: 3,
    10**5: 5,
    10**6: 7,
    10**7: 9,
    10**8: 11,
    10**9: 13,
    10**10: 15
}

def assign_modulus(label):
    node_phase_map = {
        "node_1": 10**3,
        "node_2": 10**4,
        "node_3": 10**5,
        "node_4": 10**6,
        "node_5": 10**7,
        "node_6": 10**8,
        "node_7": 10**9,
        "node_8": 10**10
    }
    return node_phase_map.get(label, 10**3)

def compute_voltage(distance, harmonic=1):
    return round(1 / (distance * harmonic), 10)

def compute_semantic_current(voltage, harmonic):
    return round(voltage * harmonic - math.sin(harmonic), 10)

def generate_entangled_pair(modulus):
    # Ensure a + b = modulus, and a ≠ b to avoid symmetrical repetition
    a = random.randint(1, modulus - 1)
    b = modulus - a
    return [a, b]

def compute_spiral_score(distance, modulus, voltage):
    ideal_voltage = compute_voltage(modulus, PHASE_VOLTAGE[modulus])
    delta_v = abs(voltage - ideal_voltage)
    if delta_v < 0.01:
        return "🟢 Harmonic", 100
    elif delta_v < 0.05:
        return "🟡 Near-Harmonic", 70
    else:
        return "🔴 Chaotic", 20

def create_loop(label, distance, parent_id=None):
    modulus = assign_modulus(label)
    harmonic = PHASE_VOLTAGE[modulus]
    voltage = compute_voltage(distance, harmonic)
    semantic_current = compute_semantic_current(voltage, harmonic)
    entangled_pair = generate_entangled_pair(modulus)
    spiral_score, harmonic_score = compute_spiral_score(distance, modulus, voltage)

    loop = {
        "id": f"txn_{str(uuid.uuid4())[:8]}",
        "label": label,
        "distance": distance,
        "voltage": voltage,
        "modulus": modulus,
        "semantic_current": semantic_current,
        "entangled_pair": entangled_pair,
        "validator_phase": modulus,
        "timestamp": datetime.utcnow().isoformat(),
        "parent_id": parent_id,
        "spiral_score": spiral_score,
        "harmonic_score": harmonic_score
    }

    save_loop_to_ledger(loop)
    return loop

def save_loop_to_ledger(loop):
    try:
        with open("ledger/ledger.json", "r") as f:
            ledger = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        ledger = []

    ledger.append(loop)

    with open("ledger/ledger.json", "w") as f:
        json.dump(ledger, f, indent=2)
