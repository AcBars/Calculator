import re
from functools import partial

from PyQt6.QtCore import QKeyCombination, Qt
from PyQt6.QtGui import QGuiApplication, QKeyEvent, QKeySequence
from PyQt6.QtWidgets import QGridLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

import calc

BUTTON_HEIGHT = 50
BUTTON_WIDTH = int(BUTTON_HEIGHT * 1.2)
DISPLAY_HEIGHT = BUTTON_HEIGHT * 2
BUTTON_ROWS = 5
# BUTTON_COLS = 6
# WINDOW_WIDTH = int(BUTTON_COLS * BUTTON_WIDTH)
WINDOW_HEIGHT = DISPLAY_HEIGHT + BUTTON_ROWS * BUTTON_HEIGHT


def _find_last_number(expr):
    last_num = ''
    for i, char in enumerate(expr[::-1], start=1):
        if char.isdigit() or char == ',':
            last_num = char + last_num
        elif last_num:
            return -i + 1, last_num

    return 0, last_num or '0'


def _find_all_numbers(expr):
    num_pattern = r'(-?\d*[,.]?\d*)'
    return re.findall(num_pattern, expr)


class CalcPushButton(QPushButton):
    def __init__(self, text, parent=None, objectName=""):
        super(CalcPushButton, self).__init__(text, parent, objectName=objectName)
        self.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)


