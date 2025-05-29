import time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Generate bits for Alice
def generate_random_bits(n):
    return np.random.randint(2, size=n)

# Generate bases for Alice and Bob
def generate_random_bases(n):
    return np.random.randint(2, size=n)

# Prepare qubits based on Alice's bits and bases
def prepare_bb84_qubits(bits, bases):
    circuits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)
        circuits.append(qc)
    return circuits

# Perform a measurement on Bob's side
def measure_bb84_qubits(circuits, bases):
    simulator = AerSimulator()
    results = []

    for qc, basis in zip(circuits, bases):
        if basis == 1:
            qc.h(0)
        qc.measure(0, 0)
        compiled = transpile(qc, simulator)
        outcome = simulator.run(compiled, shots=1).result().get_counts()
        bit = int(list(outcome.keys())[0])

        if np.random.rand() < 0.1: # 10% error rate
            bit = 1 - bit

        results.append(bit)

    return results

# Extract bits where bases match
def sift_key(alice_bases, bob_bases, alice_bits):
    return [alice_bits[i] for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]

# Calculate quantum bit error rate
def calculate_qber(alice_bits, bob_bits, alice_bases, bob_bases):
    matching_indices = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
    if not matching_indices:
        return 0.0
    errors = sum(1 for i in matching_indices if alice_bits[i] != bob_bits[i])
    return errors / len(matching_indices)

def bb84_simulation(n=10):
    start_time = time.time()

    alice_bits = generate_random_bits(n).tolist()
    alice_bases = generate_random_bases(n).tolist()
    bob_bases = generate_random_bases(n).tolist()

    circuits = prepare_bb84_qubits(alice_bits, alice_bases)
    bob_results = measure_bb84_qubits(circuits, bob_bases)
    shared_key = sift_key(alice_bases, bob_bases, alice_bits)
    qber = calculate_qber(alice_bits, bob_results, alice_bases, bob_bases)

    end_time = time.time()
    runtime = end_time - start_time

    print("BB84 Protocol Results:")
    print(f"Alice's Bits:     {alice_bits}")
    print(f"Alice's Bases:    {alice_bases}")
    print(f"Bob's Bases:      {bob_bases}")
    print(f"Bob's Results:    {bob_results}")
    print(f"Shared Key:       {shared_key}")
    print(f"QBER:             {qber:.2f}")
    print(f"Runtime:          {runtime:.4f} seconds")

bb84_simulation()