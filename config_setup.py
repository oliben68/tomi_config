import os
import sys

import yaml
from setuptools import find_packages
from setuptools import setup


class ConfigurationError(Exception):
    pass


min_version = "37"
if int(str(sys.version_info.major) + str(sys.version_info.minor)) < int(min_version):
    raise ConfigurationError("Minimum version supported is {ver}".format(ver=".".join([c for c in min_version])))


def load_setup_info():
    with open(os.path.join(os.getcwd(), ".setup_info")) as pkg_info:
        return yaml.load(pkg_info)


SETUP_INFO = load_setup_info()

setup(
    name=SETUP_INFO["package"]["name"],
    version=SETUP_INFO["package"]["version"],
    packages=find_packages(),
    url='',
    license='',
    author='Olivier Steck',
    author_email='osteck@gmail.com',
    description='TBD',
    install_requires=[],
)
