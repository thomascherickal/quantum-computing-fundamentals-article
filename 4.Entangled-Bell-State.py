# Import necessary components
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Create a circuit with 2 qubits
qc = QuantumCircuit(2)

# --- Initial State ---
# By default, the state is |00>
initial_state = Statevector(qc)
print("Initial State (|00>):")
print(initial_state.draw('text'))

# --- Step 1: Create Superposition on Control Qubit ---
# Apply a Hadamard gate to the control qubit (q0)
qc.h(0)
state_after_h = Statevector(qc)
print("\nState after H-gate on q0 (Superposition):")
print(state_after_h.draw('text'))

# --- Step 2: Apply CNOT Gate ---
# Apply a CNOT with q0 as control and q1 as target
qc.cx(0, 1)
final_state = Statevector(qc)
print("\nFinal State after CNOT (Entangled Bell State):")
print(final_state.draw('text'))

print("\nCircuit Diagram:")
print(qc)