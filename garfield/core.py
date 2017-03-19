import os
import sys
import json
import logging
import argparse
import tornado.log

import config

from lib import file_utils

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PLUGINS_DIR = os.path.join(BASE_DIR, config.PLUGINS_DIR_NAME)


class Core(object):

    """Object responsible for parsing parameters and supplying
    them to the corresponding plugins"""

    def __init__(self):
        """TODO: to be defined1. """
        self._init_logging()
        self._init_arg_parser()

        self._load_plugins()

    def _load_plugins(self):
        """Walk for plugin info files and update argument parser
        with the found details"""
        self._plugins = {}
        logging.debug("Loading plugins from %s" % (PLUGINS_DIR))
        for root, dirs, files in os.walk(PLUGINS_DIR):
            if len(dirs) > 0:
                logging.debug("Following plugin info found")
            for d in dirs:
                plugin_json_file = os.path.join(PLUGINS_DIR, d, config.PLUGIN_JSON_FILE_NAME)
                # Check if plugin.json exists
                if os.path.isfile(plugin_json_file):
                    logging.debug("\t%s" % (plugin_json_file))
                    try:
                        # Load plugin json file
                        with open(plugin_json_file, 'r') as f:
                            module_props = json.load(f)
                        # Save module props
                        self._plugins[module_props["identifier"]] = [plugin_json_file, module_props]
                        sub_parser = self.arg_subparsers.add_parser(
                            module_props["identifier"],
                            help=module_props["help"])
                        plugin = file_utils.get_plugin(*self._plugins[module_props["identifier"]])
                        sub_parser = plugin.update_arg_parser(sub_parser)
                    except ValueError:  # Catch incorrect plugin json
                        logging.exception("JSON decoding of plugin file failed: %s" % (plugin_json_file))

    def _init_arg_parser(self):
        # Create root arg parser and its attributes
        self.arg_parser = argparse.ArgumentParser(
            prog="Garfield",
            description="A framework for fingerprinting, enumerating and exploiting distributed systems")
        self.arg_parser.add_argument("-v", "--verbose", dest="verbose", action="store_true",
                                     default=False, help="Log debug messages as well")
        self.arg_parser.add_argument("--ip", dest="ip", help="Address of the target")
        self.arg_parser.add_argument("--port", dest="port", help="Port of the target")

        self.arg_subparsers = self.arg_parser.add_subparsers(title="plugin", dest="plugin",
                                                             help="Different plugins that are supported")

    def _init_logging(self):
        # Get root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(tornado.log.LogFormatter(
            fmt='%(color)s[%(asctime)s] %(message)s%(end_color)s',
            datefmt="%H:%M"))

        logger.handlers = [stream_handler]

    def run(self):
        # First parse the arguments
        args = self.arg_parser.parse_args()

        if args.verbose is True:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)

        if args.plugin is not None:
            plugin = file_utils.get_plugin(*self._plugins[args.plugin])
            plugin.run(args)


def print_banner():
    print("""
   _____             __ _      _     _
  / ____|           / _(_)    | |   | |
 | |  __  __ _ _ __| |_ _  ___| | __| |
 | | |_ |/ _` | '__|  _| |/ _ \ |/ _` |
 | |__| | (_| | |  | | | |  __/ | (_| |
  \_____|\__,_|_|  |_| |_|\___|_|\__,_| v%0.2f
   -= Distributed System Pwning Cat =-
      -= It's all about ME-OW! =-
    -= @torque59 & @tunnelshade =-
    """ % (config.VERSION))


if __name__ == "__main__":
    print_banner()
    core = Core()
    core.run()
