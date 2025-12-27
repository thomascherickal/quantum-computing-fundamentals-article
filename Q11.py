import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from math import gcd
from fractions import Fraction

def c_amod15(a, power):
    """Controlled multiplication by a mod 15"""
    if a not in [2, 4, 7, 8, 11, 13]:
        raise ValueError("'a' must be coprime to 15")
    
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in [2, 13]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [7, 8]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    U = U.to_gate()
    U.name = f"{a}^{power} mod 15"
    c_U = U.control()
    return c_U

def qft_dagger(n):
    """Inverse Quantum Fourier Transform"""
    qc = QuantumCircuit(n)
    # Swap qubits
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    # Apply inverse QFT operations
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "QFT†"
    return qc

def shors_algorithm(N=15, a=7):
    """
    Shor's algorithm for factoring N
    
    Args:
        N: Number to factor (default: 15)
        a: Coprime base for modular exponentiation (default: 7)
    
    Returns:
        tuple: (quantum_circuit, measurement_counts, factors)
    """
    # Check if N is even
    if N % 2 == 0:
        return None, None, (2, N // 2)
    
    # Check if gcd(a, N) > 1
    g = gcd(a, N)
    if g > 1:
        return None, None, (g, N // g)
    
    # Number of counting qubits
    n_count = 8
    
    # Create quantum registers
    qr_count = QuantumRegister(n_count, 'counting')
    qr_aux = QuantumRegister(4, 'auxiliary')
    cr = ClassicalRegister(n_count, 'classical')
    qc = QuantumCircuit(qr_count, qr_aux, cr)
    
    # Initialize counting qubits in superposition
    for q in range(n_count):
        qc.h(q)
    
    # Initialize auxiliary register to |1⟩
    qc.x(n_count)
    qc.barrier()
    
    # Apply controlled-U operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i+n_count for i in range(4)])
    
    qc.barrier()
    
    # Apply inverse QFT
    qc.append(qft_dagger(n_count), range(n_count))
    qc.barrier()
    
    # Measure counting qubits
    qc.measure(range(n_count), range(n_count))
    
    # CRITICAL FIX: Transpile the circuit to decompose custom gates
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator, optimization_level=0)
    
    # Simulate the transpiled circuit
    result = simulator.run(transpiled_qc, shots=2048).result()
    counts = result.get_counts()
    
    # Process results to find factors
    factors = process_measurement_results(counts, N, a, n_count)
    
    qc.name = f"Shor's Algorithm for N={N}, a={a}"

    qc.draw(output='mpl')

    return qc, counts, factors

def process_measurement_results(counts, N, a, n_count):
    """Process measurement results to extract factors"""
    
    # Sort by most frequent measurements
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    for output, count in sorted_counts[:10]:  # Check top 10 results
        decimal = int(output, 2)
        
        # Skip if measurement is 0
        if decimal == 0:
            continue
        
        # Calculate phase
        phase = decimal / (2**n_count)
        
        # Use continued fractions to find the period r
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        
        # Check if r is valid
        if r > 0 and r % 2 == 0:
            # Calculate potential factors
            x = pow(a, r//2, N)
            
            guess1 = gcd(x - 1, N)
            guess2 = gcd(x + 1, N)
            
            # Check if we found non-trivial factors
            if guess1 not in [1, N]:
                return (guess1, N // guess1)
            if guess2 not in [1, N]:
                return (guess2, N // guess2)
    
    return None

# ==================== MAIN EXECUTION ====================

print("=" * 70)
print("SHOR'S ALGORITHM - QUANTUM FACTORIZATION")
print("=" * 70)

N = 15
a = 7

print(f"\nFactoring N = {N} using a = {a}")
print(f"Note: gcd({a}, {N}) = {gcd(a, N)}")
print("\nRunning quantum circuit (this may take a moment)...")

# Run Shor's algorithm
qc, counts, factors = shors_algorithm(N, a)

if factors:
    print(f"\n{'=' * 70}")
    print("FACTORS FOUND!")
    print(f"{'=' * 70}")
    print(f"{N} = {factors[0]} × {factors[1]}")
    print(f"Verification: {factors[0]} × {factors[1]} = {factors[0] * factors[1]}")
else:
    print("\nNo factors found in this run.")
    print("This can happen due to quantum measurement randomness.")
    print("Try running again or with a different value of 'a'.")

print(qc)
print(f"\n{'=' * 70}")
print("QUANTUM CIRCUIT STATISTICS")
print(f"{'=' * 70}")
print(f"Circuit depth: {qc.depth()}")
print(f"Number of qubits: {qc.num_qubits}")
print(f"Number of classical bits: {qc.num_clbits}")
print(f"Number of operations: {qc.size()}")

print(f"\n{'=' * 70}")
print("TOP MEASUREMENT RESULTS")
print(f"{'=' * 70}")
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
for i, (output, count) in enumerate(sorted_counts[:10], 1):
    decimal = int(output, 2)
    phase = decimal / 256
    frac = Fraction(phase).limit_denominator(N)
    print(f"{i:2d}. |{output}⟩ : {count:4d} times (decimal: {decimal:3d}, phase ≈ {frac})")

print(f"\n{'=' * 70}")