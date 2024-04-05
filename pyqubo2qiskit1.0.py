from qiskit.quantum_info import SparsePauliOp, Pauli

def pyqubo2nlocalising(qubo):
    import re

    unique_variables = set()
    
    # Iterate through the keys and use regular expressions to capture variables
    for key_pair in qubo.keys():
        for key in key_pair:
            variables = re.findall(r'\w+\[\d+\]\[\d+\]', key)
            unique_variables.update(variables)
    
    unique_variables_list = sorted(list(unique_variables))
    variable_index_map = {var: index for index, var in enumerate(unique_variables_list)}

    result = SparsePauliOp.from_list([("I" * len(unique_variables_list), 0)])
    
    for key_pair, value in qubo.items():
        term_ops = SparsePauliOp.from_list([("I" * len(unique_variables_list), value)])

        # Combine both sides of the term and extract unique variables
        combined_key = "*".join(key_pair)
        unique_vars_in_term = set(re.findall(r'\w+\[\d+\]\[\d+\]', combined_key))

        for var in unique_vars_in_term:
            if var in variable_index_map:
                index = variable_index_map[var]
                i_op = SparsePauliOp.from_list([("I" * len(unique_variables_list), 0.5)])
                z_op = SparsePauliOp.from_list([("I" * index + "Z" + "I" * (len(unique_variables_list) - index - 1), -0.5)])
                term_ops = term_ops.compose(i_op + z_op)
        
        result += term_ops

        if result.coeffs[0] == 0:
            result = SparsePauliOp(result.paulis[1:], coeffs=result.coeffs[1:])

    return result

op = pyqubo2nlocalising(qubo)
print(op)
