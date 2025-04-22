import pytest
import numpy as np
import e91

def test_generate_random_bases_e91_range():
    n = 25
    bases = e91.generate_random_bases_e91(n)
    assert len(bases) == n
    assert all(b in [0, 1, 2] for b in bases)

def test_create_e91_circuit_structure():
    qc = e91.create_e91_circuit(2, 1)
    assert qc.num_qubits == 2
    assert qc.num_clbits == 2

def test_zero_qubits_simulation():
    n = 0
    alice_bases = []
    bob_bases = []
    simulator = e91.AerSimulator()

    alice_results, bob_results, shared_key = [], [], []

    for a_basis, b_basis in zip(alice_bases, bob_bases):
        qc = e91.create_e91_circuit(a_basis, b_basis)
        compiled = e91.transpile(qc, simulator)
        result = simulator.run(compiled, shots=1).result().get_counts()
        outcome = list(result.keys())[0]
        a_bit = int(outcome[0])
        b_bit = int(outcome[1])
        alice_results.append(a_bit)
        bob_results.append(b_bit)
        if a_basis == b_basis:
            shared_key.append(a_bit)

    assert alice_results == []
    assert bob_results == []
    assert shared_key == []