
from datetime import datetime, timedelta 
def dollarValueOf(number):
    s = "$" + str(round(number, 2 ))
    return s

class Logger:
    def __init__:
        self.start_time = datetime.now()
    def log(self, *args, erase=False):
        delta_time = datetime.now() - self.start_time
        output = '{0: <10}'.format(str(delta_time))
        for s in args:
            if isinstance(s, str):
                output += s
            else:
                output += str(s)
        if erase:
            print (output, end="\r")
        else:
            print(output)
