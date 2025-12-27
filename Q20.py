# Import necessary components
import random
import time
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- Circuit Parameters ---
num_qubits = 10
depth = 10

# --- Build a Random Quantum Circuit ---
qc = QuantumCircuit(num_qubits)
gates_1q = ['h', 's', 't', 'x']
gates_2q = ['cx', 'cz']

for d in range(depth):
    # Add a layer of single-qubit gates
    for i in range(num_qubits):
        gate = random.choice(gates_1q)
        getattr(qc, gate)(i)
    # Add a layer of two-qubit gates
    qubit_pairs = random.sample(range(num_qubits), num_qubits)
    for i in range(0, num_qubits, 2):
        q1, q2 = qubit_pairs[i], qubit_pairs[i+1]
        gate = random.choice(gates_2q)
        getattr(qc, gate)(q1, q2)
    qc.barrier()

qc.measure_all()

# --- Simulate the Circuit and Time it ---
simulator = AerSimulator(method='statevector')
print(f"Simulating a random circuit with {num_qubits} qubits and depth {depth}...")
start_time = time.time()
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit, shots=10).result()
end_time = time.time()
qc.draw(output='mpl', filename='quantum_advantage_long.png', fold=-1)

# --- Print Results ---
print(f"Simulation finished in {end_time - start_time:.4f} seconds.")
print("\nSampled outcomes from the random circuit's distribution:")
print(result.get_counts())