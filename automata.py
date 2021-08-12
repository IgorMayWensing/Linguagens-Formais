class Automata():
	def __init__(self, states, alphabet, start_state, final_states, transitions):
		self.states = states
		self.alphabet = alphabet
		self.start_state = start_state
		self.final_states = final_states
		self.transitions = transitions

	def __str__(self):
		string = ' '.join(self.states) + '\n'
		string += ' '.join(self.alphabet) + '\n'
		string += self.start_state + '\n'
		string += ' '.join(self.final_states) + '\n'
		for source, symbol_dict in self.transitions.items():
			for symbol, destiny_list in symbol_dict.items():
				for destiny in destiny_list:
					string += source + ' -> ' + destiny + ' ' + symbol + '\n'

		return string

	def episulon_closure(self, state):
		state_closure = set()
		if '&' in self.transitions[state]:
			for to_state in self.transitions[state]['&']:
				if to_state != state:
					to_state_closure = self.episulon_closure(to_state)
					state_closure = state_closure.union(to_state_closure)
		state_closure.add(state)
		return state_closure

	def remove_name_conflict(self, automata_2):
		changed = False
		for state in list(self.states):
			if state in automata_2.states:
				changed = True
				for origin, transition in dict(self.transitions).items():
					if origin == state:
						self.transitions[state+'\''] = dict(self.transitions[state])
						del self.transitions[state]
					for symbol, destiny in transition.items():
						if origin != state:
							if symbol in self.transitions[origin] and state in destiny:
								self.transitions[origin][symbol].remove(state)
								self.transitions[origin][symbol].append(state + '\'')
						else:
							if symbol in self.transitions[origin+'\''] and state in destiny:
								self.transitions[origin+'\''][symbol].remove(state)
								self.transitions[origin+'\''][symbol].append(state + '\'')
				self.states.remove(state)
				self.states.append(state+'\'')
				if self.start_state == state:
					self.start_state = state + '\''
				if state in self.final_states:
					self.final_states.remove(state)
					self.final_states.append(state+'\'')

		if changed:
			self.remove_name_conflict(automata_2)

	def complement(self):
		final_states = []
		for state in self.states:
			if state not in self.final_states:
				final_states.append(state)

		self.final_states = final_states
