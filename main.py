from solver import CDCL
from get_clauses import get_clauses
from pysat.formula import CNF
from pysat.solvers import Solver

def solve(n, truth_tables, use_pysat=True):
    r = 1
    if use_pysat:
        while True:
            cnf = CNF(from_clauses = get_clauses(n, truth_tables, r)[0])
            with Solver(bootstrap_with=cnf) as solver:
                solved = solver.solve()
                print(str(r) + ": " + f'{"SAT" if solved else "UNSAT"}')
                if solved:
                    return solver.get_model()
            r += 1
    else:
        while True:
            clauses, num_vars = get_clauses(n, truth_tables, r)
            val = CDCL(clauses, 30)
            print(str(r) + ": " + val[0])
            if val[0] == "Time limit reached.":
                return None
            if val[0] == "SAT":
                return val[1]
            r += 1

# write specific set of clauses to c.cnf if you want to
"""
clauses = get_clauses(3, ["01101001", "00010111"], 4)
with open("../sat exact synthesis/c.cnf", 'w') as f:
    f.write("p cnf ")
    f.write(str(clauses[1]))
    f.write(" ")
    f.write(str(len(clauses[0])))
    f.write("\n")
    for clause in clauses[0]:
        for literal in clause:
            f.write(str(literal) + " ")
        f.write("0\n")
"""

# random tests
#test_clauses = [[1, 4], [1, -3, -8], [1, 8, 12], [2, 11], [-7, -3, 9], [-7, 8, -9], [7, 8, -10], [7, 10, -12]]
#test_clauses = get_clauses(2, ["0110"], 1)[0]
#test_clauses = [[1, 2], [-1, 2], [1, -2], [-1, -2]]

n = str(input("n: ")).strip()
while not n.isdigit():
    n = str(input("n: ")).strip()
n = int(n)
truth_tables = str(input("truth tables (syntax = 01101001 00010111 ...): ")).strip().split()
correct_syntax = True
for m in truth_tables:
    if not all (d in '01' for d in m):
        correct_syntax = False
while not correct_syntax:
    truth_tables = str(input("truth tables (syntax = 01101001 00010111 ...): ")).strip().split()
    correct_syntax = True
    for m in truth_tables:
        if not all(d in '01' for d in m):
            correct_syntax = False
use_pysat = str(input("use pysat? (recommended because my CDCL implementation is extremely slow and limited, y/n): ")).strip().lower()
while use_pysat != "y" and use_pysat != "n":
    use_pysat = str(input("use pysat? (recommended because my CDCL implementation is extremely slow and limited, y/n): ")).strip().lower()

print(solve(n, truth_tables))