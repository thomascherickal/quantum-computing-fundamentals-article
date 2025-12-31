# Import necessary components
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# --- Define an arbitrary initial state for one qubit ---
# This is the state we want to clone.
initial_state_vector = np.array([np.sqrt(0.7), np.sqrt(0.3)])

# --- Calculate the "perfect" cloned state vector (hypothetical) ---
# A perfect clone would be the tensor product of the state with itself.
perfect_clone_state = np.kron(initial_state_vector, initial_state_vector)

# --- Build a circuit that attempts to "clone" the state ---
# We initialize q0 to our arbitrary state and try to copy it to q1.
qc = QuantumCircuit(2)
qc.initialize(initial_state_vector, 0) # Prepare q0 in the desired state
qc.cx(0, 1) # Use a CNOT as a "copying" mechanism

# --- Get the actual final state vector from the circuit ---
actual_final_state = Statevector(qc)

# --- Compare the states ---
print("Initial State to Clone: |psi> = sqrt(0.7)|0> + sqrt(0.3)|1>")
print("\nHypothetical 'Perfect' Cloned State |psi>|psi>:")
print(np.round(perfect_clone_state, 3))
print("\nActual State from CNOT 'Copy' Circuit:")
print(np.round(actual_final_state.data, 3))