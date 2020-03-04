#!/usr/bin/env python
# coding: utf-8

# This script performs quantum teleportation.
# IMPORTANT: We do not transport the actual qubit but the information about its state.
# More information can be found here: https://www.youtube.com/watch?v=mMwovHK2NrE


#Alice and Bob want to communicate via quantum teleportation. Initially, they meet each other
#and they set their qubits to entangled state (q1,q2) . After that, both of them take a qubit (note that
#Alice uses two qubits - q0,q1)

#Alice does not know the probability aplitude but since her qubit is entangled with Bob's, she can
#teleport its unknown state. So, Alice proceeds to a quantum computation at her qubits (q0, q1)
#in order to transfer the unknown probability aplitude to Bob's qubit.

#Bob should use a quantum circuit so as that he can set his qubit in the same state as Alice's
#qubit (CX and CZ gates after the last barrier).

#During quantum teleportation it is not teleported the physical system that implements a qubit but
#its quantum state. For example, if Alice and Bob use the spin of an electron as a qubit, the
#"thing" that is teleported it is not the actual electron. The electron remains at Alice's place as the
#information about its state is what can be teleported.

#Quantum teleportation does not violates no-cloning theorem. Afte teleportation Alice's quantum
#state does not exist. Namely, Alice cannot have a copy of the state that she teleported to Bob.
#Since, Alice measures the state of her qubits, Bob's qubit is set to a specific state.


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


# Create a quantum circuit with three qubits and three classic bits.
# The mission is to transfer the state of qubit_0 to qubit_2 through qubit_1
qr = QuantumRegister(3)
cr = ClassicalRegister(3)

circuit = QuantumCircuit(qr, cr)


# User will choose what state (|0> or |1>) will be teleported.
user_choice = input("Which state do you want to teleport?\n a: |0>\n b: |1>\n")


if user_choice == 'b':
    # If user chooses |1> change the state of q0 from 0 to 1. Then, this state will be teleported to q2
    circuit.x(qr[0])
    
# If user chooses |0> state, do nothing. 

# add a vertical line.
circuit.barrier()


# create entaglement between q1 and q2
circuit.h(qr[1])
circuit.cx(qr[1],qr[2])


# Add two more gates as the teleportation protocol indicates.
circuit.cx(qr[0],qr[1])
circuit.h(qr[0])


# measurements
circuit.barrier()
circuit.measure(qr[0],cr[0])
circuit.measure(qr[1],cr[1])


circuit.barrier()
# Add gates as teleportation protocol indicates
circuit.cx(qr[1],qr[2])
circuit.cz(qr[0],qr[2])


# Draw the circuit
circuit.draw(output='mpl')


# Measure q2's state and put it to c2.
circuit.measure(qr[2],cr[2])

#run a simulation with aer for 1024 shots.
simulator = BasicAer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots = 1024).result()
counts = result.get_counts()
plot_histogram(counts)


# the numbers 100, 101 etc take places like c2c1c0. So, if c2 is 1 (or 0) then the initial state was 1 (or 0) 
# For some reason this circuit can be run only in qasm simulator and not in a real quantum device.

