#!/usr/bin/python
# Core Settings File For Commands and Options

from utils import check_host
from dcms.hashiconsul import attacks as consul_attacks
from dcms.logger import rootLogger


target = False
mas = False
post_status = False

def Settings(args):

    target = args['ip']
    port = args['port']
    discover = args['discover']
    attack = args['attack']

    #filename = args['file']
    try:
        # Checks whether Host is up
        if target:
            if check_host(target):
                rootLogger.info("Host "+target+" is up")

        if discover == "consul":
            hashiconsul.discovery.discover(target)

        if attack == "consul":
            consul_attacks.check_ssrf(target)
            #consul_attacks.check_rce(target)

    except Exception as e:
        rootLogger.error(str(e))
