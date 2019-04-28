import os
import yaml
import sys
import signal
import subprocess

from package_mgr import PackageMgr
from file_mgr import FileMgr
from service_mgr import ServiceMgr
    

class CfgMgr():
    # here is the meat of our coordination.  We load YAML
    # declarations for packages, files, templates, and services

    def load_config(self):
        try:
            with open (self.config_file) as cf:
                self.config = yaml.load(cf)
        except OSError:
            print("Unable to load a configuration.  Aborting")
            sys.exit(1)

    def handle_file(self, obj):
        # freebie for having a file object
        successes = 1
        file_changed = False
        if "file" not in obj:
            print("No target file specified in block.  Bailing.")
            sys.exit(1)
        obj_file = FileMgr(obj['file'])
        if "delete" in obj:
            if obj_file.remove_file():
                successes += 1
        if "template" in obj:
            file_changed = obj_file.update_file_from_template(obj["template"])
            if file_changed != False:
                successes += 1
        if os.path.isfile(obj['file']):
            if "perms" in obj:
                if obj_file.update_permissions(obj["perms"]):
                    successes += 1
            if "owner" in obj and "group" in obj:
                if obj_file.update_owner(owner=obj["owner"],group=obj["group"]):
                    successes += 2
            elif "owner" in obj:
                if obj_file.update_owner(owner=obj["owner"]):
                    successes += 1
            elif "group" in obj:
                if obj_file.update_owner(owner=obj["group"]):
                    successes += 1
        if successes == len(obj):
            if file_changed:
                return file_changed
            else:
                return None

    def handle_package(self, obj):
        successes = 0
        p = PackageMgr()
        if "install" in obj:
            pkgs = obj["install"]
            numpkgs = 0
            for pkg in pkgs:
                if p.install_package(pkg):
                    numpkgs += 1
            if numpkgs == len(pkgs):
                successes += 1
        if "remove" in obj:
            pkgs = obj["remove"]
            numpkgs = 0
            for pkg in pkgs:
                if p.remove_package(pkg):
                    numpkgs += 1
            if numpkgs == len(pkgs):
                successes += 1
        return (successes == len(obj))

    def handle_service(self, services, file_changed):
        for svc in services:
            for service, state in svc.iteritems():
                if state != "restart" or file_changed == True:
                    s = ServiceMgr(service)
                    return s.service_action(state)
            
    def run_config(self):
        self.load_config()
        loop = 0
        items = len(self.config)
        while loop < 4:
            file_changed = False
            if items == len (self.completed):
                break
            for config_obj in self.config.keys():
                obj = self.config[config_obj]
                if config_obj in self.completed:
                    continue
                if "depends" in obj:
                    deps_satisfied = 0
                    # have we satisfied our deps
                    for deps in obj["depends"]:
                        if deps not in self.completed:
                            print("Deferring on:  {} for {}".format((deps),config_obj))
                        else:
                            deps_satisfied += 1
                    if deps_satisfied != len(obj["depends"]):
                        continue
                if "files" in obj:
                    print("Handling files:  {}".format(config_obj))
                    file_changed = self.handle_file(obj["files"]) 
                    if file_changed != False:
                        self.completed.append(config_obj)
                if "packages" in obj:
                    print("Handling packages:  {}".format(config_obj))
                    if self.handle_package(obj["packages"]):
                        self.completed.append(config_obj)
                if "service" in obj:
                    print("Handling service: {}".format(config_obj))
                    self.handle_service(obj["service"], file_changed)
            loop += 1

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.completed = []
        self.config = {}
