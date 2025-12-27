# Import necessary components
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# --- Function to build the QFT circuit ---
def qft_circuit(n):
    """Builds a QFT circuit on n qubits."""
    qc = QuantumCircuit(n, name=f'QFT({n})')
    # Apply the rotations
    for j in range(n):
        qc.h(j)
        for k in range(j + 1, n):
            # Controlled-Phase rotation
            qc.cp(np.pi / 2**(k - j), k, j)
    # Swap the qubits at the end to match the mathematical definition
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc

# --- Main Program ---
num_qubits = 3
# Create the input state |101> (which is 5 in decimal)
input_qc = QuantumCircuit(num_qubits)
input_qc.x(0)
input_qc.x(2)
initial_state = Statevector(input_qc)

# Create the QFT circuit
qft = qft_circuit(num_qubits)

# Apply the QFT to the input state
full_circuit = input_qc.compose(qft)
final_state = Statevector(full_circuit)

# --- Print Results ---
print(f"Input State: |101> (Decimal 5)")
print(initial_state.draw('text'))
print(f"\n{num_qubits}-Qubit QFT Circuit:")
print(qft)
print("\nFinal State after QFT:")
print(final_state.draw('text'))