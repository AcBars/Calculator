from datetime import datetime as dt

def log_decision (decisin):
    time = dt.now().strftime('%d.%m.%Y - %H:%M:%S')
    with open('Calculator\log.cvs', 'a') as file:
        file.write(f'\n {time} - {decisin}')