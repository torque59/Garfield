import logging

try:
    from etcd import Client
except ImportError:
    Client = None

#Check if Consul is available or not.

def is_etcd_available(target,port):
    version = None
    if Client is None:
        logging.warning("Skipping Etcd Discovery as Consul python library is absent")
    else:
        try:
            client = Client(host=target,port=port)
            return client

        except Exception as err:
            logging.exception(err)
            return False

#Checks if Consul is Discoverable

def run(args, helpers):

    logging.info("Starting Discovery phase for Consul\n")

    client = is_etcd_available(args.ip,args.port)
    #Used to get the Consul agent object
    try:

        logging.info("Host is Running Etcd\n")
        logging.info("Etcd Version : " + client.version)
        logging.info("Etcd Machines Available : ")
        for machine in client.machines:
            logging.info("\t" + machine)

        logging.info("Printing Etcd Leader Info")
        for details in client.leader:
                logging.info("\t" + details + " : " + str(client.leader.get(details)))

    except Exception as err:
        logging.exception(err)
