import sys


clauses = []
constants = []
expressions = []
functions = []
predicates = []
revised_clauses = []
revised_expressions = []
unification = []
variables = []


# Tests the test cases for constants
def test_constants():
    for clause in clauses:
        values = clause.split(" ")
        if len(values) == 1:
            expressions.append(values[0])
        else:
            first = values[0]
            second = values[1]
            if first[0:1] == "!":
                if second[0:1] == "!":
                    expressions.append(first[1:len(first)] + " → ¬" + second[1:len(second)])
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append("¬" + second[1:len(second)])
                else:
                    expressions.append(first[1:len(first)] + " → " + second)
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append(second)
            else:
                expressions.append(first + " ∨ " + second)

    good = "yes"
    for expression in expressions:
        for comparable in expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Tests the test cases for functions
def test_functions():
    temp = []
    for clause in clauses:
        new = None
        i = 0
        while i < len(clause)-8:
            if clause[i:i+8] in functions:
                if new is not None:
                    new = new.replace(clause[i:i + 8], "%y")
                else:
                    new = clause.replace(clause[i:i+8], "%y")
            i += 1
        if new is not None:
            temp.append(new)
        else:
            temp.append(clause)

    for clause in temp:
        new = None
        i = 0
        while i < len(clause)-2:
            if clause[i:i+2] in variables:
                if new is not None:
                    new = new.replace(clause[i:i+2], "%x")
                else:
                    new = clause.replace(clause[i:i+2], "%x")
            i += 1
        if new is not None:
            revised_clauses.append(new)
        else:
            revised_clauses.append(clause)

    comb = None
    sec = None
    thi = None
    for clause in revised_clauses:
        values = clause.split(" ")
        if len(values) == 1:
            expressions.append(values[0])
        elif len(values) == 2:
            first = values[0]
            second = values[1]
            if first[0:1] == "!":
                if second[0:1] == "!":
                    expressions.append(first[1:len(first)] + " → ¬" + second[1:len(second)])
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append("¬" + second[1:len(second)])
                else:
                    expressions.append(first[1:len(first)] + " → " + second)
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append(second)
            else:
                expressions.append(first + " ∨ " + second)
        else:
            if comb is not None:
                second = values[1]
                third = values[2]
                if second == sec and third == thi:
                    comb += " ^ " + values[0]
                    expressions.append(comb)
                else:
                    expressions.append(comb)
                comb = None
                sec = None
                thi = None
            else:
                first = values[0]
                second = values[1]
                sec = second
                third = values[2]
                thi = third
                if first[0:1] == "!":
                    comb = first[1:len(first)] + " → " + second + " ∨ " + third
                else:
                    comb = second[1:len(second)] + " ∧ " + third[1:len(third)] + " → " + first

    for expression in expressions:
        if expression[0:5] == "loves":
            revised_expressions.append("loves(%y,%x)")
            continue
        elif expression[1:6] == "loves":
            revised_expressions.append("!loves(%y,%x)")
            continue
        elif expression[0:4] == "tail":
            revised_expressions.append("tail(%y)")
            continue
        elif expression[1:5] == "tail":
            revised_expressions.append("!tail(%y)")
            continue
        else:
            new = None
            for constant in constants:
                i = 0
                while i < (len(expression)-len(constant)):
                    if expression[i:i + len(constant)] == constant:
                        new = expression.replace(expression[i:i + len(constant)], "%x")
                    i += 1
            if new is None:
                revised_expressions.append(expression)
            else:
                revised_expressions.append(new)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 1:
            value = values[0]
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 3:
                    first = comparable[0]
                    operator = comparable[1]
                    second = comparable[2]
                    if first == value and operator == "→" and second not in revised_expressions:
                        revised_expressions.append(second)
        if len(values) == 3:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in revised_expressions:
                if i == first and operator == "→" and second not in revised_expressions:
                    revised_expressions.append(second)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 5:
            first = values[0]
            satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    satisfied = True
            if satisfied:
                revised_expressions.append(values[2])
                revised_expressions.append(values[4])
        if len(values) == 7:
            first = values[0]
            fir_satisfied = False
            second = values[2]
            sec_satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    fir_satisfied = True
                if j == second:
                    sec_satisfied = True
            if fir_satisfied and sec_satisfied:
                revised_expressions.append(values[4])
                revised_expressions.append(values[6])

    good = "yes"
    for expression in revised_expressions:
        for comparable in revised_expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Tests the test cases for props
