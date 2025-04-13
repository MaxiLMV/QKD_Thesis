import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_random_bits(n):
    return np.random.randint(2, size=n)

def generate_random_bases(n):
    return np.random.randint(2, size=n)

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
        results.append(bit)

    return results

def sift_key(alice_bases, bob_bases, alice_bits):
    return [alice_bits[i] for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]

def bb84_simulation(n=10):
    alice_bits = generate_random_bits(n).tolist()
    alice_bases = generate_random_bases(n).tolist()
    bob_bases = generate_random_bases(n).tolist()

    circuits = prepare_bb84_qubits(alice_bits, alice_bases)
    bob_results = measure_bb84_qubits(circuits, bob_bases)
    shared_key = sift_key(alice_bases, bob_bases, alice_bits)

    print("BB84 Protocol Results:")
    print(f"Alice's Bits:     {alice_bits}")
    print(f"Alice's Bases:    {alice_bases}")
    print(f"Bob's Bases:      {bob_bases}")
    print(f"Bob's Results:    {bob_results}")
    print(f"Shared Key:       {shared_key}")

bb84_simulation(10)