#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Grover's Algorithm: an algorithm than can speed up 
#an unstructured search problem quadratically.
# ***This is a 3-bit implementation***.


# In[1]:


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


# In[4]:


#phase_oracle function marks states |000> and |111> as the results.
#Given a circuit and a set of registers it applies the appropriate gates.
def phase_oracle(circuit, qr):
    circuit.z(qr)
    circuit.cz(qr[1],qr[0])
    circuit.cz(qr[2],qr[0])
    circuit.cz(qr[2],qr[1])
    
#n_controlled_Z function takes a cirquit, 2 control bits and one target bit
#in order to apply the appropriate gates.
def n_controlled_Z(circuit, controls, target):
    """Implement a Z gate with two controls"""
    if (len(controls) == 2):
        circuit.h(target)
        circuit.ccx(controls[0], controls[1], target)
        circuit.h(target)
    else:
        raise ValueError('The controlled Z is implemented with just 2 controls')
        
# n should be always 2
def inversion_about_average(circuit, register, n):
    """Apply inversion about the average step of Grover's algorithm."""
    circuit.h(register)
    circuit.x(register)
    n_controlled_Z(circuit, [register[j] for j in range(n-1)], register[n-1])
    circuit.x(register)
    circuit.h(register)


# In[1]:


# set the hardware
qr = QuantumRegister(3)
cr = ClassicalRegister(3)

groverCircuit = QuantumCircuit(qr,cr)

#Create a uniform superposition at the start of the circuit as the algorithm indicates.
groverCircuit.h(qr)

phase_oracle(groverCircuit, qr)

#The only two special states we need to consider are the winner |w⟩ and the uniform superposition |s⟩. 
#These two vectors span a two-dimensional plane.
#inversion_about_average function creates a circuit of the inversion about the average for three qubits.
#It rotates the initial state |s⟩ closer towards the winner |w⟩. 
inversion_about_average(groverCircuit, qr, 3)

groverCircuit.measure(qr,cr)
groverCircuit.draw(output="mpl")


# In[ ]:


#In the case that there are multiple solutions, M, it can be shown that 
#roughly sqrt(N/M) rotations will suffice.
#since there are two solutions and eight possibilities, 
#we will only need to run one iteration. 


# In[6]:


#Expirement with simulators
backend = BasicAer.get_backend('qasm_simulator')
shots = 1024
results = execute(groverCircuit, backend=backend, shots=shots).result()
answer = results.get_counts()
plot_histogram(answer)


# In[7]:


#As we can see, the algorithm discovers our marked states.


# In[8]:


#Experiment with Real Devices
# Load our saved IBMQ accounts and get the least busy backend device
IBMQ.load_accounts()
IBMQ.backends()
backend_lb = least_busy(IBMQ.backends(simulator=False))
print("Least busy backend: ", backend_lb)


# In[9]:


# run our circuit on the least busy backend. Monitor the execution of the job in the queue
from qiskit.tools.monitor import job_monitor

backend = backend_lb
shots = 1024
job_exp = execute(groverCircuit, backend=backend, shots=shots)

job_monitor(job_exp, interval = 2)


# In[10]:


# get the results from the computation
results = job_exp.result()
answer = results.get_counts(groverCircuit)
plot_histogram(answer)


# In[ ]:




