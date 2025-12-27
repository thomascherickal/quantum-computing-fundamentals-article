import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import Parameter
from qiskit.primitives import StatevectorEstimator

# ---------------------------------------------------------
# STEP 1: Define the Problem (The Hamiltonian)
# ---------------------------------------------------------
print("--- Step 1: Defining the Hamiltonian ---")
# We will solve for the ground state energy of a simple 2-qubit system.
# Hamiltonian: H = Z ^ Z + J * (X ^ I)
# This represents a simple Ising model interactions.

# 'ZZ' acts on qubit 0 and 1. 'XI' acts on qubit 0.
hamiltonian = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0)])
print(f"Hamiltonian Operator:\n{hamiltonian}")

# Calculate the exact reference value using standard linear algebra (NumPy)
# This lets us check if our VQE actually works.
matrix = hamiltonian.to_matrix()
exact_eigenvalue = np.min(np.linalg.eigvalsh(matrix))
print(f"Target (Exact) Energy: {exact_eigenvalue:.4f}\n")


# ---------------------------------------------------------
# STEP 2: Create the Ansatz (Parameterized Circuit)
# ---------------------------------------------------------
print("--- Step 2: Creating the Ansatz Circuit ---")

# We need a circuit that can explore the Hilbert space.
# We will use a simple "Hardware Efficient" ansatz:
# 1. Rotations (RY) on both qubits to prepare superpositions.
# 2. Entanglement (CX) to correlate them.
# 3. Parameterized so the optimizer can tune it.

theta = Parameter('θ')
phi = Parameter('φ')

ansatz = QuantumCircuit(2)
ansatz.ry(theta, 0)  # Rotation on Qubit 0
ansatz.ry(phi, 1)    # Rotation on Qubit 1
ansatz.cx(0, 1)      # Entanglement

print("Ansatz Circuit Diagram:")
print(ansatz.draw(output='text'))
print(f"Parameters to optimize: {ansatz.parameters}\n")


# ---------------------------------------------------------
# STEP 3: Define the Cost Function
# ---------------------------------------------------------
print("--- Step 3: Defining the Cost Function (Expectation Value) ---")

# In Qiskit 1.0+, we use the 'Estimator' primitive.
# It replaces QuantumInstance. It takes a circuit and an observable
# and calculates <psi | H | psi>.
estimator = StatevectorEstimator()

def cost_function(params):
    """
    Accepts a list of parameters (angles), runs the circuit,
    and returns the expected energy.
    """
    # The Estimator expects inputs in a specific structure (pub = primitive unified bloc)
    # (circuit, observable, parameter_values)
    
    # 1. Bind the classical optimizer's values to the circuit parameters
    pub = (ansatz, hamiltonian, params)
    
    # 2. Run the job
    job = estimator.run([pub])
    
    # 3. Extract the result (energy)
    result = job.result()[0]
    energy = result.data.evs
    
    # Print the step for visualization
    # Note: We cast to float because the estimator returns a numpy array
    print(f"Evaluated params {params} -> Energy: {float(energy):.4f}")
    
    return energy


# ---------------------------------------------------------
# STEP 4: Run the Classical Optimization
# ---------------------------------------------------------
print("--- Step 4: Running Classical Optimization (VQE Loop) ---")

# Initial guess for the angles (e.g., [0, 0])
initial_params = [0.0, 0.0]

print(f"Starting optimization with initial guess: {initial_params}")
print("Optimizer: COBYLA (via scipy.optimize)\n")

# Use Scipy to minimize the cost function
result = minimize(
    cost_function, 
    initial_params, 
    method='COBYLA', 
    options={'maxiter': 20, 'tol': 1e-4}
)

print("\n--- Optimization Complete ---")
print(f"Success: {result.success}")
print(f"VQE Final Energy:   {result.fun:.4f}")
print(f"Exact Target Energy: {exact_eigenvalue:.4f}")

difference = abs(result.fun - exact_eigenvalue)
print(f"Accuracy Difference: {difference:.6f}")