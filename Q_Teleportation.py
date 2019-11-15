#!/usr/bin/env python
# coding: utf-8

# In[72]:


# This script performs quantum teleportation. 
#In short, the state of a qubit will be teleported and affect another qubit.
from qiskit import *
from qiskit.tools.visualization import plot_histogram


# In[73]:


#Create a circuit (quantum) with three qubits and three classic bits
circuit = QuantumCircuit(3, 3)


# In[74]:


#change the state of q0 from 0 to 1. Then, this state will be teleported to q3
circuit.x(0)
#adds the dot vertical line.
circuit.barrier()


# In[75]:


# create entaglement between q1 and q2
# add a Hadamard gate to q1
circuit.h(1)
# add a cnot gate from q1 to q2.
#cx performs the NOT operation on the q2 only when the q1 is |1> 
circuit.cx(1,2)


# In[76]:


circuit.cx(0,1)
circuit.h(0)


# In[77]:


# do measurments
# take measurements from q0 and q1 and put them in c0 and c1.
circuit.barrier()
circuit.measure([0,1],[0,1])


# In[78]:


circuit.barrier()
circuit.cx(1,2)
#performs Z operation on the q2 only when the q0 is |1>
# z=|1 0|
#   |0-1|
# It is used to make the appropriate transformation on the target qubit q2 
#to turn it into the desired state to be teleported
circuit.cz(0,2)


# In[79]:


circuit.draw(output='mpl')


# In[80]:


#verification

#take measurement from q2 and put it c2. q2 is in state |1>
circuit.measure(2,2)
#run a simulation with aer for 1024 shots.
simulator = Aer.get_backend('qasm_simulator')
result = execute(circuit, backend = simulator, shots = 1024).result()
counts = result.get_counts()
plot_histogram(counts)


# In[ ]:


# the numbers 100, 101 etc take places like c2c1c0. So, in c2 there is always 1. 

