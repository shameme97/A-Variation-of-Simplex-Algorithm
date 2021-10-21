import copy
import math
import sys

import numpy as np

import Generate_matrix
import Other
import Input
import Generate_Testcases


class My_Simplex:

    test_no = 1
    iterations = 0
    feasibility_itr = 0
    infeasibility_flag = False

    def ensure_feasibility_method_2(self, table):
        while any(table[:-1, -1] < 0):   # checking if solution column has negative value
            minimum_ratio = math.inf
            negative_rhs_rows = np.where(table[:-1, -1] < 0)[0]  # returns all rows having -ve r.h.s
            for row in negative_rhs_rows:
                b = min(table[row, 1:-1])
                if b < 0:   # if true then b is most negative
                    ratio = table[row, -1] / b  # positive ratio
                    if ratio < minimum_ratio:
                        minimum_ratio = ratio  # minimum positive ratio
                        exitVar = row
                        enterVar = np.where(table[row, 1:-1] == b)[0][0] + 1

            non_negative_rhs_rows = np.where(table[:-1, -1] >= 0)[0]  # returns all rows having +ve & 0 r.h.s
            for row in non_negative_rhs_rows:
                a = min(table[row, 1:-1])
                if a > 0:  # if true then a is +ve
                    ratio = table[row, -1] / a  # positive ratio
                    if ratio < minimum_ratio:
                        minimum_ratio = ratio  # minimum positive ratio
                        exitVar = row
                        enterVar = np.where(table[row, 1:-1] == a)[0][0] + 1

            if minimum_ratio == math.inf:
                sys.exit("Infeasible Solution")

            table = self.pivoting(enterVar, exitVar, table)
            My_Simplex.iterations += 1
            My_Simplex.feasibility_itr += 1
            # print(My_Simplex.iterations )
            # Other.print_table(table)
        table = self.maxz(table)
        return table


    """
    checks if slack variable in basis is negative in final table.
    If yes, then solution is infeasible as it breaks the constraint 
    of slack variables being >= 0.
    """
    def check_infeasibility(self, table):
        infeasible = False
        for row in table[1:-1]:
            if row[0] == 0 and row[-1] < 0:
                infeasible = True
                break
        if infeasible:
            print("Found infeasibility")
            My_Simplex.infeasibility_flag = True
            table = self.ensure_feasibility_method_2(table)
        return table


    """
    check_last_row(table) method takes a simplex table as
    an argument and returns True if the minimum value of
    the last row is negative, otherwise returns False
    """
    def check_last_row(self, table):
        m = min(table[-1, 1:-1])
        if m < 0:
            return True
        else:
            return False

    """
    find_entering_variable(table) method takes a simplex table as 
    an argument and returns the entering variable, which corresponds
    to the column containing the minimum value in the last row.
    Note: Takes 1st occurrence if two equal minimum values
    """
    def find_entering_variable(self, table):
        m = min(table[-1, 1:-1])
        enterVariable = np.where(table[-1, 1:-1] == m)[0][0] + 1
        return enterVariable

    """
    find_exiting_variable(table, enterVar) method takes a simplex table and 
    the entering variable, enterVar, as arguments and returns the exiting 
    variable from basis which corresponds to the row with the 
    minimum ratio of solution column and entering variable column. 
    It ignores undefined and negative ratios.
    """
    def find_exiting_variable(self, table, enterVar):
        m = math.inf
        i = 0
        exitVariable = -1
        for row in table[1:-1]:
            i += 1
            if row[enterVar] == 0: # ignores undefined ratio
                continue
            ratio = row[-1] / row[enterVar]
            if ratio < 0 or (row[-1] == 0 and row[enterVar] < 0):  # ignores negative ratio
                continue
            if row[-1] < 0 and row[enterVar] < 0:  # ignores -ve -ve
                continue
            if ratio < m:
                m = ratio
                exitVariable = i
        if exitVariable == -1:
            print("The system has no solutions or has many solutions.")
            # sys.exit("The system has no solutions or has many solutions.")
            return "no solution"
        return exitVariable

    """
    change_basic_variables(enterVar, exitVar, table) replaces exiting variable 
    from basis with entering variable. It takes 3 arguments, entering variable 
    as enterVar, exiting variable as exitVar and a simplex table. It updates Cb 
    by replacing the coefficient of exiting variable with the coefficient of 
    entering variable. It divides the row of the exiting variable of basis by the 
    pivot element and returns the modified simplex table.

    """
    def change_basic_variables(self, enterVar, exitVar, table):
        pivot_elem = table[exitVar, enterVar]
        table[exitVar, 0] = table[0, enterVar]
        table[exitVar, 1:] = table[exitVar, 1:] / pivot_elem
        return table

    """
    pivoting(E, X, table) method pivots the simplex table through pivot element.
    It takes 3 arguments, entering variable as E, exiting variable as X and the
    simplex table. It returns the modified simplex table after changing basic 
    variable, doing necessary row reductions and calculating reduced cost.
    """
    def pivoting(self, enterVar, exitVar, table):
        table = self.change_basic_variables(enterVar, exitVar, table)
        table = Other.row_reduction(enterVar, exitVar, table)
        # Other.print_table(table)
        return table

    """
    maxz(table) method finds the maximum solution from the given simplex table
    by running the simplex algorithm till the last row has no negative values. 
    """
    def maxz(self, table):
        # print("Executing usual maximizing method...")
        while self.check_last_row(table):
            enterVar = self.find_entering_variable(table)
            exitVar = self.find_exiting_variable(table, enterVar)
            if exitVar == "no solution":
                return '0'
            table = self.pivoting(enterVar, exitVar, table)
            My_Simplex.iterations += 1
        table = self.check_infeasibility(table)
        return table

    """
    initial_basic_variables(top, var, cons) method takes 3 arguments, no. of
    variables as var, no. of constraints as cons and a list, top, which contains 
    the top m no. of equation numbers which make the least angles with the 
    objective function, m=no. of variables. From this info, this method finds 
    the initial basic variables and sends their corresponding number as a list. 
    
    Ex - for var=2, cons=3, top=[2,3,5] means equations 2,3,5 make minimum 
    angles with objective function. Here var=2 indicates 2 decision variables, x1,x2; 
    cons=3 indicates 3 constraints, i.e 3 slack variables, y1,y2,y3. 
    Hence we get y2=0, y3=0. So our basic variables will be x1,x2 and y1.
    """
    def initial_basic_variables(self, top, var, cons):
        basic = []
        for i in range(1, var + cons + 1):
            if i not in top:
                if i <= cons:
                    basic.append(i + var)
                else:
                    basic.append(i - cons)
        basic.sort()
        non_basic = []
        for i in range(1, var + cons + 1):
            if i not in basic:
                non_basic.append(i)
        return basic, non_basic

    """
    preprocessing(variables, constraints, table) method selects the initial basic variables
    by finding the angles between the constraint vectors and objective function vector and
    considering m vectors which make minimum angle with the objective function. It takes 3 
    arguments, number of variables as variables, number of constraints as constraints and
    the simplex table.
    """
    def preprocessing(self, variables, constraints, table):
        unitVectors = Other.convert_to_unit_vec(table, variables, constraints)
        topValues = Other.find_angles(unitVectors, variables, constraints)
        basicVariables, non_basicVariables = self.initial_basic_variables(topValues, variables, constraints)
        return basicVariables, non_basicVariables

    def fill_table_initially(self, basic, nonbasic, table):
        row = 1
        n = 0
        for i in basic:
            enterVar = i
            exitVar = row
            row += 1
            # replacing with a non-basic variable if pivot=0
            while table[exitVar, enterVar] == 0:   # coefficient of basic variable in eqn == 0
                enterVar = nonbasic[n]
                n += 1
                print(f"x{i} replaced with nonbasic x{enterVar}")
                My_Simplex.output2 += "\nx"+str(i)+" replaced with nonbasic x"+str(enterVar)

            table = self.change_basic_variables(enterVar, exitVar, table)
            table = Other.row_reduction(enterVar, exitVar, table)



    """
    create_initial_table(var, cons, table) method returns a simplex table with basic 
    variables from an infeasible region through some processing. It takes 3 arguments, 
    number of variables as var, number of constraints as cons and a simplex table.
    """
    def create_initial_table(self, var, cons, table):
        bv, non_bv = self.preprocessing(var, cons, table)
        self.fill_table_initially(bv, non_bv, table)
        table = self.ensure_feasibility_method_2(table)
        return table


