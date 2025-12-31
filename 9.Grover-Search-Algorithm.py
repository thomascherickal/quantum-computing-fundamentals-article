# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# --- Define the Oracle ---
# The oracle marks the state |101> by flipping its phase.
oracle = QuantumCircuit(3, name='Oracle (101)')
oracle.x(1) # We want to match |101>, so we flip the middle qubit for the CCZ
oracle.ccz(0, 1, 2)
oracle.x(1)
oracle_gate = oracle.to_gate()

# --- Define the Diffusion Operator ---
diffuser = QuantumCircuit(3, name='Diffuser')
diffuser.h([0, 1, 2])
diffuser.x([0, 1, 2])
diffuser.ccz(0, 1, 2)
diffuser.x([0, 1, 2])
diffuser.h([0, 1, 2])
diffuser_gate = diffuser.to_gate()

# --- Build the Main Grover's Circuit ---
qc = QuantumCircuit(3, 3)

# 1. Initial superposition
qc.h([0, 1, 2])
qc.barrier()

# 2. Apply Grover iterations (Oracle + Diffuser)
num_iterations = 2
for _ in range(num_iterations):
    qc.append(oracle_gate, [0, 1, 2])
    qc.append(diffuser_gate, [0, 1, 2])
    qc.barrier()

# 3. Measure the result
qc.measure([0, 1, 2], [0, 1, 2])

# Simulate the circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

# Print results
print("Grover's Search Circuit for |101>:")
print(qc)