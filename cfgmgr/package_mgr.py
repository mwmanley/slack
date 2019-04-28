import subprocess
import time
import signal
from utils import Utils, TimeoutError

class PackageMgr():

    def check_if_installed(self, pkg):
        # are we there already.  Since 0 is true and 1 is false, we will have
        # to inverse these
        cmd = ["dpkg", "--list", pkg]
        return Utils.run_command(cmd)

    def refresh_apt_cache(self):
        # We'll refresh our cache if a time interval passes since our last run or
        # we have not yet run
        if self.last_refresh < time.time() - self.refresh_interval:
            return False
        cmd = ["apt", "update"]
        return Utils.run_command(cmd)

    def install_package(self, pkg):
        # install.  If we are already installed, then yay
        # some packages require input, so we'll have to stick a timeout
        if self.check_if_installed(pkg) == True:
            return True
        self.refresh_apt_cache()
        try:
            cmd = ["apt-get", "-y", "install", pkg]
            return Utils.run_command(cmd)
        except TimeoutError:
            print ("Warning!  Package installation timeout!")
        except OSError:
            print ("Warning!  Package installation failure!")

    def remove_package(self, pkg):
        # install.  If we are already installed, then yay
        # some packages require input, so we'll have to stick a timeout
        if self.check_if_installed(pkg) == True:
            return True
        try:
            cmd = ["apt-get", "-y", "remove", pkg]
            return Utils.run_command(cmd)
        except TimeoutError:
            print ("Warning!  Package removal timeout!")
        except OSError:
            print ("Warning!  Package installation failure!")
       
    def __init__(self):
        self.last_refresh = 0
        self.refresh_interval = 3600