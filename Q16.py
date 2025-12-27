import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator, StatevectorSampler

# ---------------------------------------------------------
# STEP 1: Define the Hamiltonian
# ---------------------------------------------------------
print("=== Step 1: Defining the Hamiltonian ===")
# Edges for a triangle graph: (0,1), (1,2), (0,2)
hamiltonian = SparsePauliOp.from_list([
    ("ZZI", 1.0),  # Edge (0, 1)
    ("IZZ", 1.0),  # Edge (1, 2)
    ("ZIZ", 1.0)   # Edge (0, 2)
])
print(f"Hamiltonian: {hamiltonian}\n")

# ---------------------------------------------------------
# STEP 2: Define the QAOA Circuit Building Function
# ---------------------------------------------------------
def create_qaoa_circuit(params, reps, n_qubits=3):
    """
    Constructs the QAOA Ansatz manually.
    """
    qc = QuantumCircuit(n_qubits)
    
    # 1. Initialization: Equal Superposition
    qc.h(range(n_qubits))
    
    # Split params
    gammas = params[0::2]
    betas = params[1::2]
    
    # 2. Apply Layers
    for i in range(reps):
        gamma = gammas[i]
        beta = betas[i]
        
        # --- Cost Layer (RZZ) ---
        qc.rzz(2 * gamma, 0, 1) 
        qc.rzz(2 * gamma, 1, 2) 
        qc.rzz(2 * gamma, 0, 2) 
        
        # --- Mixer Layer (RX) ---
        for q in range(n_qubits):
            qc.rx(2 * beta, q)
            
    return qc

# ---------------------------------------------------------
# NEW STEP: Print the Circuit Once
# ---------------------------------------------------------
print("=== Visualizing the QAOA Circuit Structure ===")
# We define initial parameters just for visualization purposes here
init_params = [0.1, 0.1, 0.2, 0.2] 
reps = 2

# Build a sample circuit to print
demo_circuit = create_qaoa_circuit(init_params, reps)

# Print it
print(demo_circuit.draw(output='text'))
print("\n(Circuit printed above. Now proceeding to optimization...)\n")


# ---------------------------------------------------------
# STEP 3: Define the Objective Function
# ---------------------------------------------------------
estimator = StatevectorEstimator()

def objective_function(params):
    # Create circuit
    reps = len(params) // 2
    qc = create_qaoa_circuit(params, reps)
    
    # Run Estimator
    pub = (qc, hamiltonian)
    job = estimator.run([pub])
    result = job.result()[0]
    energy = result.data.evs
    
    return float(energy)

# ---------------------------------------------------------
# STEP 4: Run Classical Optimization
# ---------------------------------------------------------
print("=== Step 3 & 4: Running Classical Optimization Loop ===")
print(f"Initial parameters: {init_params}")
print("Optimizing...")

result = minimize(
    objective_function, 
    init_params, 
    method='COBYLA', 
    options={'maxiter': 50, 'tol': 1e-4}
)

optimal_params = result.x
min_energy = result.fun

print("\n--- Optimization Complete ---")
print(f"Optimal Parameters: {optimal_params}")
print(f"Minimum Energy Found: {min_energy:.4f}")

# ---------------------------------------------------------
# STEP 5: Retrieve and Analyze the Optimal State
# ---------------------------------------------------------
print("\n=== Step 5: Sampling the Optimal Circuit ===")

# 1. Build the circuit with the OPTIMAL parameters
optimal_circuit = create_qaoa_circuit(optimal_params, reps)
optimal_circuit.measure_all()

# 2. Sample
sampler = StatevectorSampler()
job = sampler.run([optimal_circuit], shots=1024)
result_sampler = job.result()[0]
counts = result_sampler.data.meas.get_counts()

# 3. Find winner
sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
most_likely_string = sorted_counts[0][0]

print("\nTop 3 Measured Bitstrings (Candidate Solutions):")
for bitstring, count in sorted_counts[:3]:
    print(f"State |{bitstring}> : {count} shots")

print("\n------------------------------")
print(f"Winner: {most_likely_string}")
print("------------------------------")