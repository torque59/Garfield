import logging
try:
    from consul import Consul
except ImportError:
    Consul = None

#Check if Consul is available or not.

def is_consul_available(target,port):
    version = None
    if Consul is None:
        logging.warning("Skipping Consul Discovery as Consul python library is absent")
    else:
        try:
            con = Consul(target,port=port)
            config = con.agent.self()
            return con

        except Exception as err:
            logging.exception(err)
            return False

#Checks if Consul is Discoverable

def run(args, helpers):

    logging.info("Starting Discovery phase for Consul\n")

    con = is_consul_available(args.ip,args.port)
    #Used to get the Consul agent object
    config = con.agent.self()

    try:

        logging.info("Host is Running Consul\n")
        logging.info("Consul Version : "+config['Config']['Version'])
        logging.info("Consul Nodename : "+config['Config']['NodeName']+"\n")

        logging.info("Consul Ports open: DNS - "+str(config['Config']['Ports']['DNS']))
        logging.info("Consul Ports open: HTTP - "+str(config['Config']['Ports']['HTTP'])+"\n")

        if config['Config']['EnableUi']:

            logging.info("Consul UI is enabled, browse on to http://"+args.ip+":8500/ui/")

    except Exception as err:
        logging.exception(err)
