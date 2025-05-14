import pytest
import bb84

# Test if the number of generated bits matches the requested amount
def test_generate_random_bits_length():
    n = 20
    bits = bb84.generate_random_bits(n)
    assert len(bits) == n
    assert all(bit in [0, 1] for bit in bits)

# Test if the number of generated bases matches the requested amount
def test_generate_random_bases_length():
    n = 20
    bases = bb84.generate_random_bases(n)
    assert len(bases) == n
    assert all(b in [0, 1] for b in bases)

# Test that sifting keeps only bits where the bases match
def test_sift_key_matching_bases():
    alice_bases = [0, 1, 1, 0, 1]
    bob_bases   = [0, 0, 1, 1, 1]
    alice_bits  = [1, 0, 1, 0, 1]
    expected_key = [1, 1, 1]
    key = bb84.sift_key(alice_bases, bob_bases, alice_bits)
    assert key == expected_key

# Test that a simulation with 0 qubits doesn't break anything
def test_zero_qubits_simulation():
    alice_bits = []
    alice_bases = []
    bob_bases = []

    circuits = bb84.prepare_bb84_qubits(alice_bits, alice_bases)
    results = bb84.measure_bb84_qubits(circuits, bob_bases)
    shared_key = bb84.sift_key(alice_bases, bob_bases, alice_bits)

    assert circuits == []
    assert results == []
    assert shared_key == []

# Test that Eve's intercept and resend process creates circuits and results of correct length
def test_eve_intercept_and_resend_length():
    alice_bits = [0, 1, 1, 0]
    alice_bases = [0, 0, 1, 1]
    eve_bases = [1, 0, 1, 0]
    circuits = bb84.prepare_bb84_qubits(alice_bits, alice_bases)
    new_circuits, eve_results = bb84.eve_intercept_and_resend(circuits, eve_bases)
    assert len(new_circuits) == len(eve_results) == len(alice_bits)

# Test that QBER returns expected value for mismatched results
def test_calculate_qber_correctness():
    alice_bits  = [0, 1, 1, 0, 1]
    bob_bits    = [0, 0, 0, 1, 1]
    alice_bases = [0, 1, 1, 0, 1]
    bob_bases   = [0, 0, 1, 1, 1]
    qber = bb84.calculate_qber(alice_bits, bob_bits, alice_bases, bob_bases)
    assert qber == pytest.approx(1/3)