def sparse_pauli_to_ising(sparse_pauli_op):
    linear = {}
    quadratic = {}
    offset = 0

    # Iterate through the terms in SparsePauliOp
    for term, coeff in zip(sparse_pauli_op.paulis, sparse_pauli_op.coeffs):
        term_str = term.to_label()
        z_positions = [i for i, pauli_char in enumerate(term_str) if pauli_char == 'Z']

        if len(z_positions) == 0:
            # Offset
            offset += coeff.real
        elif len(z_positions) == 1:
            # Linear terms
            var = f'x[{z_positions[0]}]'
            linear[var] = linear.get(var, 0) + coeff.real
        else:
            # Quadratic and higher-order terms
            # Combine all but the last Z operator into a single variable
            combined_var = '*'.join(f'x[{pos}]' for pos in z_positions[:-1])
            # Pair the combined variable with the last Z operator
            pair = (combined_var, f'x[{z_positions[-1]}]')
            quadratic[pair] = quadratic.get(pair, 0) + coeff.real

    return linear, quadratic, offset
