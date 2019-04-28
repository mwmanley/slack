import subprocess
import time
import signal
from utils import Utils, TimeoutError

class ServiceMgr():

    def check_if_service_running(self):
        try:
            cmd = ["service", self.service, "status"]
            return Utils.run_command(cmd)
        except TimeoutError:
            print ("Warning!  Command timeout!")
        except OSError:
            print ("Warning!  Command failure!")

    def service_action(self, action):
        try:
            cmd = ["service", self.service, action]
            return Utils.run_command(cmd)
        except TimeoutError:
            print ("Warning!  Command timeout!")
        except OSError:
            print ("Warning!  Command failure!")

    def __init__(self,service=None):
        self.service = service
