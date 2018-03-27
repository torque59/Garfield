import os
import re
import logging

from garfield.lib import file_utils

try:
    from kazoo.client import KazooClient
    from kazoo.exceptions import NoAuthError
except ImportError:
    KazooClient = None

def prettify_acls(acls):
    acl_strings = []
    for acl in acls:
        acl_strings.append("%s:%s:%s" % (",".join(acl.acl_list), acl.id.scheme, acl.id.id))
    return(" ".join(acl_strings))

def get_data(zk, node, f=None, data_regex=None):
    try:
        data, stat = zk.get(node)
    except NoAuthError:
        data = "<Couldn't read because of ACLs>"
        logging.debug("ACLs prevent reading of this data for {node}".format(node=node))
    acls, stat = zk.get_acls(node)
    # Check if there is data
    info = "\n%s\n" % (node)
    if data is not None and len(data) > 0:
        data = data.decode("utf-8", "ignore")
        # Check if a filter is not there, if there then find
        if (data_regex is None) or (data_regex and re.findall(data_regex, data, re.M | re.I)):
            info += "Version: %s\nACLs: %s\nData: %s\n\n" % (stat.version, prettify_acls(acls), data)
    logging.info(info)
    if f is not None:
        f.write(info)

    try:
        children = zk.get_children(node)
        for c in children:
            get_data(zk, os.path.join(node, c), f=f, data_regex=data_regex)
    except NoAuthError:
        logging.debug("ACLs prevent extracting children nodes for {node}".format(node=node))


def run(args, helpers):
    if KazooClient is None:
        logging.warning("Skipping zookeper dumping as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            logging.info("Dumping all zookeeper data to %s" % (args.dump))
            file_utils.open_file(args.dump, "w", lambda x: get_data(zk, args.node, f=x, data_regex=args.data_regex))
            logging.info("Dumping finished")
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
