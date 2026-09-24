"""A tiny Bell-state simulator using only the Python standard library.

Basis order: |00>, |01>, |10>, |11>; the first bit is q0.
This is an ideal state-vector calculation, not a hardware-noise model.
"""

from math import sqrt
from random import Random


def hadamard_q0(state):
    result = [0j] * 4
    for q1 in (0, 1):
        zero = state[q1]
        one = state[2 + q1]
        result[q1] = (zero + one) / sqrt(2)
        result[2 + q1] = (zero - one) / sqrt(2)
    return result


def controlled_x_q0_q1(state):
    result = state.copy()
    result[2], result[3] = state[3], state[2]
    return result


def main():
    state = [1 + 0j, 0j, 0j, 0j]
    state = hadamard_q0(state)
    state = controlled_x_q0_q1(state)
    probabilities = [abs(amplitude) ** 2 for amplitude in state]
    assert abs(sum(probabilities) - 1) < 1e-12

    labels = ["00", "01", "10", "11"]
    print("Ideal Bell state: (|00> + |11>) / sqrt(2)")
    for label, probability in zip(labels, probabilities):
        print(f"P({label}) = {probability:.3f}")

    rng = Random(2026)  # fixed seed makes this teaching example reproducible
    samples = rng.choices(labels, weights=probabilities, k=1000)
    print("\n1000 simulated measurements (fixed seed):")
    for label in labels:
        print(f"{label}: {samples.count(label)}")
    assert samples.count("01") == samples.count("10") == 0


if __name__ == "__main__":
    main()
