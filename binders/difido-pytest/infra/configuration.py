# Created on Aug 10, 2017
#
# @author: Itai Agmon


import os
import configparser
import sys
from shutil import copyfile
from configparser import NoOptionError

from definitions import root_dir

CONF_FILE_NAME = "difido.cfg"


class Conf:

    def __init__(self, section):
        self.config_file = os.path.join(root_dir, CONF_FILE_NAME)

        if "--config-file" in sys.argv:
            self.config_file = sys.argv[sys.argv.index("--config-file") + 1]
        if not os.path.isfile(self.config_file):
            self.create_config_file()
        self.section = section
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)

    def create_config_file(self):
        template = os.path.join(root_dir, "resources", CONF_FILE_NAME)
        copyfile(template, self.config_file)

    def get_string(self, option):
        try:
            return self.parser.get(self.section, option).strip()
        except NoOptionError:
            return ""

    def get_int(self, option):
        try:
            return self.parser.getint(self.section, option)
        except NoOptionError:
            return 0

    def get_float(self, option):
        try:
            return self.parser.getboolean(self.section, option)
        except NoOptionError:
            return 0.0

    def get_list(self, option):
        try:
            return self.get_string(option).split(';')
        except Exception:
            return []

    def get_dict(self, option):
        d = {}
        try:
            value = self.get_string(option)
        except NoOptionError:
            return {}
        if value is None:
            return d
        if len(value.split(";")) == 0:
            return d
        for keyval in value.split(";"):
            if len(keyval.split("=")) < 2:
                continue
            d[keyval.split('=')[0]] = keyval.split('=')[1]
        return d
