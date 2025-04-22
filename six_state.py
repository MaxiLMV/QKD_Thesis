import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Generate bits for Alice
def generate_random_bits(n):
    return np.random.randint(2, size=n)

# Choose one of three numbers for bases
def generate_random_bases(n):
    return np.random.choice([0, 1, 2], size=n)

# Prepare the qubit
def prepare_six_state_qubit(bit, basis):
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == 1:
        qc.h(0)
    elif basis == 2:
        qc.h(0)
        qc.s(0)
    return qc

# Perform a measurement on Bob's side
def measure_six_state_qubit(qc, basis):
    if basis == 1:
        qc.h(0)
    elif basis == 2:
        qc.sdg(0)
        qc.h(0)
    qc.measure(0, 0)
    return qc

def six_state_simulation(n=10):
    alice_bits = generate_random_bits(n).tolist()
    alice_bases = generate_random_bases(n).tolist()
    bob_bases = generate_random_bases(n).tolist()

    simulator = AerSimulator()
    bob_results, shared_key = [], []

    for a_bit, a_basis, b_basis in zip(alice_bits, alice_bases, bob_bases):
        qc = prepare_six_state_qubit(a_bit, a_basis)
        qc = measure_six_state_qubit(qc, b_basis)

        compiled = transpile(qc, simulator)
        result = simulator.run(compiled, shots=1).result().get_counts()
        outcome = list(result.keys())[0]
        b_bit = int(outcome)
        bob_results.append(b_bit)

        if a_basis == b_basis:
            shared_key.append(a_bit)

    print("Six-State Protocol Results:")
    print(f"Alice's Bits:     {alice_bits}")
    print(f"Alice's Bases:    {alice_bases}")
    print(f"Bob's Bases:      {bob_bases}")
    print(f"Bob's Results:    {bob_results}")
    print(f"Shared Key:       {shared_key}")

six_state_simulation(10)