def test_prop():
    comb = None
    sec = None
    thi = None
    for clause in clauses:
        values = clause.split(" ")
        if len(values) == 1:
            expressions.append(values[0])
        elif len(values) == 2:
            first = values[0]
            second = values[1]
            if first[0:1] == "!":
                if second[0:1] == "!":
                    expressions.append(first[1:len(first)] + " → ¬" + second[1:len(second)])
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append("¬" + second[1:len(second)])
                else:
                    expressions.append(first[1:len(first)] + " → " + second)
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append(second)
            else:
                expressions.append(first + " ∨ " + second)
        else:
            if comb is not None:
                second = values[1]
                third = values[2]
                if second == sec and third == thi:
                    comb += " ^ " + values[0]
                    expressions.append(comb)
                else:
                    expressions.append(comb)
                comb = None
                sec = None
                thi = None
            else:
                first = values[0]
                second = values[1]
                sec = second
                third = values[2]
                thi = third
                if first[0:1] == "!":
                    comb = first[1:len(first)] + " → " + second + " ∨ " + third
                else:
                    comb = second[1:len(second)] + " ∧ " + third[1:len(third)] + " → " + first
        if comb is not None:
            expressions.append(comb)
            comb = None
            sec = None
            thi = None

    for expression in expressions:
        values = expression.split(" ")
        if len(values) == 1:
            value = values[0]
            for i in expressions:
                comparable = i.split(" ")
                if len(comparable) == 3:
                    first = comparable[0]
                    operator = comparable[1]
                    second = comparable[2]
                    if first == value[1:len(value)] and operator == "∨":
                        expressions.append(second)
                    if second == value[1:len(value)] and operator == "∨":
                        expressions.append(first)
        if len(values) == 3:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in expressions:
                if i == first and operator == "→":
                    expressions.append(second)
        if len(values) == 4:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in expressions:
                if i == first and operator == "→":
                    expressions.append("¬" + second)

    for expression in expressions:
        values = expression.split(" ")
        if len(values) == 5:
            first = values[0]
            satisfied = False
            satisfaction = []
            for i in expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    satisfied = True
            if satisfied:
                expressions.append(values[2])
                expressions.append(values[4])
        if len(values) == 7:
            first = values[0]
            fir_satisfied = False
            second = values[2]
            sec_satisfied = False
            satisfaction = []
            for i in expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    fir_satisfied = True
                if j == second:
                    sec_satisfied = True
            if fir_satisfied and sec_satisfied:
                expressions.append(values[4])
                expressions.append(values[6])

    good = "yes"
    for expression in expressions:
        for comparable in expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Performs unification on clauses
def unify():
    clause = ""
    for param in unification:
        clause += param
        if param != unification[len(unification)-1]:
            clause += " ^ "
    revised_clauses.append(clause)


