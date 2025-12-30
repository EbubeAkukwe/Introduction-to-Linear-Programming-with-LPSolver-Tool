import numpy as np
from scipy.optimize import linprog

def solve_lp(data):
    """
    Solves a linear programming problem using scipy.optimize.linprog.
    
    Args:
        data (dict): A dictionary containing the parsed LP problem.
                     Example: {
                         'objective_coefficients': [10, 8],
                         'constraint_matrix': [[2, 1], [1, 1]],
                         'constraint_rhs': [10, 6],
                         'optimization_type': 'maximize'
                     }
    
    Returns:
        dict: A dictionary with the solution or an error message.
    """
    c = np.array(data['objective_coefficients']) #ensures it's 1-D
    A_ub = np.array(data['constraint_matrix'], )
    b_ub = np.array(data['constraint_rhs'])
    print("c shape:", c.shape)
    print("A_ub shape:", A_ub.shape)
    print("b_ub shape:", b_ub.shape)
    
    # Handle maximization by negating the objective coefficients
    if data['optimization_type'] == 'maximize':
        c = c * -1

    # Simple logic for algorithm selection based on problem size
    num_variables = len(c)
    num_constraints = len(b_ub)
    if num_variables > 50 or num_constraints > 50:
        method = 'highs-ipm' # Best for large-scale problems
    else:
        method = 'highs' # A good all-purpose, modern solver

    # Define bounds (non-negativity for all variables by default)
    bounds = (0, None)
    
    # Call the solver
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method=method)
    
    # Process the results
    if result.success:
        optimal_value = result.fun
        if data['optimization_type'] == 'maximize':
            optimal_value = -optimal_value # Undo the negation
            
        return {
            "status": "success",
            "message": "Optimization successful.",
            "optimal_value": optimal_value,
            "solution": result.x.tolist() # Convert numpy array to a list
        }
    else:
        return {
            "status": "error",
            "message": f"Optimization failed: {result.message}"
        }