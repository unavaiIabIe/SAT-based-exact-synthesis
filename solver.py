from time import time
edited_clauses = []
edited_clause_levels = []
solved_clauses = []
original_solved_clauses = []
current_lev = 0
skip = False
# the messiest code you will ever see
def propagate(clauses, variables, assignments, levels, original_clauses):
    prev_it = clauses.copy()
    global current_lev
    global solved_clauses
    global original_solved_clauses
    original_clauses_to_remove = []
    count = 0
    while count <= len(clauses):
        for i in range(len(clauses)):
            clause = clauses[i]
            original_clause = original_clauses[i]
            if clause in solved_clauses:
                continue

            previous_clause = clause.copy()
            clause = eliminate_variables(clause, variables, assignments, i)
            if clause == previous_clause:
                count += 1
            else:
                count = 0

            conflict_clause = conflict(clause, original_clause, variables, levels)
            if conflict_clause is not None:
                if clauses == prev_it:
                    current_lev = 0
                clauses.append(conflict_clause)
                original_clauses.append(conflict_clause)
                variables, assignments, levels, clauses, UNSAT = backjump(conflict_clause, variables, assignments, levels, clauses, original_clauses)
                if UNSAT:
                    return clauses, variables, assignments, levels, original_clauses, 1
                return clauses, variables, assignments, levels, original_clauses, 0

            contracted_clause = [lit for lit in clause if lit != 0]
            clauses[i] = clause
            if len(contracted_clause) == 1:
                var = contracted_clause[0]
                if abs(var) not in variables:
                    variables.append(abs(var))
                    levels.append(current_lev)
                    solved_clauses.append(clause)
                    original_solved_clauses.append(original_clause)
                    original_clauses_to_remove.append(original_clause)
                    if var > 0:
                        assignments.append(1)
                    else:
                        assignments.append(0)

    return clauses, variables, assignments, levels, original_clauses, 0

def decide(variables, assignments, levels, clauses):
    global current_lev
    current_lev += 1
    for clause in clauses:
        for variable in clause:
            abs_var = abs(variable)
            if abs_var not in variables and abs_var != 0:
                variables.append(abs_var)
                if variable < 0:
                    assignments.append(1)
                else:
                    assignments.append(0)
                levels.append(current_lev)
                return variables, assignments, levels, 0
    return variables, assignments, levels, 1

def conflict(resulting_clause, conflict_clause, variables, levels):
    if len([lit for lit in resulting_clause if lit != 0]) == 0:
        i = 1
        problem_child = variables[-i]
        conflict_clause = conflict_clause.copy()
        while True:
            if problem_child in conflict_clause:
                conflict_clause.remove(problem_child)
                break
            elif -problem_child in conflict_clause:
                conflict_clause.remove(-problem_child)
                break
            i += 1
            problem_child = variables[-i]
        index = i

        for i, clause in enumerate(original_solved_clauses):
            if problem_child in solved_clauses[i] or -problem_child in solved_clauses[i]:
                for lit in clause:
                    if not lit in conflict_clause and abs(lit) != problem_child:
                        conflict_clause.append(lit)

        conflict_levels = []
        for lit in conflict_clause:
            conflict_levels.append(levels[variables.index(abs(lit))])

        removed_vars = []
        problem_child = variables[-index]
        while conflict_levels.count(current_lev) > 1:
            while problem_child not in conflict_clause and -problem_child not in conflict_clause:
                index += 1
                if index > len(variables):
                    index = 0
                problem_child = variables[-index]
            if problem_child in conflict_clause:
                conflict_clause.remove(problem_child)
            else:
                conflict_clause.remove(-problem_child)

            removed_vars.append(problem_child)

            for i, clause in enumerate(original_solved_clauses):
                if problem_child in solved_clauses[i] or -problem_child in solved_clauses[i]:
                    if not any((abs(var) in removed_vars and abs(var) != abs(problem_child)) for var in clause):
                        for lit in clause:
                            if not lit in conflict_clause and abs(lit) != abs(problem_child):
                                conflict_clause.append(lit)

            conflict_levels = []
            for lit in conflict_clause:
                print(levels)
                print(variables)
                print(conflict_clause)
                conflict_levels.append(levels[variables.index(abs(lit))])

        return conflict_clause
    return None

