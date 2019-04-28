import os
import hashlib
import sys
from pwd import getpwnam 
from grp import getgrnam
from jinja2 import Template

class FileMgr():

    def update_permissions(self, perms):
        try:
            os.chmod(self.target, int(perms))
        except OSError:
            print("Error updating the permissions for {} to {}".format(self.target,perms))
            return False
        return True

    def update_owner(self, owner=None, group=None):
        uid = -1
        gid = -1
        try:
            if owner is not None:
                uids = getpwnam(owner)
                uid = uids.pw_uid
            if group is not None:
                gids = getgrnam(group)
                gid = gids.gr_gid
            os.chown(self.target, uid, gid)
        except OSError:
            print("Unable to chown object {} to {}:{}".format(self.target,owner,group))
            return False
        return True

    def update_file_from_template(self, template):
        template_data = ()
        target_data = ()
        try:
            with open (template) as in_file:
                template_data = in_file.read()      
        except IOError:
            print("Unable to open template file:  {}".format(template))
            return False
        try:
            if os.path.isfile(self.target):
                with open (self.target) as target_file:
                    target_data = target_file.read()
            else:
                target_data = ""
        except IOError:
            if os.path.isfile(self.target):
                print("Unable to checksum file!")

        t = Template(template_data)
        tmd5 = hashlib.md5(t.render()).hexdigest()
        fmd5 = hashlib.md5(target_data).hexdigest()

        if tmd5 == fmd5:
            pass
        else:
            try:
                with open (self.target, "w") as output_file:
                    output_file.write(t.render())
                # did we change a file?  If so, signal back for
                # any dependent service restarts
                return True
            except IOError:
                print("Unable to write template output to {}".format(self.target))
                return False
        return None

    def remove_file(self):
        try:
            if os.path.isfile(self.target):
                os.unlink(self.target)
        except OSError:
            print ("Error removing file {}".format(self.target))
        return True

    def __init__(self, target=None):
        self.target = target