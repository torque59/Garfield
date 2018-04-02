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


def get_data(zk, node_path, data_regex=None):
    try:
        data, stat = zk.get(node_path)
    except NoAuthError:
        data = "<Couldn't read because of ACLs>"
        logging.debug("ACLs prevent reading of this data for {node_path}".format(node_path=node_path))
    acls, stat = zk.get_acls(node_path)
    node = ZKNode(path=node_path, data=data, stat=stat, acls=acls)
    # Check if there is data
    # Check if a filter is not there, if there then find
    if (data_regex is None) or (data_regex and node.data and re.findall(data_regex, node.data, re.M | re.I)):
        logging.info(node)

    try:
        children = zk.get_children(node_path)
        for c in children:
            node.add_child(get_data(zk, os.path.join(node_path, c), data_regex=data_regex))
    except NoAuthError:
        logging.debug("ACLs prevent extracting children nodes for {node_path}".format(node_path=node_path))

    return(node)


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper dumping as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Dumping all zookeeper data to %s" % (args.dump))
            node = get_data(zk, args.node, data_regex=args.data_regex)
            file_utils.json_dump(args.dump, node.jsonify())
            logging.info("Dumping finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
