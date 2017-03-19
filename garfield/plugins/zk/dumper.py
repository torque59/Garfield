import os
import logging

from garfield.lib import file_utils

try:
    from kazoo.client import KazooClient
except ImportError:
    KazooClient = None


def get_data(zk, node, f):
    info = "%s\n" % (node)
    data, stat = zk.get(node)
    if len(data) > 0:
        info += "Version: %s\nData: %s\n\n" % (stat.version, data.decode("utf-8"))
    logging.info(info)
    f.write(info)
    children = zk.get_children(node)
    for c in children:
        get_data(zk, os.path.join(node, c), f)
    return(info)


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper dumping as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Dumping all zookeeper data to %s" % (args.dump))
            file_utils.open_file(args.dump, "w", lambda x: get_data(zk, "/", x))
            logging.info("Dumping finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
