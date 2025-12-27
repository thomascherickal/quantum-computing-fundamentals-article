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
    U.name = f"{a}^{power}"  # Shortened name
    c_U = U.control()
    return c_U

def qft_dagger(n):
    """Inverse Quantum Fourier Transform"""
    qc = QuantumCircuit(n)
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi/float(2**(j-m)), m, j)
        qc.h(j)
    qc.name = "iQFT"  # Shortened name
    return qc

def shors_algorithm(N=15, a=7):
    """Shor's algorithm for factoring N"""
    
    # Check trivial cases
    if N % 2 == 0:
        return None, None, (2, N // 2)
    
    g = gcd(a, N)
    if g > 1:
        return None, None, (g, N // g)
    
    # Create compact circuit with shortened names
    n_count = 8
    qr_c = QuantumRegister(n_count, 'c')  # Shortened
    qr_a = QuantumRegister(4, 'a')        # Shortened
    cr = ClassicalRegister(n_count, 'm')  # Shortened
    qc = QuantumCircuit(qr_c, qr_a, cr)
    
    # Superposition
    for q in range(n_count):
        qc.h(q)
    
    # Initialize to |1⟩
    qc.x(n_count)
    qc.barrier()
    
    # Modular exponentiation
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q), [q] + [i+n_count for i in range(4)])
    
    qc.barrier()
    
    # Inverse QFT
    qc.append(qft_dagger(n_count), range(n_count))
    qc.barrier()
    
    # Measure
    qc.measure(range(n_count), range(n_count))
    
    # Transpile and simulate
    simulator = AerSimulator()
    transpiled_qc = transpile(qc, simulator, optimization_level=1)
    result = simulator.run(transpiled_qc, shots=2048).result()
    counts = result.get_counts()
    
    factors = process_measurement_results(counts, N, a, n_count)
    
    return qc, counts, factors

def process_measurement_results(counts, N, a, n_count):
    """Process measurement results to extract factors"""
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    for output, count in sorted_counts[:10]:
        decimal = int(output, 2)
        if decimal == 0:
            continue
        
        phase = decimal / (2**n_count)
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        
        if r > 0 and r % 2 == 0:
            x = pow(a, r//2, N)
            guess1 = gcd(x - 1, N)
            guess2 = gcd(x + 1, N)
            
            if guess1 not in [1, N]:
                return (guess1, N // guess1)
            if guess2 not in [1, N]:
                return (guess2, N // guess2)
    
    return None

def print_compact_circuit(qc, max_width=80):
    """Print circuit with line wrapping at max_width"""
    circuit_str = str(qc)
    lines = circuit_str.split('\n')
    
    print("=" * max_width)
    print("SHOR'S ALGORITHM QUANTUM CIRCUIT".center(max_width))
    print("=" * max_width)
    
    for line in lines:
        if len(line) <= max_width:
            print(line)
        else:
            # If line is too long, show truncated with ellipsis
            print(line[:max_width-3] + "...")
    
    print("=" * max_width)

def print_abstract_circuit(qc):
    """Print high-level abstract view of circuit"""
    print("=" * 80)
    print("ABSTRACT CIRCUIT STRUCTURE".center(80))
    print("=" * 80)
    print()
    print("Registers:")
    print(f"  - Counting qubits (c): {qc.num_qubits - 4} qubits")
    print(f"  - Auxiliary qubits (a): 4 qubits")
    print(f"  - Classical bits (m): {qc.num_clbits} bits")
    print()
    print("Circuit stages:")
    print("  1. Initialization:")
    print("     └─ Apply Hadamard to all counting qubits (superposition)")
    print("     └─ Set auxiliary register to |1⟩")
    print()
    print("  2. Modular Exponentiation:")
    print("     └─ Apply controlled-U operations: a^(2^k) mod 15")
    print("     └─ For k = 0, 1, 2, ..., 7")
    print()
    print("  3. Inverse QFT:")
    print("     └─ Extract period information from phase")
    print()
    print("  4. Measurement:")
    print("     └─ Measure counting qubits")
    print()
    print(f"Total operations: {qc.size()}")
    print(f"Circuit depth: {qc.depth()}")
    print("=" * 80)

# ==================== MAIN EXECUTION ====================

print("\n" + "=" * 80)
print("SHOR'S ALGORITHM - QUANTUM FACTORIZATION".center(80))
print("=" * 80)

N = 15
a = 7

print(f"\nTarget: Factor N = {N} using base a = {a}")
print("Running quantum period-finding circuit...\n")

# Run Shor's algorithm
qc, counts, factors = shors_algorithm(N, a)

# Print abstract view first
print_abstract_circuit(qc)

# Print compact circuit diagram
print("\n")
print_compact_circuit(qc, max_width=80)

# Results
print("\n" + "=" * 80)
print("RESULTS".center(80))
print("=" * 80)

if factors:
    print(f"\n✓ FACTORS FOUND!")
    print(f"  {N} = {factors[0]} × {factors[1]}")
    print(f"  Verification: {factors[0]} × {factors[1]} = {factors[0] * factors[1]}")
else:
    print("\n✗ No factors found in this run.")
    print("  (Try running again due to quantum randomness)")

print("\n" + "-" * 80)
print("Top 10 Measurement Outcomes:".center(80))
print("-" * 80)
sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
print(f"{'Rank':<6}{'Bitstring':<12}{'Count':<8}{'Decimal':<10}{'Phase'}")
print("-" * 80)
for i, (output, count) in enumerate(sorted_counts[:10], 1):
    decimal = int(output, 2)
    phase = Fraction(decimal, 256).limit_denominator(N)
    print(f"{i:<6}|{output}⟩{'':<3}{count:<8}{decimal:<10}{phase}")

print("=" * 80)
print("\nCircuit Summary:")
print(f"  - Total qubits: {qc.num_qubits}")
print(f"  - Circuit depth: {qc.depth()}")
print(f"  - Gate count: {qc.size()}")
print(f"  - Shots executed: 2048")
print("=" * 80)