def backjump(conflict_clause, variables, assignments, levels, clauses, original_clauses):
    global current_lev
    global solved_clauses
    global edited_clauses
    global edited_clause_levels
    global original_solved_clauses
    global skip
    skip = True
    ids = [i for i, var in enumerate(variables) if var in conflict_clause]
    conflict_levels = [levels[i] for i in ids]
    if current_lev == 0:
        return variables, assignments, levels, clauses, 1
    if len(conflict_clause) == 1:
        current_lev = 0
    else:
        current_lev = max(conflict_levels)
    ids_tbr = [i for i, level in enumerate(levels) if level > current_lev]
    variables = [var for i, var in enumerate(variables) if i not in ids_tbr]
    assignments = [assignment for i, assignment in enumerate(assignments) if i not in ids_tbr]
    levels = [level for i, level in enumerate(levels) if i not in ids_tbr]
    returning_clauses = [clauses[j] for i, j in enumerate(edited_clauses) if edited_clause_levels[i] not in levels]
    returning_clause_ids = [j for j, clause in enumerate(clauses) if clause in returning_clauses]
    for i, clause in enumerate([original_clause for i, original_clause in enumerate(original_clauses) if i in returning_clause_ids]):
        clauses[returning_clause_ids[i]] = eliminate_variables(clause, variables, assignments, i)
    clause_ids_tbr = [i for i, j, in enumerate(edited_clauses) if clauses[j] not in returning_clauses]
    solved_clauses = [clause for i, clause in enumerate(solved_clauses) if i in clause_ids_tbr]
    original_solved_clauses = [clause for i, clause in enumerate(original_solved_clauses) if i in clause_ids_tbr]
    edited_clauses = [j for i, j in enumerate(edited_clauses) if i in clause_ids_tbr]
    edited_clause_levels = [level for i, level in enumerate(edited_clause_levels) if i in clause_ids_tbr]
    return variables, assignments, levels, clauses, 0

def eliminate_variables(clause, variables, assignments, clause_id):
    global edited_clauses
    global edited_clause_levels
    for i in range(len(variables)):
        variable = variables[i]
        assignment = assignments[i]
        if variable in clause:
            if assignment == 0:
                clause = [0 if var == variable else var for var in clause]
                if clause_id not in edited_clauses:
                    edited_clauses.append(clause_id)
                    edited_clause_levels.append(current_lev)
                else:
                    edited_clause_levels[edited_clauses.index(clause_id)] = current_lev

        elif -variable in clause:
            if assignment == 1:
                clause = [0 if var == -variable else var for var in clause]
                if clause_id not in edited_clauses:
                    edited_clauses.append(clause_id)
                    edited_clause_levels.append(current_lev)
                else:
                    edited_clause_levels[edited_clauses.index(clause_id)] = current_lev

    return clause

def CDCL(clauses, limit):
    global skip
    global current_lev
    variables = []
    assignments = []
    levels = []
    original_clauses = clauses.copy()
    runs = 0
    UNSAT = 0
    starttime = time()
    while time() - starttime < limit:
        runs += 1
        if UNSAT:
            return "UNSAT", None
        clauses, variables, assignments, levels, original_clauses, UNSAT = propagate(clauses, variables, assignments, levels, original_clauses)
        if skip:
            skip = False
            continue

        variables, assignments, levels, SAT = decide(variables, assignments, levels, clauses)
        if SAT:
            return "SAT", [variables[i] * -1 if assignments[i] == 0 else variables[i] for i in range(len(variables))]

    return "Time limit reached.", None


