# Import necessary components
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error
from qiskit.visualization import plot_histogram

# --- Simulation Parameters ---
delay_time = 100 # Arbitrary time unit for the delay
t1_time = 1000  # T1 relaxation time in the same time unit
t2_time = 500   # T2 relaxation time in the same time unit
# --- Ideal Simulation (No Noise) ---
ideal_qc = QuantumCircuit(1, 1)
ideal_qc.h(0)
ideal_qc.delay(delay_time, 0, unit='ns') # Wait for some time
ideal_qc.h(0)
ideal_qc.measure(0, 0)

ideal_sim = AerSimulator()
ideal_result = ideal_sim.run(transpile(ideal_qc, ideal_sim), shots=1024).result()
ideal_counts = ideal_result.get_counts()
print(ideal_qc.draw())
print("Ideal Results:", ideal_counts)

# --- Noisy Simulation (With Decoherence) ---
# Create a noise model with T1=1000ns and T2=500ns.
decoherence_error = thermal_relaxation_error(t1_time, t2_time, delay_time)
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(decoherence_error, ['delay'])
noisy_sim = AerSimulator(noise_model=noise_model)
noisy_result = noisy_sim.run(transpile(ideal_qc, noisy_sim), shots=1024).result()
print(ideal_qc.draw())
print("Noisy Results:", noisy_result.get_counts())