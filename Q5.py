# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# Create a circuit with 3 qubits and 2 classical bits
# q0: input A
# q1: input B / output Sum
# q2: output Carry
qc = QuantumCircuit(3, 2)

# --- Prepare Inputs ---
# We want to compute 1 + 1, so we set q0 and q1 to |1>
qc.x(0)
qc.x(1)
qc.barrier()

# --- Half-Adder Logic ---
# 1. Calculate the Carry bit (A AND B)
# The Toffoli gate (ccx) flips the target (q2) if both controls (q0, q1) are 1.
qc.ccx(0, 1, 2)

# 2. Calculate the Sum bit (A XOR B)
# The CNOT gate flips the target (q1) if the control (q0) is 1.
qc.cx(0, 1)
qc.barrier()

# --- Measurement ---
# Measure the Sum (q1) and Carry (q2)
qc.measure(1, 0) # Map q1 to classical bit 0 (Sum)
qc.measure(2, 1) # Map q2 to classical bit 1 (Carry)

# Simulate the circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1).result()
counts = result.get_counts()

# Print the circuit and the result
print("Quantum Half-Adder Circuit for 1 + 1:")
print(qc)