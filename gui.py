from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

BUTTON_HEIGHT = 50
BUTTON_WIDTH = int(BUTTON_HEIGHT * 1.2)
BUTTON_ROWS = 5
BUTTON_COLS = 4
DISPLAY_HEIGHT = BUTTON_HEIGHT * 2
WINDOW_WIDTH = int(BUTTON_COLS * BUTTON_WIDTH)
WINDOW_HEIGHT = DISPLAY_HEIGHT + BUTTON_ROWS * BUTTON_HEIGHT


def _find_last_number(expr):
    last_num = ''
    for i, char in enumerate(expr[::-1], start=1):
        if char.isdigit() or char == ',':
            last_num = char + last_num
        elif last_num:
            return -i, last_num

    return 0, last_num if last_num else '0'


class CalcPushButton(QPushButton):
    def __init__(self, text, parent=None, objectName=""):
        super(CalcPushButton, self).__init__(text, parent, objectName=objectName)
        self.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.display = QLabel('0')
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedSize(WINDOW_WIDTH, DISPLAY_HEIGHT)
        self.display.setWordWrap(True)

        main_layout.addWidget(self.display)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.buttons = {}

        button_list = [
            [('etc_ac', 'AC'), ('etc_plusminus', '+/-'), ('etc_percent', '%'), ('op_div', '÷')],
            [('num_7', '7'), ('num_8', '8'), ('num_9', '9'), ('op_mult', '×')],
            [('num_4', '4'), ('num_5', '5'), ('num_6', '6'), ('op_minus', '-')],
            [('num_1', '1'), ('num_2', '2'), ('num_3', '3'), ('op_plus', '+')],
            [('num_0', '0'), ('num_comma', ','), ('op_equal', '=')],
        ]

        zero_button = False
        for row, keys in enumerate(button_list):
            for col, key in enumerate(keys):
                self.buttons[key[0]] = CalcPushButton(key[1], objectName=key[0])
                cur_button = self.buttons[key[0]]
                if key[0] == 'etc_ac':
                    cur_button.clicked.connect(self.clear)
                elif key[0] == 'etc_plusminus':
                    cur_button.clicked.connect(self.change_sign)
                elif key[0] == 'op_div':
                    cur_button.clicked.connect(partial(self.add_operation, '/'))
                elif key[0] == 'op_mult':
                    cur_button.clicked.connect(partial(self.add_operation, '*'))
                elif key[0] in ('etc_percent', 'op_minus', 'op_plus'):
                    cur_button.clicked.connect(partial(self.add_operation, key[1]))
                elif key[1].isdigit():
                    cur_button.clicked.connect(partial(self.add_number, key[1]))
                elif key[1] == ',':
                    cur_button.clicked.connect(self.add_comma)
                elif key[1] == '=':
                    cur_button.clicked.connect(self.get_result)

                if key[1] == '0':
                    zero_button = True
                    cur_button.setFixedSize(BUTTON_WIDTH * 2, BUTTON_HEIGHT)
                    layout.addWidget(cur_button, row, col, 1, 2)
                elif zero_button:
                    layout.addWidget(cur_button, row, col + 1)
                else:
                    layout.addWidget(cur_button, row, col)

        main_layout.addLayout(layout)

        container = QWidget()
        container.setLayout(main_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        self.set_dark_theme()

    def set_dark_theme(self):
        self.setStyleSheet("* {"
                           "    color: white;"
                           "}"
                           "QLabel {"
                           "    background-color: rgb(50, 50, 50);"
                           "    padding: 5px;"
                           f"    font: {BUTTON_HEIGHT // 2}px"
                           "}"
                           "QPushButton {"
                           "    border-top: 1px solid;"
                           "    border-left: 1px solid;"
                           "    border-style: outset;"
                           "    border-color: rgb(50, 50, 50);"
                           "    font: 20px"
                           "}"
                           "QPushButton[objectName^='etc'] {"
                           "    background-color: rgb(70, 70, 70);"
                           "}"
                           "QPushButton[objectName^='etc']:pressed {"
                           "    background-color: rgb(100, 100, 100);"
                           "    border-style: inset;"
                           "}"
                           "QPushButton[objectName^='num'] {"
                           "    background-color: rgb(100, 100, 100);"
                           "}"
                           "QPushButton[objectName^='num']:pressed {"
                           "    background-color: rgb(160, 160, 160);"
                           "    border-style: inset;"
                           "}"
                           "QPushButton[objectName^='op'] {"
                           "    background-color: rgb(253, 158, 43);"
                           "}"
                           "QPushButton[objectName^='op']:pressed {"
                           "    background-color: rgb(201, 125, 32);"
                           "}"
                           "")

    def clear(self):
        if self.buttons['etc_ac'].text() == 'C':
            cur_expr = self.display.text()
            if cur_expr[-1].isdigit() or cur_expr[-1] == ',':
                last_num_idx, _ = _find_last_number(cur_expr)
                cur_expr = cur_expr[:last_num_idx]
            else:
                cur_expr = cur_expr[:-2]

            self.display.setText(cur_expr)
            self.buttons['etc_ac'].setText('AC')
        else:
            self.display.setText('0')

    def change_sign(self):
        self.buttons['etc_ac'].setText('C')
        cur_expr = self.display.text()
        last_num_idx, _ = _find_last_number(cur_expr)
        self.display.setText(cur_expr[:last_num_idx] + '-' + cur_expr[last_num_idx:])

    def add_operation(self, op):
        self.buttons['etc_ac'].setText('C')
        cur_expr = self.display.text()
        if cur_expr[-1].isdigit() or cur_expr[-1] == ',':
            cur_expr += ' ' + op
        else:
            cur_expr = cur_expr[:-1] + op
        self.display.setText(cur_expr)

    def add_number(self, num):
        self.buttons['etc_ac'].setText('C')
        cur_expr = self.display.text()
        if cur_expr == '0':
            cur_expr = num
        else:
            no_space = cur_expr[-1].isdigit() or cur_expr[-1] == ','
            cur_expr += num if no_space else ' ' + num
        self.display.setText(cur_expr)

    def add_comma(self):
        self.buttons['etc_ac'].setText('C')
        cur_expr = self.display.text()
        if cur_expr[-1] == ',':
            return
        cur_expr += ',' if cur_expr[-1].isdigit() else '0,'
        self.display.setText(cur_expr)

    def get_result(self):
        self.buttons['etc_ac'].setText('AC')
        cur_expr = self.display.text()
        if not (cur_expr[-1].isdigit() or cur_expr[-1] == ','):
            _, last_num = _find_last_number(cur_expr)
            cur_expr += ' ' + last_num

        # self.display.setText(calc.expression_in_brackets(cur_expr))
        self.display.setText(cur_expr + ' =')
