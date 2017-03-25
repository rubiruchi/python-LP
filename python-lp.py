#BEGIN CODE

from random import randint, seed
from numpy import matrix
from itertools import combinations
from numpy import linalg

obj_func = []
mat_a = []
mat_at = []
mat_b = []
mat_x = []
lp_num_const = 5 #constraints to the LP
lp_num_vars = 20 #variables to the objective function
mat_sing = 0
soln_inf = 0
soln_feas = 0

seed(1031)

"""###########################################################
SUB-ROUTINES
##########################################################"""

def checkSoln(matrix):
    #Checks for feasibility of the solution
    x = sum(n < 0 for n in matrix)
    if x > 0: #negative numbers exist, infeasible solution
        return 1
    else:
        return 0

def generateLP(numvars, numconst):
    global mat_a, mat_b, mat_x, obj_func
    obj_func = matGenRanInt(-5, 5, numvars, 1)
    mat_a = matGenRanInt(0, 3, numconst, numvars)
    mat_b = matGenRanInt(4, 9, numconst, 1)
    mat_x = matGenRanInt(0, 0, numvars, 1) #zeros used for place holding data

def matGenRanInt(lower, upper, rowsize, colsize):
    return [[randint(lower,upper) for col in range(colsize)] for row in range (rowsize)]

def matGetCol(matrix, colnumber):
    getcol = [ [row[colnumber] for row in matrix]]
    return getcol

def matGetIJ(matrix, i, j): #retrives the ij element from a matrix
    icol = matGetCol(matrix, i - 1)
    return icol[0][j - 1]

def matPrint(matrix):
    for row in matrix:
        print row

def matTranspose(matrix):
    return [[row[col] for row in matrix] for col in range(len(matrix[0]))]

"""###########################################################
Main Script
##########################################################"""

print "\n\nSimplex Method Python Script\nWritten by: Stephen Thomas"

print "Form is z = c1x1 + ... + cnxn, for n = %d" % lp_num_vars
print "Constants [cn] randomly generated."
print "Matrix form is Ax = b"
print "  -Matrix A is the LHS of the constraint equations"
print "  -Matrix b is the RHS of the constraint equations"
print "  -Matrix x is the solution vector that optimizes the objective function"


print "\nGenerating random LP...\n"


generateLP(lp_num_vars, lp_num_const) #Generates a LP

print "Objective Function:"

sout = ""
xvar = 1
for vars in obj_func:
    if xvar == lp_num_vars:
        sout += "%sX%d" % (str(vars), xvar)
    else:
        sout += "%sX%d+" % (str(vars), xvar)
        xvar += 1

print "Maximize z = %s" % sout

A = matrix(mat_a)
x = matrix(mat_x)
b = matrix(mat_b)
AT = matTranspose(mat_a)

print "\nCalculating solutions..."

comboxl = list(range(20))
z = 0
z_max = -1000000
z_min = 1000000

for combo5 in combinations(comboxl, 5):
    mat_Bs = []
    mat_ctb = []
    z +=1

    if z == 100000: #we can arbitrarily exit the loop here
        break
    else:
        for entry in combo5:
            mat_Bs.extend(matGetCol(mat_a, entry))
            mat_ctb.extend(obj_func[entry])

        B = matrix(mat_Bs)
        ctb = matrix(mat_ctb)

        try:
            BI = linalg.inv(B)
        except linalg.LinAlgError: #B can not invert
            mat_sing += 1
            pass
        else: #B is invertible, calc BI*B for feasibility of basic soln
            soln = BI*b
            if checkSoln(soln) == 1:
                soln_inf += 1
            else:
                soln_feas += 1

                #CALCULATE OBJECTIVE HERE
                obj_z = ctb*soln
                if obj_z > z_max:
                    mat_x = matGenRanInt(0, 0, lp_num_vars, 1)
                    z_max = obj_z
                    stepthru = 0
                    for idx in combo5:
                        mat_x[idx] = soln[stepthru] #generate soln matrix x
                        stepthru += 1

                if obj_z < z_min:
                    z_min = obj_z


print "\nMatrix A:"
print A
print "\nMatrix x:"
print matrix(mat_x)
print "\nMatrix b:"
print b

print "\nCombinations Enumerated: %d" % z
print "Feasible Solutions: %d" % soln_feas
print "Infeasible Solutions: %d" % soln_inf
print "Non-Basic Solutions: %d" % mat_sing
print "Maximum Objective Value: %d" % z_max
print "Minimum Objective Value: %d" % z_min

#END OF CODE