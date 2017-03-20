import os
import re
import logging

from garfield.lib import file_utils

try:
    from kazoo.client import KazooClient
except ImportError:
    KazooClient = None


def get_data(zk, node, f=None, data_regex=None):
    data, stat = zk.get(node)
    # Check if there is data
    if data is not None and len(data) > 0:
        data = data.decode("utf-8", "ignore")
        # Check if a filter is not there, if there then find
        if (data_regex is None) or (data_regex and re.findall(data_regex, data, re.M | re.I)):
            info = "\n%s\nVersion: %s\nData: %s\n\n" % (node, stat.version, data)
            logging.info(info)
            if f is not None:
                f.write(info)
    children = zk.get_children(node)
    for c in children:
        get_data(zk, os.path.join(node, c), f=f, data_regex=data_regex)


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper dumping as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Dumping all zookeeper data to %s" % (args.dump))
            file_utils.open_file(args.dump, "w", lambda x: get_data(zk, "/", f=x, data_regex=args.data_regex))
            logging.info("Dumping finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
