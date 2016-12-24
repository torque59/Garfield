import os

#Check host is up or not
def check_host(hostname):

    response = os.system("ping -c 1 " + hostname)
    #and then check the response...
    if response == 0:
      return True
    else:
      return False
