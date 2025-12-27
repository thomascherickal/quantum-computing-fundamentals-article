# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Create a circuit with 4 qubits and 4 classical bits
qc = QuantumCircuit(4, 4)

# --- Create the GHZ State ---
# 1. Put the first qubit (q0) into superposition
qc.h(0)

# 2. Cascade CNOT gates to entangle the other qubits with q0
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)

# Add a barrier for visual clarity
qc.barrier()

# Measure all four qubits
qc.measure([0, 1, 2, 3], [0, 1, 2, 3])

# Initialize and run the simulator
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts(qc)

# Print the circuit and results
print("4-Qubit GHZ State (Multi-Qubit Entanglement) Circuit:")
print(qc)
print(counts)