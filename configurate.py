import os
import subprocess
import sys
import ujson

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
MIN_CONFIG_KEYS = ["log", "db"]


def patch_config(config_file=None):
    if config_file is None or not os.path.isfile(str(config_file)):
        config_data = SETUP_INFO['defaults']
    else:
        with open(config_file, mode="r") as configuration_file:
            config_data = yaml.load(configuration_file)

    if type(config_data) != dict:
        ConfigurationError("Error in the configuration file '{file}'".format(file=config_file))

    if not set(MIN_CONFIG_KEYS).issubset(set(config_data.keys())):
        ConfigurationError("Error in the configuration file '{file}': wrong keys".format(file=config_file))

    with open(PKG_FILE, mode="w") as config_definition:
        config_definition.writelines(
            ["\n", "DB_CONFIG = {db_config}".format(db_config=ujson.dumps(config_data["db"])), "\n",
             "LOG_CONFIG = {log_config}".format(log_config=ujson.dumps(config_data["log"])), "\n", ])


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
