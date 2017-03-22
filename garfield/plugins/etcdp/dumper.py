import logging

try:
    from etcd import Client
except ImportError:
    Client = None

from garfield.plugins.etcdp import fingerprinter

def get_data(client,node="/"):
    directory = client.get(node)
    # loop through directory children
    for result in directory.children:
        if result.dir == True:
            get_data(client,result.key)
        else:
            logging.info("\t" + result.key + " : " + result.value)

def run(args,helpers):
    if Client is None:
        logging.warning("Skipping Etcd dumping as Kazoo python library is absent")
    else:
        try:
            logging.info("Dumping Etcd Key Value pairs")
            client = fingerprinter.is_etcd_available(args.ip,args.port)
            get_data(client)
        except Exception:
            logging.exception("Etcd might not be running on this port")