a = My_Simplex()
test_no = 1
while test_no <= 100:
    print("Running test no.:", test_no)
    output = str(test_no) + '      '
    My_Simplex.output2 = "Test no.: " + str(test_no) + "\n"
    test_no += 1
    non_homogeneous = False
    My_Simplex.infeasibility_flag = False

    number_of_variables = 20
    number_of_constraints = 10
    obj, constraints = Generate_Testcases.generate_random_testcase(number_of_variables, number_of_constraints)

    input_table = Generate_matrix.gen_matrix(number_of_variables, number_of_constraints)
    Input.insert_data_into_matrix(obj, constraints, input_table)
    # print("Objective function:", obj)
    # Other.print_table(input_table)
    for method in range(1, 3):
        My_Simplex.iterations = 0
        My_Simplex.feasibility_itr = 0

        if method == 1:
            print("\nThe usual way:")
            table = a.maxz(copy.copy(input_table))
            if len(table) == 1:
                non_homogeneous = True
                break
            result1 = float(table[-1, -1])
            # Other.print_table("Final usual table:", table)
            itr_no_1 = My_Simplex.iterations

        else:
            print("\nThe new way:")
            My_Simplex.output2 += "\nThe new way:\n"
            table2 = a.create_initial_table(number_of_variables, number_of_constraints, copy.copy(input_table))
            # table2 = a.maxz(table2)
            result2 = float(table2[-1, -1])
            itr_no_2 = My_Simplex.iterations

        # print("Feasibility iterations:", My_Simplex.feasibility_itr)
        print("Number of iterations:", My_Simplex.iterations)
        print("Optimal solution =", float(table[-1, -1]))
        output += str(My_Simplex.iterations) + '      '

    if non_homogeneous:
        test_no -= 1
        continue
    output += str(result1 == result2) + '      '
    if itr_no_1 < itr_no_2: output += "usual" + '                '
    elif itr_no_1 == itr_no_2: output += "BOTH EQUAL" + '           '
    else: output += "improvised method" + '    '

    if My_Simplex.infeasibility_flag:
        output += "Infeasibility found\n"
    else:
        output += "\n"

    s = str(number_of_variables) + " variables " + str(number_of_constraints) + " constraints testcases.txt"
    output_file = open(s, 'a+')
    output_file.writelines(output)

    print("---------------------------------------------------------------------------")


# Input from file

# My_Simplex.iterations = 0
# My_Simplex.basic_variable = np.full(Input.number_of_constraints+1, 0)
# print("\nThe usual way:")
# # table2 = a.check_infeasibility()
# table2 = a.maxz(copy.copy(Input.matrix))
# print("Number of iterations:", My_Simplex.iterations)
# print("Optimal solution =", float(table2[-1, -1]))
#
# My_Simplex.iterations = 0
# My_Simplex.basic_variable = np.full(Input.number_of_constraints+1, 0)
# print("\nThe new way:")
# matrix = a.create_initial_table(Input.number_of_variables, Input.number_of_constraints, copy.copy(Input.matrix))
# # Other.print_table(matrix)
# table = a.maxz(matrix)
# print("Number of iterations:", My_Simplex.iterations)
# print("Optimal solution =", float(table[-1, -1]))
