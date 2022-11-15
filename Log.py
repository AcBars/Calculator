from datetime import datetime as dt

def log_decision (exp, decisin):
    time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    with open('Calculator\log.csv', 'a') as file:
        file.write(f'\n {time}; {exp}; {decisin}')


def log_startend (status):
    if status == 1:
        time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
        with open('Calculator\log.csv', 'a') as file:
            file.write(f'\n {time}; Start')
    else:
        time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
        with open('Calculator\log.csv', 'a') as file:
            file.write(f'\n {time}; End')