from datetime import datetime as dt
import getpass

def log_solution (exp, solution):
    time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
    with open('log.csv', 'a') as file:
        file.write(f'\n {time}; calculation; {getpass.getuser()}; {exp}; {solution}')


def log_startend (status):
    if status == 1:
        time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
        with open('log.csv', 'a') as file:
            file.write(f'\n {time}; Start; {getpass.getuser()}')
    else:
        time = dt.now().strftime('%d.%m.%Y ; %H:%M:%S')
        with open('log.csv', 'a') as file:
            file.write(f'\n {time}; End; {getpass.getuser()}')
            

