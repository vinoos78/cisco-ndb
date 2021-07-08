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


class NXOSSwitch:

    def __init__(self, ip_address, con_type='ssh', username='admin', password='nbv12345', controller=None, device_params=dict()):

        self.ip_address = ip_address
        self.con_type = con_type
        self.username = username
        self.password = password
        self.controller = controller
        self.mon_port_list = device_params['mon_port_list']
        self.tap_port_list = device_params['tap_port_list']
        self.mon_device_name_list = device_params['mon_device_name_list']

        self.int_mon_name_dict = dict()
        for i in range(0,len(self.mon_port_list)):
            self.int_mon_name_dict.update({self.mon_port_list[i] : self.mon_device_name_list[i]})
            
        print("Initialzed the swtich %s object" % self.ip_address)
        self.handle = None
        self.pipeline = None
        self._type = None
        self.node_id = None

    def get_ip_address(self):
        return self.ip_address

    def get_con_type(self):
        return self.con_type

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_mon_port_list(self):
        return self.mon_port_list

    def get_tap_port_list(self):
        return self.tap_port_list

    def get_mon_device_name_list(self):
        return self.mon_device_name_list

    def set_node_id(self,node_id):
        self.node_id = node_id

    def get_node_id(self):
        return self.node_id

    def connect(self):

        swHdl = pexpect.spawn("%s -o StrictHostKeyChecking=no %s@" % (self.con_type,self.username) + self.ip_address)
        #swHdl.logfile = sys.stdout
        swHdl.logfile = None
        swHdl.sendline('\r')

        # Login to switches
        j = swHdl.expect(['# $','login:','assword:'],timeout=20)
        if j==0:
            swHdl.sendline('\r')
            swHdl.expect('# $')
        if j==1:
            swHdl.sendline(self.username)
            swHdl.expect('assword:')
            swHdl.sendline(self.password)
            swHdl.expect('# $')
        if j==2:
            swHdl.sendline(self.password)
            swHdl.expect('# $')

        swHdl.timeout = 300
        sleep(2)
        swHdl.sendline("term length 0")
        swHdl.expect('# $')

        self.handle = swHdl
        print("Connected to Switch %s" % self.ip_address)

        return swHdl

    def get_platform(self):

        swHdl = self.handle

        swHdl.sendline('bcm-shell module 1')
        swHdl.sendline('\r')
        j = swHdl.expect(['bcm-shell.0> $', '% Invalid command.*'],timeout=5)

        if j==0:
            swHdl.sendline('exit')
            swHdl.expect('# $')
            self.platform = "BRCM"
            self.pipeline = 201
            self._type = "OF"
        if j==1:
            swHdl.expect('# $')
            self.platform = "TAHOE"
            self._type = "NX"

            swHdl.sendline('show module')
            swHdl.expect('# $')
            output = swHdl.before

            mat = re.search('3548', output)
            if mat:
                self.pipeline = 203
                self.platform = "MTC"
                self._type = "OF"

        return self.platform

    def register_openflow_device(self):
        print("Configuring openflow commands in the switch...")
        print("Pipeline = %d \n Controller IP = %s \n Controller port = 6653 " % (self.pipeline, self.controller.ip_address))
        config = "\n"
        for ofport in self.mon_port_list + self.tap_port_list:
            print("Adding port %s as OF-PORT" % ofport)
            config += "of-port interface {0}\n".format(ofport)
        cmd = '''conf t
                openflow
                switch 1 pipeline %d
                controller ipv4 %s port 6653 vrf management security none
                probe-interval 10
                max-backoff 5
                %s
                end
        ''' % (self.pipeline, self.controller.ip_address, config)
        swHdl = self.handle
        swHdl.sendline(cmd)
        swHdl.sendline('\r')
        swHdl.expect('# $')

###########################################################################
######################     Main Script ends here     ######################
###########################################################################
