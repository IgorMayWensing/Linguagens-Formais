from PyQt5 import Qt

class Interface(Qt.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()
        self.resize(900,600)
        self.setStyleSheet("background-color: #FFCCE5;")
        self.widget = Qt.QWidget(self)
        self.editor = Qt.QTextEdit()
        self.secondary_editor = Qt.QTextEdit()
        self.layout = Qt.QGridLayout()
        self.layout.addWidget(self.editor, 1, 300, 1, 2)
        self.layout.addWidget(self.secondary_editor, 2, 300, 1, 2)
        self.editor.setText('Input principal')
        self.secondary_editor.setText('Input para realizar a união de autômatos')
        self.widget.setLayout(self.layout)

        self.create_buttons()

        self.setCentralWidget(self.widget)

    def create_buttons(self):

        self.comboAction = Qt.QComboBox(self)
        self.comboAction.addItem("Converter")
        self.comboAction.addItem("União")
        self.comboAction.addItem("Determinizar")
        self.comboAction.move(10, 50)
        self.comboAction.setFixedWidth(150)

        self.comboFrom = Qt.QComboBox(self)
        self.comboFrom.addItem("Expressão regular")
        self.comboFrom.addItem("Autômato Finito")
        self.comboFrom.move(10, 100)
        self.comboFrom.setFixedWidth(150)

        self.comboTo = Qt.QComboBox(self)
        self.comboTo.addItem("Expressão regular")
        self.comboTo.addItem("Autômato Finito")
        self.comboTo.move(10, 150)
        self.comboTo.setFixedWidth(150)


        self.ok_button = Qt.QPushButton('OK')
        self.layout.addWidget(self.ok_button, 2, 0)