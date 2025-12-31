# Import necessary components
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Create a circuit with one qubit and one classical bit
qc = QuantumCircuit(1, 1)

# --- Prepare a Biased Superposition ---
# A Y-rotation by angle theta sets the state to cos(theta/2)|0> + sin(theta/2)|1>.
# To get Prob(1) = 0.75, we need sin(theta/2) = sqrt(0.75), so theta = 2 * arcsin(sqrt(0.75)) = pi * 2/3.
angle = 2 * np.pi / 3
qc.ry(angle, 0)

# --- Measurement ---
qc.measure(0, 0)

# Simulate the circuit
shots = 4096
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=shots).result()
counts = result.get_counts(qc)

# Print the results and theoretical probabilities
print("Circuit with Biased Superposition (75% |1>):")
print(qc)
print("Counts:", counts)