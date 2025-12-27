# Import necessary components
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

# --- Setup ---
q = QuantumRegister(3, 'q')
anc = QuantumRegister(2, 'ancilla')
c = ClassicalRegister(2, 'syndrome')
qc = QuantumCircuit(q, anc, c)

# --- 1. State Preparation & Encoding ---
qc.h(q[0])
qc.cx(q[0], q[1])
qc.cx(q[0], q[2])
qc.barrier()

# --- 2. Introduce an Error ---
error_qubit = 1
qc.x(q[error_qubit])
qc.barrier()

# --- 3. Syndrome Measurement ---
qc.cx(q[0], anc[0])
qc.cx(q[1], anc[0])
qc.cx(q[1], anc[1])
qc.cx(q[2], anc[1])
qc.measure(anc[0], c[0])
qc.measure(anc[1], c[1])
qc.barrier()

# --- 4. Conditional Correction ---
with qc.if_test((c, int('10', 2))):
    qc.x(q[1])

# --- Verification (Optional) ---
qc.cx(q[0], q[1])
qc.cx(q[0], q[2])
qc.h(q[0])
final_measure = ClassicalRegister(1, 'final')
qc.add_register(final_measure)
qc.measure(q[0], final_measure[0])

# --- Simulation ---
simulator = AerSimulator()
result = simulator.run(transpile(qc, simulator), shots=100).result()
print("Bit-Flip Error Correction Circuit:")
print(qc)