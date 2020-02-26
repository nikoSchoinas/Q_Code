#!/usr/bin/env python
# coding: utf-8

# Grover's Algorithm: an algorithm than can speed up an unstructured search problem quadratically.
# It is based on a procedure called amplitude amplification.
# This procedure boosts the amplitude of the unknown item and decays all other item's amplitude.
# Documentation and examples can be found on https://qiskit.org/textbook/ch-algorithms/grover.html
# This is a 2-Qubit implementation that covers all the possible states.


#import the essentials
import matplotlib.pyplot
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.tools.visualization import plot_histogram




# User decides which choice will be the winner
user_choice = input("Which state will be the winner?\n a:00\n b:01\n c:10\n d:11\n")

# A quantum circuit for two qubits and a classical register with two bits.
qr = QuantumRegister(2)
cr = ClassicalRegister(2)

groverCircuit = QuantumCircuit(qr,cr)

# Initialize the state |s>
groverCircuit.h(qr)
groverCircuit.barrier()

# Apply the oracle for every possible winner
# We can say that we apply x gates (controled-z gates are between x gates) to qubits with value 0.
if user_choice == 'a': # case |00>
    groverCircuit.x(qr)
    groverCircuit.cz(qr[0],qr[1])
    groverCircuit.x(qr)
elif user_choice =='b': # case |01>
    groverCircuit.x(qr[1])
    groverCircuit.cz(qr[0],qr[1])
    groverCircuit.x(qr[1])
elif user_choice =='c': # case |10>
    groverCircuit.x(qr[0])
    groverCircuit.cz(qr[0],qr[1])
    groverCircuit.x(qr[0])
elif user_choice =='d': # case |11>
    groverCircuit.cz(qr[0],qr[1])
else:
    print("Ooops, something went wrong.\n I choose the winner to be |00>")
    groverCircuit.x(qr)
    groverCircuit.cz(qr[0],qr[1])
    groverCircuit.x(qr)
    
groverCircuit.barrier()

# Apply a Hadamard operation to both qubits.
groverCircuit.h(qr)
groverCircuit.barrier()

# Apply the reflection Us = 2\s><s| - I
# It can be applied to every case.
groverCircuit.z(qr)
groverCircuit.cz(qr[0],qr[1])
groverCircuit.barrier()

# Apply a Hadamard operation to both qubits.
groverCircuit.h(qr)

# Actual measurement
groverCircuit.measure(qr,cr)

# Draw the circuit.
groverCircuit.draw(output="mpl")





# Run the circuit with a classical computer
backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(groverCircuit, backend=backend, shots=shots).result()
answer = results.get_counts()
plot_histogram(answer)

# Load IBM Q account and get the least busy backend device
provider = IBMQ.load_account()
device = least_busy(provider.backends(simulator=False))
print("Running on current least busy device: ", device)





# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor
job = execute(groverCircuit, backend=device, shots=1024, max_credits=10)
job_monitor(job, interval = 2)


# Get the results from the computation
results = job.result()
answer = results.get_counts(groverCircuit)
plot_histogram(answer)




