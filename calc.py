import re

''' расчет производится в функции main_calculation(full_expression) '''
def main_calculation(full_expression):
    full_expression = prepare_expression(full_expression)
    pattern = re.compile(r"\([-+ *\/.\d\s]+\)")
    m = pattern.search(full_expression)
    if not m:
        full_expression = calculate_mul_div(full_expression)
        # addition
        full_expression = calculate_sum_sub(full_expression)
        return full_expression

    while m:
        value = calculate_mul_div(full_expression[m.start():m.end()])
        if float(value) > 0:
            full_expression = full_expression[:m.start()] + "+" + value + full_expression[m.end():]
        else:
            full_expression = full_expression[:m.start()] + value + full_expression[m.end():]
        m = pattern.search(full_expression)
    # addition
    full_expression = calculate_sum_sub(full_expression)
    return full_expression


def prepare_expression(expression):
    full_expression = expression.replace(" ", '')
    full_expression = full_expression.replace(",", '.')
    ''' проверка, три знака подряд - ошибка '''
    pattern = re.compile(r"[-+*\/]{3,}")
    m = pattern.findall(full_expression)
    if m:
        return 'NaN'
    ''' конец проверки '''
    return full_expression


def check_val_and_make_exp(full_expression, m, value):
    if float(value) > 0:
        full_expression = full_expression[:m.start()] + "+" + str(value) + full_expression[m.end():]
    else:
        full_expression = full_expression[:m.start()] + str(value) + full_expression[m.end():]
    return full_expression


def calculate_mul_div(full_expression):
    full_expression = full_expression.replace(")", '')
    full_expression = full_expression.replace("(", '')

    m = re.search(r'[-+ *\ /][*\ /]', full_expression)
    if m:
        print('Недопустимая компбинация операций')
        return 'NaN'

    m = re.search(r"[-+]?[0-9.]+[*\/][-+]?[0-9.]+", full_expression)
    # dividing
    while m:
        mm = re.search(r'/', m[0])
        if mm:
            d = full_expression[m.start():m.end()]
            if (d[mm.end():]) != '0':
                value = float(d[:mm.start()]) / float(d[mm.end():])
                full_expression = check_val_and_make_exp(full_expression, m, value)
            else:
                print('ошибка = деление на ноль')
                return 'NaN'

        m = re.search(r"[-+]?[0-9.]+[*\/][-+]?[0-9.]+", full_expression)
        # multiplication
        if m:
            mm = re.search(r'\*', m[0])
            if mm:
                d = full_expression[m.start():m.end()]
                value = float(d[:mm.start()]) * float(d[mm.end():])
                full_expression = check_val_and_make_exp(full_expression, m, value)
    # addition
    full_expression = calculate_sum_sub(full_expression)
    return full_expression


def calculate_sum_sub(full_expression):
    m = re.findall(r"[-+]?[0-9.]+", full_expression)
    if m:
        s = m.copy()
    else:
        return full_expression
    # addition
    value = 0
    for i in s:
        value += float(i)
    return str(value)

# expression = '(49+(20*-25*4,0/(-3-7/7))'
# print(f'expression : {expression}')
# result = main_calculation(expression)
# print(f'result: {result}')
