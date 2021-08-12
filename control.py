import sys
from interface import *
import algorithms

class Control():
    def __init__(self):
        app = Qt.QApplication([])
        self.create_interface()
        self.interface.show() 
        self.interface.raise_()
        sys.exit(app.exec_())

    def create_interface(self):
        self.interface = Interface() 
        self.bind_buttons()

    def bind_buttons(self):
        self.interface.ok_button.clicked.connect(self.call_convertion)
        
    def call_convertion(self):
        if self.interface.comboAction.currentText() == "Determinizar":
            self.determinize_automata()
        elif (self.interface.comboFrom.currentText() == "Expressão regular") and (self.interface.comboTo.currentText() == "Autômato Finito"):
            self.regular_expression_to_fsm()
        elif self.interface.comboAction.currentText() == "União":
            self.unite_automata()

    def unite_automata(self):
        automata_1 = self.read_automata(self.interface.editor)
        automata_2 = self.read_automata(self.interface.secondary_editor)
        automata = algorithms.unite_automata(automata_1, automata_2)
        self.interface.editor.setText(str(automata)[:-1])

    def regular_expression_to_fsm(self):
        expression = self.interface.editor.toPlainText()
        fsm = algorithms.regular_expression_to_fsm(expression)
        self.interface.editor.setText(str(fsm)[:-1])

    def read_automata(self, editor):
        content = editor.toPlainText()
        content = content.split('\n')
        states = content[0].split()
        alphabet = content[1].split()
        initial_state = content[2]
        final_states = content[3].split()

        transitions = {}
        for state in states:
            transitions[state] = {}
            for symbol in alphabet:
                transitions[state][symbol] = []
            transitions[state]['&'] = []
        for transition in content[4:]:
            t = transition.split()
            source = t[0]
            destiny = t[2]
            symbol = t[3]
            transitions[source][symbol].append(destiny)

        automata = algorithms.Automata(states, alphabet, initial_state, final_states, transitions)
        return automata

    def determinize_automata(self):
        automata = self.read_automata(self.interface.editor)
        determinized_automata = algorithms.determinize_automata(automata)
        self.interface.editor.setText(str(determinized_automata)[:-1])