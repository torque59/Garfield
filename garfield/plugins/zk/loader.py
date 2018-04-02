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


def set_data(zk, node):
    zk.ensure_path(node.path)

    try:
        zk.set(node.path, node.data.encode("utf-8"))
    except NoAuthError:
        logging.info("ACLs have prevented setting of data on {path}".format(path=node.path))

    for c in node.children:
        set_data(zk, c)


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper loading as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Reading data from %s" % (args.load))
            node = ZKNode(json_data=file_utils.json_load(args.load))
            logging.info("Restoring all zookeeper data")
            set_data(zk, node)
            logging.info("Loading finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
