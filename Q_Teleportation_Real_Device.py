#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For more information about how this algorithm works see Q_teleportation.py 


# In[86]:


#import the essentials
import matplotlib.pyplot
import numpy as np

# importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# import basic plot tools
from qiskit.tools.visualization import plot_histogram


# In[99]:


# Create a quantum circuit with three qubits and three classic bits.
# The mission is to transfer the state of qubit_0 to qubit_2
qr = QuantumRegister(3)
cr = ClassicalRegister(3)

circuit = QuantumCircuit(qr, cr)


# In[100]:


# User will choose what state (|0> or |1>) will be teleported.
user_choice = input("Which state do you want to teleport?\n a: |0>\n b: |1>\n")


if user_choice == 'b':
    # If user chooses |1> change the state of q0 from 0 to 1.
    circuit.x(qr[0])
    
# If user chooses |0> state, do nothing. 

# add a vertical line.
circuit.barrier()


# In[101]:


# create entaglement between q1 and q2
circuit.h(qr[1])
circuit.cx(qr[1],qr[2])

# Add the suitable gates as the teleportation protocol indicates.
circuit.cx(qr[0],qr[1])
circuit.h(qr[0])
circuit.barrier() #barrier is optional
circuit.cx(qr[1],qr[2])
circuit.cz(qr[0],qr[2])


# In[102]:


# Actual measurement
circuit.measure(qr,cr)


# In[103]:


# Draw the circuit
circuit.draw(output='mpl')


# In[104]:


# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
provider = IBMQ.load_account()
device = least_busy(provider.backends(simulator=False))

# armonk device has just one qubit so it will not run the job and it will produce an error.
# visit https://quantum-computing.ibm.com/ and from the left panel pick the least busy provider
# In this case I chose ibmq_london
if device.name() == 'ibmq_armonk':
    device = provider.get_backend('ibmq_london')

print("Running on current least busy device: ", device)

# Run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor
job = execute(circuit, backend=device, shots=1024)
job_monitor(job)

# Get the results from the computation
results = job.result()
answer = results.get_counts(circuit)
plot_histogram(answer)


# In[85]:


# the numbers 100, 101 etc take places like c2c1c0. So, if c2 is 1 (or 0) then the initial state was 1 (or 0) 


# In[ ]:




