import consul
#from logger import rootLogger
global passfound

def discover(target):

    con = consul.Consul(target)
    print con['Config']['Version']