class MainWindow(QMainWindow):
    def __init__(self, basic=True):
        super().__init__()

        self.basic = basic

        button_cols = 4 if self.basic else 6
        self.window_width = int(button_cols * BUTTON_WIDTH)

        self.setWindowTitle("Calculator")
        self.setFixedSize(self.window_width, WINDOW_HEIGHT)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._create_display()
        main_layout.addWidget(self._display)

        layout = self._create_buttons_layout()
        main_layout.addLayout(layout)

        container = QWidget()
        container.setLayout(main_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        self._set_dark_theme()

    def _create_display(self):
        self._display = QLabel('0')
        self._display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._display.setFixedSize(self.window_width, DISPLAY_HEIGHT)
        self._display.setWordWrap(True)

    def _create_buttons_layout(self):
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self._buttons = {}
        self._create_buttons(self._get_buttons_list(), layout)
        return layout

    def _get_buttons_list(self):
        return [
            [('etc_ac', 'AC'), ('etc_lp', '('), ('etc_rp', ')'), ('op_div', '??')],
            [('num_7', '7'), ('num_8', '8'), ('num_9', '9'), ('op_mult', '??')],
            [('num_4', '4'), ('num_5', '5'), ('num_6', '6'), ('op_minus', '-')],
            [('num_1', '1'), ('num_2', '2'), ('num_3', '3'), ('op_plus', '+')],
            [('num_0', '0'), ('num_comma', ','), ('op_equal', '=')],
        ] if self.basic else [
            [('etc_lp', '('), ('etc_rp', ')'), ('etc_ac', 'AC'),
             ('etc_plusminus', '\u207A\u2044\u208B'), ('etc_percent', '%'), ('op_div', '??')],

            [('etc_pow2', 'x\u00B2'), ('etc_pow_y', 'x\u02B8'), ('num_7', '7'),
             ('num_8', '8'), ('num_9', '9'), ('op_mult', '??')],

            [('etc_2pow_x', '2\u02E3'), ('etc_10pow_x', '10\u02E3'), ('num_4', '4'),
             ('num_5', '5'), ('num_6', '6'), ('op_minus', '-')],

            [('etc_root2', '\u221Ax\u0305'), ('num_1', '1'),
             ('num_2', '2'), ('num_3', '3'), ('op_plus', '+')],

            [('etc_root_y', '\u02B8\u221Ax\u0305'), ('num_0', '0'),
             ('num_comma', ','), ('op_equal', '=')],
        ]

    def _create_buttons(self, buttons_list, layout):
        for row, keys in enumerate(buttons_list):
            shift = 0
            for col, key in enumerate(keys):
                self._buttons[key[0]] = CalcPushButton(key[1], objectName=key[0])
                cur_button = self._buttons[key[0]]
                if key[0] == 'etc_ac':
                    cur_button.clicked.connect(self._clear)
                elif key[0] == 'etc_plusminus':
                    cur_button.clicked.connect(partial(self._calc, self._change_sign))
                elif key[0] == 'op_div':
                    cur_button.clicked.connect(partial(self._calc, self._add_operation, '/'))
                elif key[0] == 'op_mult':
                    cur_button.clicked.connect(partial(self._calc, self._add_operation, '*'))
                elif key[0] in ('etc_percent', 'op_minus', 'op_plus'):
                    cur_button.clicked.connect(partial(self._calc, self._add_operation, key[1]))
                elif key[1].isdigit():
                    cur_button.clicked.connect(partial(self._calc, self._add_number, key[1]))
                elif key[1] == ',':
                    cur_button.clicked.connect(partial(self._calc, self._add_comma))
                elif key[1] == '(':
                    cur_button.clicked.connect(partial(self._calc, self._add_left_par))
                elif key[1] == ')':
                    cur_button.clicked.connect(partial(self._calc, self._add_right_par))
                elif key[1] == '=':
                    cur_button.clicked.connect(partial(self._calc, self._get_result))

                if key[0] in ('num_0', 'etc_root2', 'etc_root_y'):
                    cur_button.setFixedSize(BUTTON_WIDTH * 2, BUTTON_HEIGHT)
                    layout.addWidget(cur_button, row, col + shift, 1, 2)
                    shift += 1
                else:
                    layout.addWidget(cur_button, row, col + shift)

    def _set_dark_theme(self):
        self.setStyleSheet(
            "* {"
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
            f"    font: {BUTTON_HEIGHT // 2 - 2}px"
            "}"
            "QPushButton[objectName^='etc'] {"
            "    border-color: rgb(40, 40, 40);"
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
            "    border-color: rgb(60, 60, 60);"
            "    background-color: rgb(253, 158, 43);"
            "}"
            "QPushButton[objectName^='op']:pressed {"
            "    background-color: rgb(201, 125, 32);"
            "}"
        )

    def _update_font_size(self):
        cur_expr = self._display.text()
        num_len = len(max(_find_all_numbers(cur_expr), key=len))
        self._display.setStyleSheet(
            "QLabel {"
            f"    font: {max(10, BUTTON_HEIGHT // 2 - max(0, (num_len // 12 - 1) * 12 + num_len % 12))}px"
            "}"
        )

    @staticmethod
    def _start(expr):
        return expr in ('0', 'Error')

    def _clear(self):
        if self._start(self._display.text()) or self._buttons['etc_ac'].text() == 'AC':
            self._clear_all()
        else:
            self._clear_one()
            self._buttons['etc_ac'].setText('AC')

        self._update_font_size()

    def _clear_all(self):
        self._display.setText('0')
        self._buttons['etc_ac'].setText('AC')

    def _clear_char(self):
        if self._start(self._display.text()):
            self._clear_all()
            return

        if cur_expr := self._display.text()[:-1]:
            self._display.setText(cur_expr)
            self._update_font_size()
        else:
            self._clear_all()

    def _clear_one(self):
        if self._start(self._display.text()) or self._buttons['etc_ac'].text() == 'AC':
            self._clear_all()
            return

        cur_expr = self._display.text()
        if cur_expr[-1].isdigit() or cur_expr[-1] == ',':
            last_num_idx, _ = _find_last_number(cur_expr)
            cur_expr = cur_expr[:last_num_idx]
        elif cur_expr[-1] == ')':
            cur_expr = cur_expr[:-1]
        else:
            cur_expr = cur_expr[:-2]

        if not cur_expr:
            cur_expr = '0'

        self._display.setText(cur_expr)
        if self._start(cur_expr):
            self._buttons['etc_ac'].setText('AC')
        else:
            self._buttons['etc_ac'].setText('C')

    def _calc(self, func, arg=''):
        if self._start(self._display.text()):
            self._display.setText('0')

        return func(arg) if arg else func()

    def _change_sign(self):
        if self._start(self._display.text()):
            return

        cur_expr = self._display.text()
        last_num_idx, _ = _find_last_number(cur_expr)
        self._display.setText(f'{cur_expr[:last_num_idx]}-{cur_expr[last_num_idx:]}')
        self._buttons['etc_ac'].setText('C')

    def _add_operation(self, op):
        cur_expr = self._display.text()
        if cur_expr[-1] == '(' and op != '-':
            return

        if op == '-' and cur_expr[-1] in ('(', ')'):
            cur_expr += op
        elif cur_expr[-1].isdigit() or cur_expr[-1] in (',', '(', ')'):
            cur_expr += f' {op}'
        else:
            cur_expr = cur_expr[:-1] + op
        self._display.setText(cur_expr)
        self._buttons['etc_ac'].setText('C')

    def _add_number(self, num):
        cur_expr = self._display.text()
        if cur_expr and cur_expr[-1] == ')':
            return

        if self._start(cur_expr):
            cur_expr = num
        else:
            no_space = cur_expr[-1].isdigit() or cur_expr[-1] == ','
            cur_expr += num if no_space else f' {num}'

        self._display.setText(cur_expr)
        self._buttons['etc_ac'].setText('C')
        self._update_font_size()

    def _add_comma(self):
        cur_expr = self._display.text()
        if cur_expr[-1] in (')', ','):
            return

        cur_expr += ',' if cur_expr[-1].isdigit() else '0,'
        self._display.setText(cur_expr)
        self._buttons['etc_ac'].setText('C')

    def _add_left_par(self):
        cur_expr = self._display.text()
        if self._start(cur_expr):
            cur_expr = '('
        elif not cur_expr[-1].isdigit() and cur_expr[-1] not in (')', ','):
            cur_expr = f'{cur_expr} ('
        else:
            return
        self._display.setText(cur_expr)
        self._buttons['etc_ac'].setText('C')

    def _add_right_par(self):
        cur_expr = self._display.text()
        if (cur_expr[-1].isdigit() or cur_expr[-1] in (')', ',')) \
                and cur_expr.count('(') > cur_expr.count(')'):
            cur_expr += ')'
            self._display.setText(cur_expr)
            self._buttons['etc_ac'].setText('C')

    def _get_result(self):
        cur_expr = self._display.text()
        if self._start(cur_expr):
            self._clear_all()
            return

        if not (cur_expr[-1].isdigit() or cur_expr[-1] in (',', ')')):
            _, last_num = _find_last_number(cur_expr)
            cur_expr += f' {last_num}'

        try:
            result = str(round(float(calc.main_calculation(cur_expr)), 6))
        except Exception as e:
            print(e)
            result = 'Error'

        result = result.replace('.', ',').removesuffix(',0')
        self._display.setText(result)
        self._buttons['etc_ac'].setText('AC')
        self._update_font_size()

    @property
    def _key_mappings(self):
        return {
            Qt.Key.Key_Escape: 'etc_ac',
            Qt.Key.Key_Delete: 'etc_ac',
            Qt.Key.Key_ParenLeft: 'etc_lp',
            Qt.Key.Key_ParenRight: 'etc_rp',
            Qt.Key.Key_Percent: 'etc_percent',
            Qt.Key.Key_Slash: 'op_div',
            Qt.Key.Key_Minus: 'op_minus',
            Qt.Key.Key_Plus: 'op_plus',
            Qt.Key.Key_Comma: 'num_comma',
            Qt.Key.Key_Period: 'num_comma',
            Qt.Key.Key_Return: 'op_equal',
            Qt.Key.Key_Enter: 'op_equal'
        }

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.matches(QKeySequence.StandardKey.Paste):
            self._clear_all()
            self._display.setText(QGuiApplication.clipboard().text())
            self._update_font_size()
        elif event.matches(QKeySequence.StandardKey.Copy):
            QGuiApplication.clipboard().setText(self._display.text())
        elif event.keyCombination() == QKeyCombination(Qt.Modifier.ALT, Qt.Key.Key_Escape):
            self._buttons['etc_ac'].setText('AC')
            self._buttons['etc_ac'].animateClick()
        elif event.keyCombination() == QKeyCombination(Qt.Modifier.ALT, Qt.Key.Key_Minus):
            self._buttons['etc_plusminus'].animateClick()
        elif Qt.Key.Key_Asterisk in (event.keyCombination().key(), event.key()):
            self._buttons['op_mult'].animateClick()
        elif event.key() == Qt.Key.Key_Backspace:
            self._clear_char()
        elif event.text() in [str(i) for i in range(10)]:
            self._buttons[f'num_{event.text()}'].animateClick()
        elif btn_name := self._key_mappings.get(event.key()):
            self._buttons[btn_name].animateClick()
