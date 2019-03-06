import os
import ujson

import yaml


class ConfigurationError(Exception):
    pass


MIN_CONFIG_KEYS = ["log", "db"]


def load(defaults, config_location=None, defaults_have_priority=True):
    config_data = defaults
    if os.path.isdir(str(config_location)):
        for root, dirs, files in os.walk(config_location):
            for file in files:
                if file.endswith(".yml") or file.endswith(".yaml"):
                    with open(os.path.join(root, file), mode="r") as configuration_file:
                        config_data = {**yaml.load(configuration_file), **config_data} if defaults_have_priority else {
                            **config_data, **yaml.load(configuration_file)}
    else:
        if config_location is not None and os.path.isfile(str(config_location)):
            with open(config_location, mode="r") as configuration_file:
                config_data = {**yaml.load(configuration_file), **config_data} if defaults_have_priority else {
                    **config_data,  **yaml.load(configuration_file)}

    if type(config_data) != dict:
        raise ConfigurationError("Error in the configuration file '{file}'".format(file=config_location))

    if not set(MIN_CONFIG_KEYS).issubset(set(config_data.keys())):
        raise ConfigurationError("Error in the configuration file '{file}': wrong or missing keys '{keys}'".format(
            file=config_location,
            keys=ujson.dumps(MIN_CONFIG_KEYS)))

    return {key.upper() + "_CONFIG": value for key, value in config_data.items()}
