import numpy as np
import math
from fractions import Fraction
import operator
import copy



"""
print_table(table) prints the table containing 
Fraction values in a more readable format
"""
def print_table(table):
    max_s = 0
    for row in table:
        for col in row:
            s = str(col)
            max_s = max(len(s), max_s)
    for row in table:
        for col in row:
            l = len(str(col))
            if l<max_s:
                print(" "*(max_s-l), end='')
                print(col, end='  ')
            else:
                print(col, end='  ')
        print()
    print()


"""
row_reduction(E, X, table) method does row reduction operations 
using the Gauss-Jordan Elimination method and returns the modified
table. It takes 3 arguments, entering variable column number as E,
exiting variable row number as X and a simplex table.
"""
def row_reduction(E, X, table):
    var = len(table[0, 1:-1]) - len(table[:-2, 0])  # calculating no. of variables
    i = 1
    for row in table[1:]:
        if all(row == table[X, :]):     # pivoting row
            i += 1
            continue
        m = row[E] * -1
        table[i, 1:] = table[i, 1:] + m * table[X, 1:]
        i += 1
    return table


"""
convert_to_unit_vec(table, var, cons) method takes 3 arguments, a simplex table,
number of variables as var, number of constraints as cons. It creates a table with 
cons+1 number of rows and var number of columns and fills it with unit vectors 
of the constraint vectors and objective function vector and returns the table.

If there are n constraints then 1st n rows contain unit vectors of constraints
and last row contains unit vector of objective function
"""
def convert_to_unit_vec(table, var, cons):
    newTab = np.full((cons + 1, var), Fraction(0))
    i = 0
    for row in table[:-1, 1:-(cons + 1)]:
        length = Fraction(math.sqrt(np.sum(np.square(row[:var]))))
        newTab[i] = row[:var] / length
        i += 1
    return newTab


"""
find_angles(newTab, var, cons) method takes 3 arguments, a table containing
unit vectors of constraint equations and the objective function, number of 
variables as var, number of constraints as cons. It finds the cosine values 
between the constraint vectors with the objective function vector and returns
a sorted list containing the top m equation numbers in descending order of 
their cosine values, where m = number of variables.
"""
def find_angles(newTab, var, cons):
    eqn = np.delete(newTab, 0, 0)
    obj = newTab[0]
    angles = np.append(np.sum(eqn * obj, axis=1), obj)
    cos = {}
    for j in range(len(angles)):
        cos[j + 1] = angles[j]  # key = eqn number, value = cosine value
    sorted_cos = sorted(cos.items(), key=operator.itemgetter(1),
                        reverse=True)  # cosine values sorted in descending order
    # print("Angles:", sorted_cos)
    set_of_equations = []
    for i in sorted_cos[:var]:
        set_of_equations.append(i[0])
    return set_of_equations
