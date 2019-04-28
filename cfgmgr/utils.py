import signal
import os
from subprocess import CalledProcessError, check_call

class TimeoutError(Exception):
    pass

# quirk of the alarm, I guess
def handler(signum, frame):
    print ("Timeout in command operation")
    raise TimeoutError

class Utils():
    @staticmethod
    def run_command(command):
        rc = False
        DEVNULL = open(os.devnull, 'w')
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(600)
        try:
            check_call(command, stdout=DEVNULL, stderr=DEVNULL)
            rc = True
        except CalledProcessError:
            rc = False
        signal.alarm(0)
        return (rc)