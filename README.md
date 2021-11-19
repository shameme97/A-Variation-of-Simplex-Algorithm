# A-Variation-of-Simplex-Algorithm

# Generating random test cases

To run this algorithm with random test cases, do the following steps:
1. Fix the number of variables and number of contraints to your preferrance in the main.py file in line 249-250.
2. Fix the range of random numbers for your coefficients in the Generate_Testcases.py file.  
	2.i) Fix the range of random numbers for objective function coefficient in the generate_objective_function() in line 9.  
	2.ii) Fix the range of random numbers for the coefficients of constraints in the function generate_lhs_of_constraints() in line 20.  
	      Note: If for all test cases you get "The system has no solutions or has many solutions." then set the lower range such that |lower range|<|upper range|. Slowly decrease the lower range till you get some test cases which show "Found Infeasibility".  

# Input from file

To run your own test case, do the following steps:
1. Uncomment the portion under the comment "Input from file" (line 306-321).
2. Set the directory of your input .txt file in the Input.py file, in the function take_input_from_file(), line 103.
3. Type your desired test case in the .txt file in the following manner:-

	Objective function: max 4x + 6y  
	Constraints:  
	0.5x + 1y <= 600  
	12.5x + 10y <= 10000  
	1x + 0y <= 700   


NOTE: This version of program is buggy for '>=' and '=' constraints and can only solve for maximizing linear programming problems.
