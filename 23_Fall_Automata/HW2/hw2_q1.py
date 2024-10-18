import string

# Get data from Input, and organize them
def inputGrammar():
    grammar = {}

    try:
        while(True):
            conv = input()
            if conv is None or conv == "":
                return grammar

            word = conv.split(":")
            variable = word[0]
            conversion = word[1]

            if variable not in grammar:
                grammar[variable] = [conversion]
            else:
                grammar[variable].append(conversion)
            
    except:
        pass
    
    return grammar


# Check if variable
def isVariable(value):
    return len(value)==1 and value.isalpha()


# Get graph between all variables
def getVariableGraph(grammar):
    variableGraph = {}

    for variable, conversions in grammar.items():
        variableGraph[variable] = []
        for conversion in conversions:
            if isVariable(conversion):
                variableGraph[variable].append(conversion)

    return variableGraph


# Get A *=> ?
def getPathToVariable(variableGraph, startVariable):
    # get all variables
    visit = []
    visited = {}
    for variable in variableGraph:
        visited[variable] = False

    # visit other variables
    queue = [startVariable]
    visited[startVariable] = True
    while len(queue) > 0:
        now = queue[0]
        paths = variableGraph[now]
        for next in paths:
            if visited[next] == False:
                visited[next] = True
                visit.append(next)
                queue.append(next)
        del queue[0]

    return visit


# Remove unit production
def removeUnitProduction(grammar):
    variableGraph = getVariableGraph(grammar)

    grammarP2 = {}

    for variable, conversions in grammar.items():
        grammarP2[variable] = []

        # put in P2 that not unit production
        for conversion in conversions:
            if not isVariable(conversion):
                grammarP2[variable].append(conversion)
        
        # put in P2 that A *=> B and B -> x is not unit production
        pathVariables = getPathToVariable(variableGraph, variable)
        for path in pathVariables:
            pathConversions = grammar[path]
            for pathConversion in pathConversions:
                if not isVariable(pathConversion):
                    grammarP2[variable].append(pathConversion)

        # remove variable if there is no conversion
        if grammarP2[variable] == []:
            del grammarP2[variable]

    return grammarP2


# get vacant variables
def getVacantVariables(grammar):
    vacantVariables = list(string.ascii_uppercase)
    vacantVariables.extend(list(string.ascii_lowercase))
    for occupiedVariable in grammar:
        vacantVariables.remove(occupiedVariable)

    return vacantVariables


# get (alphabet or variables) -> A that is the only A -> (alphabet or variables)
def getReverseGrammar(grammar):
    reverseGrammar = {}
    for variable, conversions in grammar.items():
        if len(conversions) == 1:   # assume that there is no unit production
            reverseGrammar[conversions[0]] = variable

    return reverseGrammar


# Convert to Chomsky Normal Form
def convertChomskyNormForm(grammar):
    grammarP3 = {}
    reverseGrammar = getReverseGrammar(grammar)
    vacantVariables = getVacantVariables(grammar)

    for variable, conversions in grammar.items():
        grammarP3[variable] = []

        for i in range(len(conversions)):
            conversion = conversions[i]
            if len(conversion) == 1:    # assume that there is no unit production
                grammarP3[variable].append(conversion)
                continue

            # convert alphabets into variables if r>=2
            newConversion = []
            for value in conversion:
                if isVariable(value):
                    newConversion.append(value)
                else:
                    if value in reverseGrammar:
                        newConversion.append(reverseGrammar[value])
                    else:
                        if len(vacantVariables) == 0:   # Error! There is no vacant variable
                            return grammar
                        reverseGrammar[value] = vacantVariables[0]
                        newConversion.append(vacantVariables[0])
                        grammarP3[vacantVariables[0]] = [value]
                        del vacantVariables[0]
            newConversion = "".join(newConversion)

            # convert A -> BCDE... into A->Ba, a->Cb, b->Dc... etc
            length = len(newConversion)
            for j in range(length-1, 1, -1):
                part = newConversion[j-1:j+1]
                if part in reverseGrammar:
                    newConversion = newConversion[0:j-1] + reverseGrammar[part]
                else:
                    if len(vacantVariables) == 0:   # Error! There is no vacant variable
                        return grammar
                    reverseGrammar[part] = vacantVariables[0]
                    newConversion = newConversion[0:j-1] + vacantVariables[0]
                    grammarP3[vacantVariables[0]] = [part]
                    del vacantVariables[0]
            grammarP3[variable].append(newConversion[0:2])

    return grammarP3
                

# print grammar (for debugging)
def printGrammar(grammar):
    for variable, conversions in grammar.items():
        print(variable, end=" -> ")
        for conversion in conversions:
            print(conversion, end=" | ")
        print()
    return


# std output grammar (real output)
def outputGrammar(grammar):
    for variable, conversions in grammar.items():
        for conversion in conversions:
            print(variable + ":" + conversion)
    return

grammar = inputGrammar()
grammar = removeUnitProduction(grammar)
#printGrammar(grammar)
#print()
grammar = convertChomskyNormForm(grammar)
#printGrammar(grammar)
outputGrammar(grammar)