import math
import itertools

variables = {}

def new_var(name):
    if name in variables:
        return variables[name]
    variables[name] = len(variables) + 1
    return len(variables)

def exactly_one(var_list, clauses):
    clause = []
    for var in var_list:
        clause.append(var)
    clauses.append(clause)

    for combs in itertools.combinations(var_list, 2):
        clause = []
        for var in combs:
            clause.append(-var)
        clauses.append(clause)

    return clauses

def get_clauses(n, tt, r):
    clauses = []
    variables.clear()

    for i in range(n+1,n+1+r):
        combs = []
        for j in range(1, i):
            for k in range(j + 1, i):
                combs.append(new_var("s{}{}{}".format(i, j, k)))
        clauses = exactly_one(combs, clauses)


    for h in range(1,len(tt)+1):
        h_i = []
        for i in range(n+1, n+1+r):
            h_i.append(new_var("g{}{}".format(h, i)))
        clauses = exactly_one(h_i, clauses)

    for i in range(1,n+1):
        for t in range(int(math.pow(2, n))):
            clause = []
            if (t >> i - 1) & 1:
                clause.append(new_var("x{}{}".format(i, t)))
            else:
                clause.append(-new_var("x{}{}".format(i, t)))
            clauses.append(clause)

    for i in range(n+1,n+1+r):
        for j in range(1, i):
            for k in range(j + 1, i):
                for (a, b, c) in itertools.product(range(0, 2), repeat=3):
                    for t in range(int(math.pow(2, n))):
                        clause = [-new_var("s{}{}{}".format(i, j, k))]
                        if a == 1:
                            clause.append(-new_var("x{}{}".format(i, t)))
                        else:
                            clause.append(new_var("x{}{}".format(i, t)))

                        if b == 1:
                            clause.append(-new_var("x{}{}".format(j, t)))
                        else:
                            clause.append(new_var("x{}{}".format(j, t)))

                        if c == 1:
                            clause.append(-new_var("x{}{}".format(k, t)))
                        else:
                            clause.append(new_var("x{}{}".format(k, t)))

                        if a == 1:
                            clause.append(new_var("f{}{}{}".format(i, b, c)))
                        else:
                            clause.append(-new_var("f{}{}{}".format(i, b, c)))

                        clauses.append(clause)

    for h in range(1, len(tt)+1):
        for t in range(int(math.pow(2, n))):
            for i in range(n+1,n+1+r):
                clause = [-new_var("g{}{}".format(h, i))]
                if tt[h - 1][t] == "1":
                    clause.append(new_var("x{}{}".format(i, t)))
                else:
                    clause.append(-new_var("x{}{}".format(i, t)))

                clauses.append(clause)

    for i in range(n+1, n+1+r):
        clauses.append([-new_var("f{}{}{}".format(i, 0, 0))])

    for i in range(n+1, n+1+r):
        clauses.append([new_var("f{}{}{}".format(i, 0, 1)), new_var("f{}{}{}".format(i, 1, 0)),
                        new_var("f{}{}{}".format(i, 1, 1))])
        clauses.append([new_var("f{}{}{}".format(i, 0, 1)), -new_var("f{}{}{}".format(i, 1, 0)),
                        -new_var("f{}{}{}".format(i, 1, 1))])
        clauses.append([-new_var("f{}{}{}".format(i, 0, 1)), new_var("f{}{}{}".format(i, 1, 0)),
                        -new_var("f{}{}{}".format(i, 1, 1))])

    for i in range(n+1, n+1+r):
        clause = []
        for j in range(1, len(tt)+1):
            clause.append(new_var("x{}{}".format(j, i)))
        for j in range(i+1, n+1+r):
            for k in range(1, i):
                clause.append(new_var("s{}{}{}".format(j, k, i)))
        for j in range(i+1, n+r+1):
            for k in range(i+1, j):
                clause.append(new_var("s{}{}{}".format(j, k, i)))

        clauses.append(clause)

    for j in range(1, i):
        for k in range(j+1, i):
            for l in range(i+1, n+1+r):
                clauses.append([-new_var("s{}{}{}".format(i, j, k)), -new_var("s{}{}{}".format(l, j, i))])
                clauses.append([-new_var("s{}{}{}".format(i, j, k)), -new_var("s{}{}{}".format(l, k, i))])

    num = len(variables)

    for clause in clauses:
        if len(clause) == 0:
            clauses.remove(clause)

    return clauses, num