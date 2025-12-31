# Import necessary components
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# Create a circuit with one qubit
qc = QuantumCircuit(1)

# Apply a Hadamard gate to create superposition (50/50 chance)
qc.h(0)

# Measure the final state
qc.measure_all()

# --- Run the simulation 1024 times ---
# Use the Qiskit Aer simulator backend
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts(qc)

print("Circuit:")
print(qc)

# Plotting the histogram shows the simulated probabilities
plot_histogram(counts, title="Simulation Results (50/50)").savefig('Q6.png')