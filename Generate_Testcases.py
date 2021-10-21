import random
import numpy as np
import Other


def generate_objective_function(variables):
    obj = ""
    for i in range(variables):
        obj += str(random.randint(0, 100)) + ','
    obj += '0'
    # print(obj)
    return obj


def generate_lhs_of_constraints(variables, constraints):
    cons = []
    for i in range(constraints):  # creating constraints
        eqn = []
        for j in range(1, variables + 1):
            n = random.randint(-100, 100)
            if j > 1 and n < 0:
                eqn.append('-')
            elif j > 1 and n >= 0:
                eqn.append('+')
            eqn.append(str(abs(n)) + 'x' + str(j))
        cons.append(eqn)
    return cons


def assume_random_solution(variables):
    soln = []  # assuming a solution to calculate rhs
    for i in range(0, variables):
        soln.append(random.randint(1, 100))
    return soln


def generate_rhs_of_constraints(cons, soln):
    for equation in cons:
        rhs = 0
        j = 0
        for i in range(len(equation)):
            term = equation[i]
            if 'x' in term:
                mul = soln[j] * int(term[: term.find('x')])
                j += 1
            if i == 0:   rhs += mul
            elif equation[i-1] == '+':   rhs += mul
            elif equation[i-1] == '-':   rhs -= mul
        equation.append('<=')
        equation.append(str(rhs))
    return cons


def generate_random_testcase(variables, constraints):
    obj = generate_objective_function(variables)
    cons = generate_lhs_of_constraints(variables, constraints)
    soln = assume_random_solution(variables)     # assuming a solution to calculate rhs
    cons = generate_rhs_of_constraints(cons, soln)
    # Other.print_table(cons)
    # print(obj)
    # print(cons)
    return obj, cons


