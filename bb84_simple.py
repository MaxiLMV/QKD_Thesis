import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def generate_random_bits(n):
    return np.random.randint(2, size=n)

def generate_random_bases(n):
    return np.random.randint(2, size=n)

def prepare_qubits(bits, bases):
    qubits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)
        qubits.append(qc)
    return qubits

def measure_qubits(qubits, bases):
    results = []
    simulator = AerSimulator()

    for qc, basis in zip(qubits, bases):
        if basis == 1:
            qc.h(0)
        qc.measure(0, 0)

        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1).result()
        measured_bit = int(list(result.get_counts().keys())[0])
        results.append(measured_bit)

    return results

def sift_key(alice_bases, bob_bases, alice_bits):
    key = [alice_bits[i] for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
    return key

def bb84_simulation(n=10):
    alice_bits = [int(bit) for bit in generate_random_bits(n)]
    alice_bases = [int(bit) for bit in generate_random_bases(n)]

    qubits = prepare_qubits(alice_bits, alice_bases)

    bob_bases = [int(bit) for bit in generate_random_bases(n)]

    bob_results = measure_qubits(qubits, bob_bases)

    key = [int(bit) for bit in sift_key(alice_bases, bob_bases, alice_bits)]

    print(f"Alice's Bits:     {list(alice_bits)}")
    print(f"Alice's Bases:    {list(alice_bases)}")
    print(f"Bob's Bases:      {list(bob_bases)}")
    print(f"Bob's Results:    {list(bob_results)}")
    print(f"Final Shared Key: {list(key)}")

bb84_simulation(10)