# Tests the test cases for universals
def test_universals():
    for clause in clauses:
        new = None
        i = 0
        while i < len(clause)-2:
            if clause[i:i+2] in variables:
                if new is not None:
                    new = new.replace(clause[i:i+2], "%" + clause[i:i+1])
                else:
                    new = clause.replace(clause[i:i+2], "%" + clause[i:i+1])
            i += 1
        if new is not None:
            revised_clauses.append(new)
        else:
            revised_clauses.append(clause)

    comb = None
    sec = None
    thi = None
    for clause in revised_clauses:
        values = clause.split(" ")
        if len(values) == 1:
            expressions.append(values[0])
            unification.append(values[0])
        elif len(values) == 2:
            first = values[0]
            second = values[1]
            if first[0:1] == "!":
                if second[0:1] == "!":
                    expressions.append(first[1:len(first)] + " → ¬" + second[1:len(second)])
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append("¬" + second[1:len(second)])
                else:
                    expressions.append(first[1:len(first)] + " → " + second)
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append(second)
            else:
                expressions.append(first + " ∨ " + second)
        else:
            if comb is not None:
                second = values[1]
                third = values[2]
                if second == sec and third == thi:
                    comb += " ^ " + values[0]
                    expressions.append(comb)
                else:
                    expressions.append(comb)
                comb = None
                sec = None
                thi = None
            else:
                first = values[0]
                second = values[1]
                sec = second
                third = values[2]
                thi = third
                if first[0:1] == "!":
                    comb = first[1:len(first)] + " → " + second + " ∨ " + third
                else:
                    comb = second[1:len(second)] + " ∧ " + third[1:len(third)] + " → " + first
        if comb is not None:
            expressions.append(comb)
            comb = None
            sec = None
            thi = None
    unify()

    for expression in expressions:
        new = None
        for constant in constants:
            i = 0
            while i < (len(expression)-len(constant)):
                if expression[i:i + len(constant)] == constant:
                    new = expression.replace(expression[i:i + len(constant)], "%x")
                i += 1
        if new is None:
            revised_expressions.append(expression)
        else:
            revised_expressions.append(new)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 1:
            value = values[0]
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 3:
                    first = comparable[0]
                    operator = comparable[1]
                    second = comparable[2]
                    if first == value and operator == "→" and second not in revised_expressions:
                        revised_expressions.append(second)
                    if first == value[1:len(value)] and operator == "∨":
                        revised_expressions.append(second)
                    if second == value[1:len(value)] and operator == "∨":
                        revised_expressions.append(first)
        if len(values) == 3:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in revised_expressions:
                if i == first and operator == "→" and second not in revised_expressions:
                    revised_expressions.append(second)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 5:
            first = values[0]
            satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    satisfied = True
            if satisfied:
                revised_expressions.append(values[2])
                revised_expressions.append(values[4])
        if len(values) == 7:
            first = values[0]
            fir_satisfied = False
            second = values[2]
            sec_satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    fir_satisfied = True
                if j == second:
                    sec_satisfied = True
            if fir_satisfied and sec_satisfied:
                revised_expressions.append(values[4])
                revised_expressions.append(values[6])

    good = "yes"
    for expression in revised_expressions:
        for comparable in revised_expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Tests the test cases for universals + constants
