import numpy as np
from fractions import Fraction



"""
gen_matrix(var, cons) method takes 2 arguments, number of variables as var,
number of constraints as cons, and returns a table with cons+2 number of rows 
and var+cons+2 number of columns, set with default value 0 as a Fraction
"""
def gen_matrix(var, cons):
    tab = np.full((cons + 2, var + cons + 2), Fraction(0))
    return tab


"""
convert(eq) method takes a string argument as eq, representing an equation.
Let 2x+3y<=5 is an equation; then eq would contain string '2,3,L,5'. It 
converts this string to a list of Fraction values and returns it.
"""
def convert(eq):
    eq = eq.split(',')
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [Fraction(i) for i in eq]
    elif 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [Fraction(i) * -1 for i in eq]
    return eq


"""
add_cons(table) method takes a table as an argument and 
checks if it has an empty row for adding a constraint
"""
def add_cons(table):
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            # print(j)
            total += int(j) ** 2
        if total == 0:
            empty.append(total)
    if len(empty) > 1:
        return True
    else:
        return False

"""
constraint(table, eq) method takes a table and a string eq,
representing an equation, as arguments. It finds the first 
empty row from top and adds the equation to the table. If it 
doesn't find an empty row, then it prints an error message. 
"""
def constraint(table, eq):
    if add_cons(table):
        lc = len(table[0, :])
        lr = len(table[:, 0])
        var = lc - lr + 1
        j = 1
        while j < lr:
            row_check = table[j, :]
            total = 0
            for i in row_check:
                total += float(int(i) ** 2)
            if total == 0:
                row = row_check
                break
            j += 1
        eq = convert(eq)
        i = 0
        while i < len(eq) - 1:
            row[i + 1] = eq[i]
            i += 1
        row[-1] = eq[-1]
        row[var + j - 1] = Fraction(1) # change: added -1 to var+j
    else:
        print('Cannot add another constraint.')


"""
add_obj(table) method takes a table as an argument and checks 
if all constraints have been added. It returns True only if 
the last two rows are empty, otherwise returns False 
"""
def add_obj(table):  # checks if all constraints have been added
    lr = len(table[:, 0])
    empty = []
    for i in range(lr):
        total = 0
        for j in table[i, :]:
            total += int(j) ** 2
        if total == 0:
            empty.append(total)
    if len(empty) <= 2:
        return True
    else:
        return False

"""
obj(table, eq) method takes a table and a string eq, representing the 
objective function, as arguments. If all constraints have been added, 
it fills the last two rows of the table with objective function and 
initial reduced cost respectively. Otherwise it prints an error message.
"""
def obj(table, eq):
    if add_obj(table):
        eq = [Fraction(i) for i in eq.split(',')]
        lr = len(table[:, 0])
        # row = table[lr - 2, :]
        row = table[0, :]
        row2 = table[lr - 1, :]
        i = 0
        while i < len(eq) - 1:
            row[i + 1] = eq[i]
            row2[i + 1] = eq[i] * -1
            i += 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')
