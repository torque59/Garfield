import consul
from dcms.logger import rootLogger

def is_consul_available(target):

    try:
        con = consul.Consul(target)
        config = con.agent.self()
        return con

    except Exception as err:
        return False


def discover(con):

    rootLogger.info("Starting Discovery phase for Consul\n")
    config = con.agent.self()
    
    try:

        rootLogger.info("Host is Running Consul\n")
        rootLogger.info("Consul Version : "+config['Config']['Version'])
        rootLogger.info("Consul Nodename : "+config['Config']['NodeName']+"\n")

        rootLogger.info("Consul Ports open: DNS - "+str(config['Config']['Ports']['DNS']))
        rootLogger.info("Consul Ports open: HTTP - "+str(config['Config']['Ports']['HTTP'])+"\n")

        if config['Config']['EnableUi']:

            rootLogger.info("Consul UI is enabled, browse on to http://"+target+":8500/ui/")

    except Exception as err:

        rootLogger.error(err)
