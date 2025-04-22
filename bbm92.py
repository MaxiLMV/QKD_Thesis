import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Generate bases for Alice and Bob
def generate_random_bases(n):
    return np.random.randint(2, size=n)

# Create a Bell pair and measure according to Alice’s and Bob’s bases
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

def bbm92_simulation(n=10):
    alice_bases = generate_random_bases(n).tolist()
    bob_bases = generate_random_bases(n).tolist()

    simulator = AerSimulator()
    alice_results, bob_results, shared_key = [], [], []

    for a_basis, b_basis in zip(alice_bases, bob_bases):
        qc = create_bbm92_circuit(a_basis, b_basis)
        compiled = transpile(qc, simulator)
        result = simulator.run(compiled).result().get_counts()
        outcome = list(result.keys())[0]
        a_bit, b_bit = int(outcome[1]), int(outcome[0])

        alice_results.append(a_bit)
        bob_results.append(b_bit)

        if a_basis == b_basis:
            shared_key.append(a_bit)

    print("BBM92 Protocol Results:")
    print(f"Alice's Bases:    {alice_bases}")
    print(f"Bob's Bases:      {bob_bases}")
    print(f"Alice's Results:  {alice_results}")
    print(f"Bob's Results:    {bob_results}")
    print(f"Shared Key:       {shared_key}")

bbm92_simulation(10)