startVar = ""

# Get data from Input, and organize them
def inputGrammar():

    global startVar

    grammar = {}
    sentence = ""

    try:
        while(True):
            conv = input()
            if conv is None or conv == "":
                return grammar, sentence

            word = conv.split(":")
            if len(word) == 1:
                sentence = word[0]
                return grammar, sentence    # normally return into here

            variable = word[0]
            if startVar == "":
                startVar = variable
            conversion = word[1]

            if variable not in grammar:
                grammar[variable] = [conversion]
            else:
                grammar[variable].append(conversion)
            
    except:
        pass
    
    return grammar, sentence


# run CYK algorithm
def CYK(grammar, sentence):

    global startVar

    n = len(sentence)
    mem = [[set() for i in range(n+1)] for j in range(n+1)]

    # initial V_ii
    for i in range(1, n+1):
        for variable, conversions in grammar.items():
            if sentence[i-1] in conversions:
                mem[i][i].add(variable)

    # Step with DP
    for d in range(1, n):
        for i in range(1, n-d+1):
            j = i + d
            for k in range(i, j):
                for variable, conversions in grammar.items():
                    for conversion in conversions:
                        if len(conversion) == 1:    # A -> (alphabet)
                            continue
                        if conversion[0] in mem[i][k] and conversion[1] in mem[k+1][j]:
                            mem[i][j].add(variable)

    # print for Debugging
    #print(mem)

    return startVar in mem[1][n]


grammar, sentence = inputGrammar()
result = CYK(grammar, sentence)
if result:
    print("yes")
else:
    print("no")