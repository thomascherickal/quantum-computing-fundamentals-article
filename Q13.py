# Import necessary components
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- Function for inverse QFT ---
def qft_dagger(qc, n):
    """Builds an inverse QFT circuit on n qubits."""
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / (2**(j - m)), m, j)
        qc.h(j)

# --- Main QPE Circuit ---
# Use 3 qubits for the counting register and 1 for the state register
qc = QuantumCircuit(4, 3)

# --- Step 1: Prepare the Eigenvector ---
# We want to find the phase for the eigenvector |1> of the Z gate.
qc.x(3)
qc.barrier()

# --- Step 2: Superposition on Counting Register ---
qc.h(range(3))

# --- Step 3: Controlled Unitary Operations ---
# The unitary is the Z gate. We apply controlled-Z^(2^k).
qc.cz(0, 3)
qc.barrier()

# --- Step 4: Inverse QFT ---
qft_dagger(qc, 3)
qc.barrier()

# --- Step 5: Measurement ---
qc.measure(range(3), range(3))

# Simulate the circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

# Print results
print("QPE Circuit for Z-gate with eigenvector |1>:")
print(qc)
print("Measurement Counts:", counts)