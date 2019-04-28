# Rudimentary configuration management

These scripts handle configuration management for Debian-based systems.  Before running, use the **bootstrap.sh** script to make sure that Python and its required modules are installed.  The script also installs the zsh to demonstrate package removal.

# Layout

All the Python classes that drive this tool are in the cfgmgr directory.  The Cfgmgr class should do what you want and it's only necessary to instatiate an object of that type, feeding it a YAML file, then execute it by running a __run_config_ against the class object.

The _run_cfg.py_ file has this class all ready to go, so run this script to invoke the configuration manager.  It's taking the manifest.yaml file as its configuration file.

# Configuration

The configuration file is in the YAML format for easier readability.  Each object has a name declaration, then a series of configuration options for that object.  Dependencies on other objects are honored by declaring the object on which the object depends.  For instance:

package_1:
  packages 
    install:
    - package1

package_1_config:
  files:
    file: /etc/package.cfg
    owner: root
  depends:
  - package_1
  service:
  - package_service: restart

package_1_service:
  service:
  - package_service: start

Those stanzas will install package one, then restart (or start for the first time) it with a configuration file.  Should the configuration file template change, the service will also restart.  The service stanza should keep the service running.  

# Depends declarations

All the following stanzas support the _depends_ declaration to establish dependencies between stanzas, creating better predictability.  

# Packages stanzas
Package declarations include:

1. _install_ declarations.  Itemize a list of packages under it.
1. _remove_ declarations.  Itemize a list of packages to remove under it.

# Files stanzas

Files declarations include:

1. _file_ declarations.  This name is for the target file.
1. _template_ declarations.  These files run through the Jinja2 Python templating engine.
1. _owner_ declarations.  These are for the POSIX usernames such as "root".
1. _group_ declartions.  These are for the POSIX groups as such as "wheel."
1. _perms_ declarations.  Use the Unix octal notation, such as 644 for write/read/read for owner/group/other.
1. _delete_ declarations.  For when you really want that file deleted.

# Service stanzas

1. _service_ declarations.  The service declarations pass directly to the **service** system command, so use stop, start, or restart.

# Other notes

System calls to install packages or restart services have a ten minute timeout.  If operations fail to meet that timeout, the script kills the executing operation.  Be aware that killing package installations can adversely affect the Debian packaging system by leaving lock files behind.

