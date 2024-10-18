
# Get data from Input, and organize them
def inputAutomata():

    conv = input()
    string_list = conv.split()[1:]

    automata = []
    try:
        while(True):
            conv = input()
            if conv is None or conv == "":
                break

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

            automata.append(data)
    except:
        pass
    return string_list, automata


# both DFA, NFA is available
def run(automata, string):
    state_queue = set([0])
    
    for character in string:
        new_queue = set([])

        for state in state_queue:
            new_queue = new_queue.union(set(automata[state][character]))

        e_queue = list(new_queue)
        while len(e_queue) > 0:
            e_path = automata[e_queue[0]]['e']

            for state in e_path:
                if state not in new_queue:
                    new_queue = new_queue.union(set([state]))
                    e_queue.append(state)

            del(e_queue[0])
        
        state_queue = new_queue

    for state in state_queue:
        if automata[state]['is_final_state'] == 1:
            return "yes"
        
    return "no"

string_list, automata = inputAutomata()
for string in string_list:
    print(run(automata, string))