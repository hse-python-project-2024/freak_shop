import os
import json
import logging
import logging.config

FOLDER_LOG = "server/logs"
LOGGING_CONFIG_FILE = 'server/logs/loggers.json'


def create_log_folder(folder=FOLDER_LOG):
    if not os.path.exists(folder):
        os.mkdir(folder)


def get_logger(name, template='default'):
    create_log_folder()
    with open(LOGGING_CONFIG_FILE, "r") as f:
        dict_config = json.load(f)
        dict_config["loggers"][name] = dict_config["loggers"][template]
    logging.config.dictConfig(dict_config)
    return logging.getLogger(name)


def get_default_logger():
    create_log_folder()
    with open(LOGGING_CONFIG_FILE, "r") as f:
        logging.config.dictConfig(json.load(f))

    return logging.getLogger("default")
