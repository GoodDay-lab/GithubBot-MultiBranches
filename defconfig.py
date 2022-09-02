from mylogger import mylogger
import itertools

def load_defconfig():
    config = {
            "repository": "/var/localrepository",
            "host": "127.0.0.1",
            "port": 9000,
            "branch": ""
            }
    mylogger.info("Loaded defconfig:\n"
                  "%s" % str(config))
    return config

def create_config(config):
    """
      Compares defconfig and custom config and
    create a full config on both of them.
    param: custom config
    """
    defconfig = load_defconfig()
    for dkey in defconfig.keys():
        if (dkey not in config):
            config[dkey] = defconfig[dkey]
    mylogger.info("Created new config:\n"
                  "%s" % str(config))
    return config

