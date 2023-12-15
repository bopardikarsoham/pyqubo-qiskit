import re
from qiskit.quantum_info import SparsePauliOp
from qiskit.opflow import I, Z

def pyqubo2nlocalising(qubo):
"""Converts an n-local pyqubo dictionary to the Qiskit Ising dictionary"""
    unique_variables = set()
    
    # Iterate through the keys and use regular expressions to capture variables
    for key_pair in qubo.keys():
        for key in key_pair:
            variables = re.findall(r'\w+\[\d+\]\[\d+\]', key)
            unique_variables.update(variables)
    
    # Convert the set of unique variables to a list
    unique_variables_list = list(unique_variables)
    
    #Sort them in the right order
    unique_variables_list.sort()

    # Create a dictionary to map variables to their new indexes
    variable_index_map = {var: index for index, var in enumerate(unique_variables_list)}
    
    # Replace variables with their new indexes and replace '*' with ','
    indexed_data = {}
    for key_pair, value in qubo.items():
        new_key_pair = tuple(variable_index_map.get(var, var) for key in key_pair for var in re.findall(r'\w+\[\d+\]\[\d+\]', key))
        indexed_data[new_key_pair] = value

    # Length of unique variables for the 'I' string
    unique_variables_length = len(unique_variables_list)

    # Converting the dictionary which is unordered to a 2d array
    array_2d = []
    for key, value in indexed_data.items():
        array_2d.append([key, value])

    # Making it PauliOp ready and indexing '(I-Z)/2' strings in the array
    output_list = []   
    for indices, value in array_2d:
        # Create a list of 'I's 
        pauli_string = ['I'] * unique_variables_length    
        # Replace 'I' with 'Z' at the specified indices
        for index in indices:
            pauli_string[index] = '((I-Z)/2)'    
        # Convert the list to a string
        pauli_string = '^'.join(pauli_string)    
        # Append the result as a tuple to the output list
        output_list.append((pauli_string, value))
    # Initialize the result
    #print(output_list)
    result = 0   
    # Iterate through the input list and calculate the result
    for item in output_list:
        expression = item[0]
        coefficient = item[1]
        evaluated_expression = eval(expression)
        result += coefficient * evaluated_expression
    return result
