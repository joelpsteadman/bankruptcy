from datetime import datetime, timedelta
import os

def dollarValueOf(number):
    s = "$" + str(round(number, 2 ))
    return s

class Logger:
    def __init__(self):
        self.start_time = datetime.now()
        print('\n0:00:00.00 - Starting Application')

    def format(self, args, delimiter=' '):
        delta_time = datetime.now() - self.start_time
        output = '{0: <10}'.format(str(delta_time)[0:10]) + ' -'
        for s in args:
            output += delimiter
            if isinstance(s, str):
                output += s
            else:
                output += str(s)
        return output

    def log(self, *args, erase=False, delimiter=' '):
        output = self.format(args, delimiter)
        if erase:
            output += '                      '
            print(output, end="\r")
        else:
            print(output)

    def define_issue_log(self, file_path, overwrite=False):
        self.issue_log = file_path
        if overwrite:
            with open(file_path, 'w') as file:
                file.write('')

    def record_issue(self, *args, erase=False, delimiter=' '):
        with open(self.issue_log, 'a') as file:
            output = self.format(args, delimiter) + '\n'
            file.write(output)