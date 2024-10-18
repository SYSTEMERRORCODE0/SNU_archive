

#
#   turing machine structure
#   turing_machine[state number][alphabet][0] : next state
#   turing_machine[state number][alphabet][1] : change alphabet into
#   turing_machine[state number][alphabet][2] : move L/R
#

# Get data from Input, and organize them
def inputTuringMachine():
    turing_machine = {}

    try:
        conv = input()
        word = conv.split()

        N = int(word[0])
        string = list(word[1])

        for state in range(N):
            state_prop = {}
            for alphabet in string:
                conv = input()
                word = conv.split()

                transition = []

                transition.append(int(word[0]))
                transition.append(word[1])
                transition.append(word[2])

                state_prop[alphabet] = transition

            turing_machine[state] = state_prop
            
    except:
        pass
    
    return N, turing_machine

# run turing machine with string
def run_turing_machine(N, turing_machine, w):

    state = 0
    tape = list(w)
    tape_length = len(tape)
    head = -1

    transitions = 0

    # already dead state
    if state >= N:
        return w, state

    # transition runs until dead state
    while True:
        
        # if the head out of running tape, extend it with '#'
        if head >= tape_length:
            tape.append('#')
            tape_length += 1
        elif head == -1:
            tape.insert(0, '#')
            head = 0
            tape_length += 1
        
        alphabet = tape[head]

        # transition
        transition = turing_machine[state][alphabet]

        tape[head] = transition[1]
        if transition[2] == 'R':
            head += 1
        elif transition[2] == 'L':
            head -= 1

        state = transition[0]

        # into the dead state
        if state >= N:
            break

    # get organized string in tape
    result = ''.join(tape)
    result = result.strip('#')

    return result, state




N, turing_machine = inputTuringMachine()

K = int(input())
for i in range(K):
    w = input()
    tape, state = run_turing_machine(N, turing_machine, w)
    print(tape, state)
