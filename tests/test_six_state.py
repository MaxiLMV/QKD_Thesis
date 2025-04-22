import pytest
import numpy as np
import six_state

# Test if the number of generated bits matches the requested amount
def test_generate_random_bits_length():
    n = 20
    bits = six_state.generate_random_bits(n)
    assert len(bits) == n
    assert all(b in [0, 1] for b in bits)

# Test that each generated basis is within expected range {0, 1, 2}
def test_generate_random_bases_range():
    n = 20
    bases = six_state.generate_random_bases(n)
    assert len(bases) == n
    assert all(b in [0, 1, 2] for b in bases)

# Test that prepare_six_state_qubit returns a single-qubit circuit object
def test_prepare_six_state_qubit_returns_circuit():
    qc = six_state.prepare_six_state_qubit(1, 2)
    assert qc.num_qubits == 1
    assert isinstance(qc, six_state.QuantumCircuit)

# Tets that a simulation with 0 qubits doesn't break anything
def test_zero_qubits_simulation():
    n = 0
    alice_bits = []
    alice_bases = []
    bob_bases = []
    simulator = six_state.AerSimulator()

    bob_results, shared_key = [], []

    for a_bit, a_basis, b_basis in zip(alice_bits, alice_bases, bob_bases):
        qc = six_state.prepare_six_state_qubit(a_bit, a_basis)
        qc = six_state.measure_six_state_qubit(qc, b_basis)
        compiled = six_state.transpile(qc, simulator)
        result = simulator.run(compiled, shots=1).result().get_counts()
        outcome = list(result.keys())[0]
        b_bit = int(outcome)
        bob_results.append(b_bit)
        if a_basis == b_basis:
            shared_key.append(a_bit)

    assert bob_results == []
    assert shared_key == []