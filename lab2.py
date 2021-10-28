import sys


clauses = []
constants = []
functions = []
predicates = []
variables = []


# Parses the file content into global data structures
def file_parse(file):
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

        filename = sys.argv[1].split(".")
        if filename[1] != "cnf":
            print("The file " + sys.argv[1] + " has an incorrect file format - it must be a cnf file!")
        else:
            file_parse(open(sys.argv[1], "r"))


# Runs the lab2 file
if __name__ == '__main__':
    main()