def test_universe_constants():
    for clause in clauses:
        new = None
        i = 0
        while i < len(clause)-2:
            if clause[i:i+2] in variables:
                if new is not None:
                    new = new.replace(clause[i:i+2], "%" + clause[i:i+1])
                else:
                    new = clause.replace(clause[i:i+2], "%" + clause[i:i+1])
            i += 1
        if new is not None:
            revised_clauses.append(new)
        else:
            revised_clauses.append(clause)

    comb = None
    sec = None
    thi = None
    for clause in revised_clauses:
        values = clause.split(" ")
        if len(values) == 1:
            expressions.append(values[0])
            unification.append(values[0])
        elif len(values) == 2:
            first = values[0]
            second = values[1]
            if first[0:1] == "!":
                if second[0:1] == "!":
                    expressions.append(first[1:len(first)] + " → ¬" + second[1:len(second)])
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append("¬" + second[1:len(second)])
                else:
                    expressions.append(first[1:len(first)] + " → " + second)
                    for i in expressions:
                        if first[1:len(first)] == i:
                            expressions.append(second)
            else:
                expressions.append(first + " ∨ " + second)
        else:
            if comb is not None:
                second = values[1]
                third = values[2]
                if second == sec and third == thi:
                    comb += " ^ " + values[0]
                    expressions.append(comb)
                else:
                    expressions.append(comb)
                comb = None
                sec = None
                thi = None
            else:
                first = values[0]
                second = values[1]
                sec = second
                third = values[2]
                thi = third
                if first[0:1] == "!":
                    comb = first[1:len(first)] + " → " + second + " ∨ " + third
                else:
                    comb = second[1:len(second)] + " ∧ " + third[1:len(third)] + " → " + first
    unify()

    for expression in expressions:
        new = None
        for constant in constants:
            i = 0
            while i < (len(expression) - len(constant)):
                if expression[i:i + len(constant)] == constant:
                    new = expression.replace(expression[i:i + len(constant)], "%x")
                i += 1
        if new is None:
            revised_expressions.append(expression)
        else:
            revised_expressions.append(new)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 1:
            value = values[0]
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 3:
                    first = comparable[0]
                    operator = comparable[1]
                    second = comparable[2]
                    if first == value and operator == "→" and second not in revised_expressions:
                        revised_expressions.append(second)
        if len(values) == 3:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in revised_expressions:
                if i == first and operator == "→" and second not in revised_expressions:
                    revised_expressions.append(second)

    for expression in revised_expressions:
        values = expression.split(" ")
        if len(values) == 5:
            first = values[0]
            satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    satisfied = True
            if satisfied:
                revised_expressions.append(values[2])
                revised_expressions.append(values[4])
        if len(values) == 7:
            first = values[0]
            fir_satisfied = False
            second = values[2]
            sec_satisfied = False
            satisfaction = []
            for i in revised_expressions:
                comparable = i.split(" ")
                if len(comparable) == 1:
                    satisfaction.append(comparable[0])
            for j in satisfaction:
                if j == first:
                    fir_satisfied = True
                if j == second:
                    sec_satisfied = True
            if fir_satisfied and sec_satisfied:
                revised_expressions.append(values[4])
                revised_expressions.append(values[6])

    good = "yes"
    for expression in revised_expressions:
        for comparable in revised_expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Parses the file content into global data structures
def file_parse(file, case):
    is_clause = False
    for line in file:
        things = line.strip().split(" ")
        if is_clause:
            clauses.append(line.strip())
        if (things[0]) == "Predicates:":
            i = 1
            while i < len(things):
                predicates.append(things[i])
                i += 1
        elif (things[0]) == "Variables:":
            i = 1
            while i < len(things):
                variables.append(things[i])
                i += 1
        elif (things[0]) == "Constants:":
            i = 1
            while i < len(things):
                constants.append(things[i])
                i += 1
        elif (things[0]) == "Functions:":
            i = 1
            while i < len(things):
                j = 0
                while j < len(variables):
                    functions.append(things[i] + "(" + variables[j] + ")")
                    j += 1
                i += 1
        elif (things[0].strip()) == "Clauses:":
            is_clause = True

    if case[0:1] == "c":
        test_constants()
    elif case[0:1] == "f":
        test_functions()
    elif case[0:1] == "p":
        test_prop()
    elif case[0:2] == "uc":
        test_universe_constants()
    else:
        test_universals()


# Checks for any errors with the command line arguments
def main():
    if len(sys.argv) != 2:
        print("Please enter the arguments in this format: e.g. python3 lab2.py filename.cnf")
    else:
        try:
            open(sys.argv[1], "r")
        except FileNotFoundError:
            print("The file " + sys.argv[1] + " was not found!")
            quit()

        folders = sys.argv[1].split("/")
        filename = sys.argv[1].split(".")
        if filename[1] != "cnf":
            print("The file " + sys.argv[1] + " has an incorrect file format - it must be a cnf file!")
        else:
            file_parse(open(sys.argv[1], "r"), folders[len(folders)-1])


# Runs the lab2 file
if __name__ == '__main__':
    main()
