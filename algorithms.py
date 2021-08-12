from automata import *
from syntax_tree import *

def regular_expression_to_fsm(expression):
	tree = Syntax_Tree(expression.replace(" ", ""))
	start_state = ''.join(map(str, sorted(list(tree.firstpos[1])))) 
	alphabet = []
	for i in tree.roots:
		if tree.tree[i] != '#' and tree.tree[i] not in alphabet:
			alphabet.append(tree.tree[i])

	transitions = {}
	states = []
	unmarked_states = [tree.firstpos[1]]
	while(unmarked_states):
		state = unmarked_states.pop()
		state_name = ''.join(map(str, sorted(list(state))))
		transitions[state_name] = {}
		states.append(state_name)
		for symbol in alphabet:
			b = set()
			for i in state:
				for index, value in tree.roots.items():
					if i == value and tree.tree[index] == symbol:
						b = b | tree.followpos[i]
			b_name = ''.join(map(str, sorted(list(b))))
			if b and b not in unmarked_states and b_name not in states:
				unmarked_states.append(b)
			if b_name:
				transitions[state_name][symbol] = [b_name]

	final_states = []
	final_state_name = str(len(tree.roots))
	for state in states:
		if final_state_name in state:
			final_states.append(state)


	fsm = Automata(states, alphabet, start_state, final_states, transitions)
	return fsm		


def determinize_automata(automata):
	episulon_closure = {}
	for state in automata.states:
		episulon_closure[state] = automata.episulon_closure(state)
	
	states = []
	transitions = {}
	start_state = ''.join(sorted(episulon_closure[automata.start_state]))
	final_states = []
	states_to_be_added = []
	states_to_be_added.append(episulon_closure[automata.start_state])

	while(states_to_be_added):
		new_state = states_to_be_added.pop(0)
		new_state_name = ''.join(sorted(list(new_state)))
		states.append(new_state_name)
		for state in new_state:
			if state in automata.final_states and new_state_name not in final_states:
				final_states.append(new_state_name)

		transitions[new_state_name] = {}

		for symbol in automata.alphabet:
			destiny = set()
			for state in new_state:
				if symbol not in automata.transitions[state]:
					continue

				for transition in automata.transitions[state][symbol]:
					destiny.add(transition)
					for episulon_transition in automata.episulon_closure(transition):
						destiny.add(episulon_transition)

			if (destiny):
				string_destiny = ''.join(sorted(destiny))
				transitions[new_state_name][symbol] = [string_destiny]

				if (string_destiny not in states) and (destiny not in states_to_be_added):
					states_to_be_added.append(destiny)

	new_automata = Automata(states, automata.alphabet, start_state, final_states, transitions)
	return new_automata

def remove_dead_states(automata):
	states = []
	to_check = [x for x in automata.final_states]

	while(to_check):
		check_state = to_check.pop()
		states.append(check_state)
		for origin, transition in automata.transitions.items():
			for symbol, destiny in transition.items():
				for state in destiny:
					if state == check_state and origin not in states and origin not in to_check:
						to_check.append(origin)

	alphabet = automata.alphabet
	start_state = automata.start_state
	final_states = automata.final_states

	for origin, transition in dict(automata.transitions).items():
		if origin not in states:
			del automata.transitions[origin]
		else:
			for symbol, destiny in transition.items():
				for destiny_state in destiny:
					if destiny_state not in states:
						automata.transitions[origin][symbol].remove(destiny_state)
						if not automata.transitions[origin][symbol]:
							del automata.transitions[origin][symbol]

	transitions = automata.transitions

	resulting_automata = Automata(states, alphabet, start_state, final_states, transitions)
	return resulting_automata

def remove_equivalent_states(automata):
	p = [automata.final_states, [state for state in automata.states if state not in automata.final_states]]
	consistent = False
	while not consistent:
		consistent = True
		for sets in p:
			for symbol in automata.alphabet:
				for sett in p:
					temp = []
					for q in sett:
						if symbol in automata.transitions[q]:
							for destiny in automata.transitions[q][symbol]:
								if destiny in sets:
									if q not in temp:
										temp.append(q)
					if temp and temp != sett:
						consistent = False
						p.remove(sett)
						p.append(temp)
						temp_t = list(sett)
						for state in temp:
							temp_t.remove(state)

						p.append(temp_t)
	return recreate_states(automata, p)

def recreate_states(automata, p):
    states = []
    for state in p:
        states.append(''.join(state))
    for state in p:
        if automata.start_state in state:
            start_state = ''.join(state)
            break
    final_states = []
    for state in p:
        for final_state in automata.final_states:
            if final_state in state and ''.join(state) not in final_states:
                final_states.append(''.join(state))

    transitions = {}
    for state in p:
        state_name = ''.join(state)
        transitions[state_name] = {}
        for symbol in automata.alphabet:
        	destiny = ''
        	if symbol in automata.transitions[state[0]]:
        		for state2 in p:
        			for transition_destiny in automata.transitions[state[0]][symbol]:
        				if transition_destiny in state2:
        					destiny = ''.join(state2)
        	if destiny:
        		transitions[state_name][symbol] = [destiny]

    resulting_automata = Automata(states, automata.alphabet, start_state, final_states, transitions)
    return resulting_automata

def unite_automata(automata_1, automata_2):
	automata_1.remove_name_conflict(automata_2)
	start_state = 'q0'
	while(start_state in automata_1.states or start_state in automata_2.states):
		start_state += '\''
	states = automata_1.states + automata_2.states
	states.append(start_state)
	final_states = automata_1.final_states + automata_2.final_states
	alphabet = set(automata_1.alphabet)
	alphabet.union(automata_2.alphabet)
	alphabet = list(alphabet)
	transitions = dict(automata_1.transitions)
	transitions.update(automata_2.transitions)
	transitions[start_state] = {}
	transitions[start_state]['&'] = [automata_1.start_state, automata_2.start_state]

	automata = Automata(states, alphabet, start_state, final_states, transitions)
	return automata
