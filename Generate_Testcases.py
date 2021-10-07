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
                mul = soln[j] * int(term[: term.find('x')])     # calculating a_i * x_i
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
    # return variables, constraints, obj, cons


def homogeneity_test(cons):
    rows = len(cons)
    columns = len(cons[0])
    table = np.full((rows, columns//2 + 1), 0)

    # Other.print_table(cons)
    for row in range(rows):
        c = 0
        for col in range(columns):
            term = cons[row][col]
            if 'x' in term:
                table[row, c] = int(term[: term.find('x')])
                if col != 0 and cons[row][col - 1] == '-':
                    table[row, c] = table[row, c]*-1
                c += 1
        table[row, -1] = int(cons[row][-1])
    # print(table)

    lst = []
    i = 0
    for row in table:
        if row[i] == 0:
            return False
        table[i, :] = row / row[i]

        j = 0
        for row2 in table[:]:
            if all(row2 == table[i, :]):  # pivoting row
                j += 1
                continue
            m = row2[i] * -1
            table[j, :] = table[j, :] + m * table[i, :]
            j += 1

        lst.append(row[-1])
        i += 1
        # Other.print_table(table)
    for i in lst:
        if i < 0:
            return False
    return True


def special_problem():
    n = 30
    var = 2
    cons = n+2
    obj = "1,1,0"
    cons = []
    for i in range(0, n+2):
        eqn = [str(n-i+1)+'x', '+', str(i)+'y', '<=', str(n+1)]
        cons.append(eqn)
    Other.print_table(cons)
    return obj, cons
