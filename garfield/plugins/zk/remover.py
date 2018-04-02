import os
import re
import logging

from garfield.lib import file_utils
from .ZKNode import ZKNode

try:
    from kazoo.client import KazooClient
    from kazoo.exceptions import NoAuthError
except ImportError:
    KazooClient = None


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper loading as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Deleting node tree starting from %s" % (args.node))
            logging.info("Press Enter to continue")
            raw_input()
            zk.delete(args.node, recursive=True)
            logging.info("Deleting finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
