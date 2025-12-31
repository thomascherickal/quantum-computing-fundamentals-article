# Import necessary components
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import NumPyMinimumEigensolver
import numpy as np

# --- Define the Hamiltonian ---
# H = XX + ZZ
hamiltonian = SparsePauliOp.from_list([("XX", 1.0), ("ZZ", 1.0)])

# --- Use a classical exact solver to find the ground state ---
exact_solver = NumPyMinimumEigensolver()
result = exact_solver.compute_minimum_eigenvalue(hamiltonian)

ground_state_energy = result.eigenvalue.real
ground_state = result.eigenstate.to_dict()

# --- Print the Results ---
print(f"Hamiltonian H = XX + ZZ")
print(f"\nCalculated Ground State Energy (Lowest Eigenvalue): {ground_state_energy:.4f}")
print("\nCorresponding Ground State (Eigenvector):")
print(ground_state)