class Syntax_Tree():
	def __init__(self, expression):
		self.tree = {}
		self.roots = {}
		self.nullable = {}
		self.firstpos = {}
		self.lastpos = {}
		self.followpos = {}
		expression = expression + '#'
		self.create_tree(1, expression)
		self.calculate_nullable(1)
		self.calculate_firstpos(1)
		self.calculate_lastpos(1)
		
		for x,i in self.roots.items():
			self.followpos[i] = set()
		self.calculate_followpos(1)

	def create_tree(self, index, expression):
		if len(expression) == 0:
			return
		elif len(expression) == 1:
			self.tree[index] = expression
			self.roots[index] = len(self.roots)+1
			return

		symbol = expression[len(expression)-1]
		operation = expression[len(expression)-2]

		if symbol != ')' and symbol != '*':
			if operation != '|':
				self.tree[index] = '.'
				self.create_tree(index*2, expression[:-1])
				self.create_tree(index*2+1, symbol)
			else:
				operand_index = self.left_operand_index(expression[:-2])

				if operand_index != 0:
					self.tree[index] = '.'
					self.create_tree(index*2, expression[:operand_index])
					self.create_or_branch(index*2+1, expression[operand_index:])

				else:
					self.create_or_branch(index, expression)

		elif symbol == '*':
			operand_index = self.left_operand_index(expression[:-1])
			if operand_index != 0:
				self.tree[index] = '.'
				self.create_tree(index*2, expression[:operand_index])
				self.create_closure_branch(index*2+1, expression[operand_index:])
			else:
				self.create_closure_branch(index, expression)

		elif symbol == ')':
			opening_index = self.parenthesis_opening_index(expression[:-1])
			predecessor_symbol = expression[opening_index-1]

			if opening_index == 0 or predecessor_symbol != '|':
				expression = expression[:-1]
				expression = list(expression)
				expression.pop(opening_index)
				expression = ''.join(expression)
				self.create_tree(index, expression)

			else:
				operand_index = self.left_operand_index(expression[:opening_index])

				if operand_index != 0:
					self.tree[index] = '.'
					self.create_tree(index*2, expression[:operand_index])
					self.create_or_branch(index*2+1, expression[operand_index:])

				else:
					self.create_or_branch(index, expression)

	def left_operand_index(self, expression):
		symbol = expression[len(expression)-1]

		if symbol == '*':
			return self.left_operand_index(expression[:-1])
		elif symbol != ')':
			return len(expression) - 1
		else:
			opens = self.parenthesis_opening_index(expression[:-1])
			return opens

	def parenthesis_opening_index(self, expression):
		new_closed_parenthesis = 0

		for i in reversed(range(len(expression)-1)):
			if expression[i] == ')':
				new_closed_parenthesis += 1

			elif expression[i] == '(':
				if new_closed_parenthesis == 0:
					return i
				else:
					new_closed_parenthesis -= 1

	def create_or_branch(self, index, expression):
		if expression[len(expression)-1] != ')':
			operator_index = len(expression)-2
		else:
			start_index = self.parenthesis_opening_index(expression[:-1])
			operator_index = start_index - 1	

		self.tree[index] = '|'
		self.create_tree(2*index, expression[:operator_index])
		self.create_tree(2*index+1, expression[operator_index+1:])

	def create_closure_branch(self, index, expression):
		self.tree[index] = '*'
		self.create_tree(2*index+1, expression[:-1])

	def calculate_nullable(self, index):
		if index*2 in self.tree:
			self.calculate_nullable(index*2)
		if index*2+1 in self.tree:
			self.calculate_nullable(index*2+1)

		if self.tree[index] == '|':
			self.nullable[index] = self.nullable[index*2] or self.nullable[index*2+1]
		elif self.tree[index] == '.':
			self.nullable[index] = self.nullable[index*2] and self.nullable[index*2+1]
		elif self.tree[index] == '*':
			self.nullable[index] = True
		else:
			self.nullable[index] = False

	def calculate_firstpos(self, index):
		if index*2 in self.tree:
			self.calculate_firstpos(index*2)
		if index*2+1 in self.tree:
			self.calculate_firstpos(index*2+1)

		if self.tree[index] == '|':
			self.firstpos[index] = self.firstpos[index*2] | self.firstpos[index*2+1]
		elif self.tree[index] == '.':
			if self.nullable[index*2]:
				self.firstpos[index] = self.firstpos[index*2] | self.firstpos[index*2+1]
			else:
				self.firstpos[index] = self.firstpos[index*2]
		elif self.tree[index] == '*':
			self.firstpos[index] = self.firstpos[index*2+1]
		else:
			self.firstpos[index] = {self.roots[index]}

	def calculate_lastpos(self, index):
		if index*2 in self.tree:
			self.calculate_lastpos(index*2)
		if index*2+1 in self.tree:
			self.calculate_lastpos(index*2+1)

		if self.tree[index] == '|':
			self.lastpos[index] = self.lastpos[index*2] | self.lastpos[index*2+1]
		elif self.tree[index] == '.':
			if self.nullable[index*2+1]:
				self.lastpos[index] = self.lastpos[index*2] | self.lastpos[index*2+1]
			else:
				self.lastpos[index] = self.lastpos[index*2+1]
		elif self.tree[index] == '*':
			self.lastpos[index] = self.lastpos[index*2+1]
		else:
			self.lastpos[index] = {self.roots[index]}

	def calculate_followpos(self, index):
		if index*2 in self.tree:
			self.calculate_followpos(index*2)
		if index*2+1 in self.tree:
			self.calculate_followpos(index*2+1)

		if self.tree[index] == '.':
			for i in self.lastpos[index*2]:
				self.followpos[i] = self.followpos[i] | self.firstpos[index*2+1]
		elif self.tree[index] == '*':
			for i in self.lastpos[index]:
				self.followpos[i] = self.followpos[i] | self.firstpos[index]