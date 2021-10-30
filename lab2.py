import sys


clauses = []
constants = []
expressions = []
functions = []
predicates = []
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
    return


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
        values = expression.split(" ")
        if len(values) == 3:
            first = values[0]
            operator = values[1]
            second = values[2]
            for i in expressions:
                if i == first and operator == "→":
                    expressions.append(second)

    good = "yes"
    for expression in expressions:
        print(expression)
        for comparable in expressions:
            if comparable[1:len(comparable)] == expression:
                good = "no"
    print(good)


# Tests the test cases for universals
def test_universals():
    return


# Tests the test cases for universals + constants
def test_universe_constants():
    return


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
                i = i + 1
        elif (things[0]) == "Variables:":
            i = 1
            while i < len(things):
                variables.append(things[i])
                i = i + 1
        elif (things[0]) == "Constants:":
            i = 1
            while i < len(things):
                constants.append(things[i])
                i = i + 1
        elif (things[0]) == "Functions:":
            i = 1
            while i < len(things):
                functions.append(things[i])
                i = i + 1
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
