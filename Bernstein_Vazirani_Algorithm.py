#!/usr/bin/env python
# coding: utf-8

# This is an implementation of Bernstein-Vazirani Algorithm
# In short, there is a secret binary number that we need to find.
# For N digits a classical computer needs N tries. A quantum computer needs just one!
# For more information visit https://www.youtube.com/watch?v=sqJIpHYl7oo

from qiskit import *
get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.tools.visualization import plot_histogram

# Prompt user to choose a binary number
secret_number = input('Give a binary number: ')

# Check if the chosen number is a binary one.
for i in range (0, len(secret_number)):
    if secret_number[i] != '0' and secret_number[i] != '1':
        # If user input is not a binary number pick up 1000101 to secure that everything will be fine
        secret_number = '1000101'

#create a circuit with number-of-digits-plus-one qubits and number-of-digits bits.
circuit = QuantumCircuit(len(secret_number)+1,len(secret_number))
#apply a Hadamard gate to every qubit except for the last one. 
circuit.h(range(len(secret_number)))


#apply a an X and a Hadamard gate to qubits
circuit.x(len(secret_number))
circuit.h(len(secret_number))
#set a vertical dot line.
circuit.barrier()


#apply CX gates to qubits when we meet one at secretnumber.
#enumerate returns an iterrable: position - bit
#0 0
#1 1
#2 1 
#3 0
#4 0
#5 0
# etc...

for i, yesno in enumerate(reversed(secret_number)):
    if yesno =='1':
        circuit.cx(i,len(secret_number))

circuit.barrier()
#apply a Hadamard gate to every qubit except for the last one. ...again
circuit.h(range(len(secret_number)))
circuit.measure(range(len(secret_number)),range(len(secret_number)))

circuit.draw(output='mpl')

#use Aer simulator
simulator = Aer.get_backend('qasm_simulator')
# execute and get results with one shot
result = execute(circuit, backend = simulator, shots = 1).result()
counts = result.get_counts()
print(counts)
