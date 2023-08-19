import cirq
import matplotlib.pyplot as plt

# Define the number of qubits
num_qubits = 6  # Change the number of qubits here

# Create qubits
qubits = [cirq.LineQubit(i) for i in range(num_qubits)]

# Create a quantum circuit
circuit = cirq.Circuit()

# Add quantum gates to the circuit
circuit.append(cirq.H(q) for q in qubits)  # Apply Hadamard gate to all qubits
circuit.append(cirq.CNOT(qubits[0], qubits[1]))  # Apply CNOT gate

# Add measurement operations to the circuit
for qubit in qubits:
    circuit.append(cirq.measure(qubit, key=str(qubit)))

# Create a simulator
simulator = cirq.Simulator()

# Simulate the circuit and collect measurement results
repetitions = 1000  # Number of times to repeat the measurement
results = simulator.run(circuit, repetitions=repetitions)

# Analyze and interpret results
# Initialize a dictionary to count measurement outcomes
counts = {}
for qubit in qubits:
    qubit_key = str(qubit)
    counts[qubit_key] = {'0': 0, '1': 0}  # Initialize counts for each qubit outcome

# Count measurement outcomes
for qubit_key in counts.keys():
    measurements = results.measurements[qubit_key]
    for outcome in measurements:
        outcome_str = ''.join(str(bit) for bit in outcome)
        counts[qubit_key][outcome_str] += 1

# Calculate probabilities
probabilities = {}
for qubit_key, outcomes in counts.items():
    total_counts = repetitions
    probabilities[qubit_key] = {
        outcome: count / total_counts for outcome, count in outcomes.items()
    }

# Print measurement probabilities
print("Measurement Probabilities:")
for qubit_key, outcomes in probabilities.items():
    print(f"{qubit_key}: {outcomes}")

# Create a single subplot with bar charts for each qubit
fig, axes = plt.subplots(1, num_qubits, figsize=(15, 5))
fig.suptitle("Measurement Probabilities for Each Qubit")

for i, (qubit_key, outcomes) in enumerate(probabilities.items()):
    ax = axes[i]
    ax.bar(outcomes.keys(), outcomes.values())
    ax.set_title(f"{qubit_key}")
    ax.set_xlabel("Measurement Outcome")
    ax.set_ylabel("Probability")

plt.tight_layout()
plt.show()
