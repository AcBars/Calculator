import re

def expression_in_brackets(expression):
    # выделяет блоки от открывающей до закрывающей круглой скобки
    # вложенные в том числе
    pattern = re.compile(r"\([^(^)]+\)")
    m = pattern.findall(expression)
    x = expression
    while m != []:
        for i in m:
            # print(f'i: {i}->',end='')
            x = calc_in_brackets(x, i)
        m = pattern.findall(x)
    return x


def calc_in_brackets(full_expression, expression):
    pattern = re.compile(r"[-|+]*[0-9]+")
    m = pattern.findall(expression)
    sum = 0
    for i in m:
        sum += int(i)
    # print(sum)
    full_expression = str(full_expression).replace(expression, str(sum))
    return full_expression

def multiplicate(full_expression):
    pattern = re.compile(r"[\.0-9]+\*[\.0-9]+") # не работает для вещественных чисел
    m = pattern.findall(full_expression)
    while m != []:
        for i in m:
            pos = str(i).find('*')
            # print("pos:"+str(i)[:pos])
            # print("pos:"+str(i)[pos+1:])
            value = float(str(i)[:pos])*float(str(i)[pos+1:])
        full_expression = str(full_expression).replace(i, str(value))
        m = pattern.findall(full_expression)
    # print(full_expression)
    return full_expression

def devide(full_expression):
    pattern = re.compile(r"[\.0-9]+\/[\.0-9]+")
    m = pattern.findall(full_expression)
    while m != []:
        for i in m:
            pos = str(i).find('/')
            if (str(i)[pos+1:]) != '0':
                value = float(str(i)[:pos])/float(str(i)[pos+1:])
            else:
                print('деление на ноль недопустимо!')
        full_expression = str(full_expression).replace(i, str(value))
        m = pattern.findall(full_expression)
    # print(full_expression)
    return full_expression

def plus_minus(full_expression):
    pattern = re.compile(r"[-|+]*[\.0-9]+")
    m = pattern.findall(full_expression)
    sum = float(0)
    for i in m:
        sum += float(i)
        full_expression = str(sum)
    return full_expression

calc_str = '((1+2)+3)*2*2/(3+9)+(12+13)'
calc_str = input('введите строку для расчета:')
calc_str = calc_str.replace(" ", '')
#print(f'\n\nисходное выражение: {calc_str}')

calc_str = multiplicate(calc_str)
# print(f'multiplicate: {calc_str}')
calc_str = devide(calc_str)
# print(f'devide: {calc_str}')
calc_str = expression_in_brackets(calc_str)
# print(f'expression_in_brackets: {calc_str}')

calc_str = multiplicate(calc_str)
# print(f'multiplicate: {calc_str}')

calc_str = devide(calc_str)
# print(f'devide: {calc_str}')

calc_str = plus_minus(calc_str)
# print(f'plus_minus: {calc_str}')

print(float(calc_str))

