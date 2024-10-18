
# Get data from Input, and organize them
def inputNfa():
    nfa = []
    
    try:
        while(True):
            conv = input()
            if conv is None or conv == "":
                return nfa

            state = conv.split()

            data = {}
            data['state'] = int(state[0])
            data['is_final_state'] = int(state[1])

            # paths
            if state[2] == "-":
                data['0'] = []
            else:
                paths = state[2].split(',')
                zero_list = []
                for path in paths:
                    zero_list.append(int(path))
                data['0'] = zero_list

            if state[3] == "-":
                data['1'] = []
            else:
                paths = state[3].split(',')
                one_list = []
                for path in paths:
                    one_list.append(int(path))
                data['1'] = one_list

            if state[4] == "-":
                data['e'] = []
            else:
                paths = state[4].split(',')
                e_list = []
                for path in paths:
                    e_list.append(int(path))
                data['e'] = e_list

            nfa.append(data)
    except:
        pass
    return nfa

# numbering states(zipped) to 0~
state_transform = {}
# state queue for search paths
state_queue = []

# states zipped (int) to state list
def unzipState(state_zip):
    i=0
    state_list = []
    while state_zip > 0:
        if state_zip % 2 == 1:
            state_list.append(i)
        i = i + 1
        state_zip = state_zip // 2

    return state_list

# zip state list to zipped states (int)
def zipState(state_list):
    state_zip = 0
    for state in state_list:
        state_zip = state_zip + pow(2, state)
    
    return state_zip

# check if there are final states in the state list
def checkFinalState(nfa, state_list):
    for state in state_list:
        if nfa[state]['is_final_state'] == 1:
            return 1
        
    return 0

# transform path list to state
def transformPathListToState(dfa):
    for i in range(0,len(dfa)):
        dfa[i]['0'] = state_transform[zipState(dfa[i]['0'])]
        dfa[i]['1'] = state_transform[zipState(dfa[i]['1'])]
    return dfa

# main function for convert NFA to DFA
def nfaToDfa(nfa):
    global state_transform
    global state_queue

    state_transform = {}
    state_queue = []

    alphabets = ['0', '1']  # e will be checked individually
    n = len(nfa)

    dfa = []

    # initialize with state 0
    state_queue.append(1)
    state_transform[1] = 0
    state_idx = 1

    # using bfs
    while len(state_queue) > 0:
        
        # initialize a dfa state
        dfa_state = {}

        state_zip = state_queue[0]
        dfa_state['state'] = state_transform[state_zip]

        # check final state
        state_list = unzipState(state_zip)
        dfa_state['is_final_state'] = checkFinalState(nfa, state_list)

        for alphabet in alphabets:
            
            path_list = []
            for state in state_list:
                path_list.extend(nfa[state][alphabet])
            path_list = list(set(path_list))

            # check e paths
            path_queue = []
            for path in path_list:
                path_queue.append(path)
            
            while len(path_queue) > 0:  # also use bfs
                path = path_queue[0]
                e_path_list = nfa[path]['e']

                for e_path in e_path_list:
                    if e_path not in path_list:
                        path_queue.append(e_path)
                        path_list.append(e_path)

                del(path_queue[0])
                
            # organize path list
            path_list.sort()
            path_zip = zipState(path_list)

            # new state into queue
            if path_zip not in state_transform.keys():
                state_queue.append(path_zip)
                state_transform[path_zip] = state_idx
                state_idx = state_idx + 1

            dfa_state[alphabet] = path_list

        dfa.append(dfa_state)
        del(state_queue[0])

    dfa = transformPathListToState(dfa)

    return dfa

# print DFA
def printDfa(dfa):
    for dfa_state in dfa:
        print(dfa_state['state'], dfa_state['is_final_state'], dfa_state['0'], dfa_state['1'], "-")
    return

nfa = inputNfa()
dfa = nfaToDfa(nfa)
printDfa(dfa)