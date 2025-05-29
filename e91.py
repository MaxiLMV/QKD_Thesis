import time
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Choose one of three numbers for bases
def generate_random_bases(n):
    return np.random.choice([0, 1, 2], size=n)

# Create a Bell pair and measure according to Alice’s and Bob’s bases
def create_e91_circuit(alice_basis, bob_basis):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)

    if alice_basis == 1:
        qc.h(0)
    elif alice_basis == 2:
        qc.sdg(0)
        qc.h(0)

    if bob_basis == 1:
        qc.h(1)
    elif bob_basis == 2:
        qc.sdg(1)
        qc.h(1)

    qc.measure([0, 1], [0, 1])
    return qc

# Calculate quantum bit error rate
def calculate_qber(alice_bits, bob_bits):
    if not alice_bits:
        return 0.0
    errors = sum(1 for a, b in zip(alice_bits, bob_bits) if a != b)
    return errors / len(alice_bits)

def e91_simulation(n=10):
    start_time = time.time()

    alice_bases = generate_random_bases(n).tolist()
    bob_bases = generate_random_bases(n).tolist()

    simulator = AerSimulator()
    alice_results, bob_results = [], []
    matching_alice_bits, matching_bob_bits = [], []

    for a_basis, b_basis in zip(alice_bases, bob_bases):
        qc = create_e91_circuit(a_basis, b_basis)
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=1).result().get_counts()
        outcome = list(result.keys())[0]

        a_bit = int(outcome[0])
        b_bit = int(outcome[1])

        alice_results.append(a_bit)
        bob_results.append(b_bit)

        if a_basis == b_basis:
            matching_alice_bits.append(a_bit)
            matching_bob_bits.append(b_bit)

    shared_key = matching_alice_bits
    qber = calculate_qber(matching_alice_bits, matching_bob_bits)

    end_time = time.time()
    runtime = end_time - start_time

    print("E91 Protocol Results:")
    print(f"Alice's Bases:    {alice_bases}")
    print(f"Bob's Bases:      {bob_bases}")
    print(f"Alice's Results:  {alice_results}")
    print(f"Bob's Results:    {bob_results}")
    print(f"Shared Key:       {shared_key}")
    print(f"QBER:             {qber:.2f}")
    print(f"Runtime:          {runtime:.4f} seconds")

e91_simulation()