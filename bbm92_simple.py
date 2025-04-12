import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_random_bits(n):
    return np.random.randint(0, 2, n)

def generate_random_bases(n):
    return np.random.randint(0, 2, n)

def create_bbm92_circuit(alice_basis, bob_basis):
    qc = QuantumCircuit(2, 2)

    qc.h(0)
    qc.cx(0, 1)

    if alice_basis == 1:
        qc.sdg(0)
        qc.h(0)
    qc.measure(0, 0)

    if bob_basis == 1:
        qc.sdg(1)
        qc.h(1)
    qc.measure(1, 1)

    return qc

def bbm92_simulation(n):
    alice_bases = generate_random_bases(n)
    bob_bases = generate_random_bases(n)

    simulator = AerSimulator()
    shared_key = []
    alice_measurements = []
    bob_measurements = []

    for i in range(n):
        qc = create_bbm92_circuit(alice_bases[i], bob_bases[i])
        transpiled_qc = transpile(qc, simulator)
        result = simulator.run(transpiled_qc).result()
        outcome = result.get_counts()

        measured_bits = max(outcome, key=outcome.get)
        alice_bit, bob_bit = int(measured_bits[1]), int(measured_bits[0])

        alice_measurements.append(alice_bit)
        bob_measurements.append(bob_bit)

        if alice_bases[i] == bob_bases[i]:
            shared_key.append(alice_bit)

    alice_bases = [int(bit) for bit in alice_bases]
    bob_bases = [int(bit) for bit in bob_bases.tolist()]
    alice_measurements = [int(bit) for bit in alice_measurements]
    bob_measurements = [int(bit) for bit in bob_measurements]
    shared_key = shared_key

    return alice_bases, bob_bases, alice_measurements, bob_measurements, shared_key

alice_bases, bob_bases, alice_results, bob_results, final_key = bbm92_simulation(10)

print("Alice's Bases:    ", list(alice_bases))
print("Bob's Bases:      ", list(bob_bases))
print("Alice's Results:  ", list(alice_results))
print("Bob's Results:    ", list(bob_results))
print("Final Shared Key: ", list(final_key))