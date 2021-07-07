#!/auto/bgl-golden/python/bin/python2.7

import pexpect
from time import sleep
import sys,os
import re
import logging

#from nxos_switchconfiguration import *
sys.path.append(os.path.abspath("/home/trex/BITS/SEM4-PROJECT/swagger_client"))
sys.path.append(os.path.abspath("/home/trex/BITS/SEM4-PROJECT/swagger_client/api"))

from resource_manager_northbound_api import *

###########################################################################
######################    Main Script starts here    ######################
###########################################################################

# Uncomment the following lines if Log needs to be stored 

#logFile = '/tmp/' + 'CopyFileToStart' + time.strftime("_%d_%b_%Y_%H_%M_%S",time.gmtime())
#print('\nLogs will be stored at {0}\n'.format(logFile))
#print('\nScript Started... Please wait for Linux prompt...\n\n')
#log_file = open(logFile,"w+")
#sys.stdout = log_file

import random, string
import pdb

class ForkedPdb(pdb.Pdb):
    '''A Pdb subclass that may be used
    from a forked multiprocessing child
    '''

    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin

    #HOW TO USE: 
    # ForkedPdb().set_trace()


class Connections:

    def __init__(self, allow_filter_list=[], deny_filter_list=[], src_port=None, monitor_device_list=[], priority="100" ):

        self.name =  str("con" + "-" + generateRandomString())
        self.allowFilterList = allow_filter_list
        self.denyFilterList = deny_filter_list
        self.sourcePort = src_port
        self.monitor_device_list = monitor_device_list
        self.priority = priority
        self.stripVlan = "false"
        self.installInHw = "true"
        self.lock =  "false"
        self.isDeny = "false"

    def get_connection_name(self):
        return self.name
    def get_allowed_filter_list(self):
        return self.allowFilterList
    def get_deny_filter_list(self):
        return self.denyFilterList
    def get_source_port(self):
        return self.sourcePort
    def get_monitor_device_list(self):
        return self.monitor_device_list
    def get_priority(self):
        return self.priority

def generateRandomString(count=5):
    return ''.join(random.sample(string.ascii_lowercase, count))

###########################################################################
######################     Main Script ends here     ######################
###########################################################################
