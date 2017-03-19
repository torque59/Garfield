import logging

try:
    from kazoo.client import KazooClient
except ImportError:
    KazooClient = None


def run(args, helpers):
    version = None
    if KazooClient is None:
        logging.warning("Skipping zookeper discovery as Kazoo python library is absent")
    else:
        try:
            zk = KazooClient(hosts="%s:%d" % (args.ip, args.port), read_only=True)
            zk.start()
            version = zk.server_version()
            logging.info("Detected Zookeeper version: %s" % ('.'.join(str(i) for i in version)))
        except Exception:
            logging.exception("Zookeeper might not be running a client listener on this port")
    return(version)
