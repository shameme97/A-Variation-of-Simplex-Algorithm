import Generate_matrix


"""
forming_eqn(line) method takes a string line as argument and 
finds the equation from the line and splits it to a list. For 
example, 2x + 3y <= 10 would be returned as ['2x','+','3y','<=',10].
"""
def forming_eqn(line):
    pos = 0
    for i in line:   # finding start of equation
        if i.isdigit():
            pos = line.index(i)
            break
    if line[pos-1] == '-': pos -= 1
    equation = line[pos:].split()
    return equation


"""
convert_lhs_eq_to_string(equation) method takes an equation list as 
argument and converts its left hand side into a string. For example, 
['2x','-','3y','<=',10] would be converted as '2,-3,0' and returned.
"""
def convert_lhs_eq_to_string(equation):
    str = ''
    symb = '<=>'
    flag = True
    for term in equation:
        for char in term:
            if char in symb:
                str += '0'
                # print(str)
                return str
            if char == '-' or char == '+' or char == '.':
                str += char
                flag = True
            if char.isdigit() and flag:
                str += char
            if char.isalpha():
                str += ','
                flag = False
    str += '0'
    return str


"""
adding_rhs_of_eqn_string(constraint, constraint_lhs, equal='False') method takes 
3 arguments, a constraint in list, left hand side of constraint in string and an 
optional argument, equal in boolean. It converts the right hand side of constraint 
to string and adds it to the left hand side and returns it. Ex: ['2x','-','3y','<=',10],
'2,-3,0', False would return string '2,-3,L,10'. Boolean equal is used to handle 
constraints like 2x+3y=10.
"""
def adding_rhs_of_eqn_string(constraint, constraint_lhs, equal='False'):
    cons = constraint_lhs[:-1]
    if constraint[-2] == '>=' :
        cons += 'G,'
    elif constraint[-2] == '<=' :
        cons += 'L,'
    cons += constraint[-1]
    return cons


def convert_equal_constraints_into_2_equations(equation, constraints):
    eq1 = equation.copy()
    eq2 = equation.copy()
    eq1[-2] = '<='
    eq2[-2] = '>='
    constraints.append(eq1)
    constraints.append(eq2)

"""
insert_data_into_matrix(constraints, matrix) method takes a list of constraints 
and inserts them into the table known as matrix. Constraints like 2x+3y=10 
would be added as '2,3,L,10' and '2,3,G,10' in the table.
"""
def insert_data_into_matrix(obj, constraints, matrix):
    for constraint in constraints:
        constraint_lhs = convert_lhs_eq_to_string(constraint)
        constraint_as_string = adding_rhs_of_eqn_string(constraint, constraint_lhs)
        Generate_matrix.constraint(matrix, constraint_as_string)
    Generate_matrix.obj(matrix, obj)


def forming_constraint_table(file):
    num_of_variables = 0
    num_of_constraints = 0
    constraints = []
    for line in file.readlines()[1:]:
        eq = forming_eqn(line)
        num_of_variables = max(num_of_variables, len(eq) // 2)
        num_of_constraints += 1
        if eq[-2] == '=':  # As 2x+3y=10 would be broken down to 2x+3y<=10 & 2x+3y>=10
            num_of_constraints += 1
            convert_equal_constraints_into_2_equations(eq, constraints)
        else:
            constraints.append(eq)
    return num_of_variables, num_of_constraints, constraints


def take_input_from_file():
    file = open('input.txt', 'r')
    objective_function = file.readline()

    obj = convert_lhs_eq_to_string(forming_eqn(objective_function))
    num_of_variables, num_of_constraints, constraints = forming_constraint_table(file)

    return num_of_variables, num_of_constraints, obj, constraints


# uncomment when taking input from local file

# number_of_variables, number_of_constraints, obj, constraints = take_input_from_file()
# matrix = Generate_matrix.gen_matrix(number_of_variables, number_of_constraints)
# insert_data_into_matrix(obj, constraints, matrix)


# print(obj)
# Other.print_table(constraints)
# Other.print_table(matrix)
