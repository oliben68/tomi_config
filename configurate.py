import os
import subprocess
import sys
import json

import yaml


class ConfigurationError(Exception):
    pass


min_version = "37"
if int(str(sys.version_info.major) + str(sys.version_info.minor)) < int(min_version):
    print("Minimum version supported is {ver}".format(ver=".".join([c for c in min_version])))
    sys.exit(-1)


def load_setup_info():
    with open(os.path.join(os.getcwd(), ".setup_info")) as pkg_info:
        return yaml.load(pkg_info)


SETUP_INFO = load_setup_info()
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
PKG_FILE = os.path.join(CURRENT_DIR, SETUP_INFO["package"]["name"], "__init__.py")


def patch_config(config_location=None):
    """

    :param config_location:
    :return:
    """
    with open(PKG_FILE, mode="w") as config_definition:
        config_definition.write("""import sys

from tomi_config.load_configuration import load


min_version = "37"


if int(str(sys.version_info.major) + str(sys.version_info.minor)) < int(min_version):
    print("Minimum version supported is {{ver}}".format(ver=".".join([c for c in min_version])))
    sys.exit(-1)

   
class Config(object):
    def __init__(self, setup_info, config_location=None):
        self._setup_info = setup_info
        self._config_location = config_location

    def __getattr__(self, attr):
        configs = load(self._setup_info, config_location=self._config_location)
        
        if attr not in configs.keys():
            raise AttributeError(attr)
        
        return configs[attr]


CONFIG=Config( {setup_info}, "{config_location}")

""".format(setup_info=json.dumps(SETUP_INFO["defaults"], separators=(',', ':')), config_location=config_location))


def run_setup():
    install_proc = subprocess.Popen(
        [sys.executable, os.path.join(CURRENT_DIR, "config_setup.py"), "install", "--force"],
        stdout=subprocess.PIPE)
    for line in install_proc.communicate():
        if line is not None:
            print(line.decode())


if __name__ == '__main__':
    patch_config(sys.argv[1] if len(sys.argv) > 1 else None)
    run_setup()
    os.remove(PKG_FILE)
