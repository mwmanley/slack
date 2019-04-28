#!/usr/bin/env python2.7

from cfgmgr.cfgmgr import CfgMgr

if __name__ == "__main__":
    cfg = CfgMgr(config_file="manifest.yaml")
    cfg.run_config()