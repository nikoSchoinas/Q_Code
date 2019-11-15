#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#This is an implementation of Bernstein-Vazirani Algorithm
#In short, there is a secret binary number that we need to find.
# For N digits a classical computer needs N tries. A quantum computer needs just one!


# In[82]:


from qiskit import *
get_ipython().run_line_magic('matplotlib', 'inline')
from qiskit.tools.visualization import plot_histogram


# In[117]:


secret_number = '100110'


# In[120]:


#create a circuit with 7 qubits (number of digits plus one) and 6 bits.
circuit = QuantumCircuit(len(secret_number)+1,len(secret_number))
#apply a Hadamard gate to qubits q0-q6 
circuit.h(range(len(secret_number)))

#apply a an X and a Hadamard gate to qubit q6 (last qubit)
#x gate inverts the states
circuit.x(len(secret_number))
circuit.h(len(secret_number))
#set a vertical dot line.
circuit.barrier()

#apply Hadamard gates to qubits when we meet one at secretnumber.
#enumerate returns an iterrable: position - bit
#0 0
#1 1
#2 1 
#3 0
#4 0
#5 0
for i, yesno in enumerate(reversed(secret_number)):
    if yesno =='1':
        circuit.cx(i,len(secret_number))


circuit.barrier()
#apply a Hadamard gate to qubits q0-q6...again
circuit.h(range(len(secret_number)))
circuit.measure(range(len(secret_number)),range(len(secret_number)))


# In[121]:


circuit.draw(output='mpl')


# In[122]:


#use Aer simulator
simulator = Aer.get_backend('qasm_simulator')
# execute and get results with one shot
result = execute(circuit, backend = simulator, shots = 1).result()
counts = result.get_counts()
print(counts)


# In[ ]:




