#!/usr/bin/python

#+++++++++++++++++++++++++++++#
# Author: Vinu Chandran
#++++++++++++++++++++++++++++#

#Following code invokes regsitration tasks for different types of NX-OS switches supporting either OpenFlow or NX-API.
#Internally platform is identified and corresponding registration APIs are called.
# Broadcom based - Supports Openflow
# 3548 High Freqeuncy Trading Switches - Supports Openflow
# Nexus 9000 with Cisco Asics - Supports NX-API

from nxos_switch import *
from controller import *
from connections import *

device_params = dict()

'''
Add your device ip addresses reachable from NDB controller as a LIST
Example
nxos_device_list = ['192.168.0.1', '192.168.0.2']
'''
nxos_device_list = []

'''
device_params is a nested dictionary where you map device IP address with 
Monitor port list
Monitor Device Name list
Edge SPAN tap port list 
Example:
device_params = {'192.168.0.1': {'mon_port_list': ['Ethernet1/1'],
                 'mon_device_name_list': ['FIREPOWER'],
                'tap_port_list': ['Ethernet1/2']}
                }
'''

device_params = {}

'''
connection_params is a dictionary holding the device IP as key and list of connection objects for that device.
Connection objects are create using Connections class. Arguments to the constructor is 
allow_filter_list
src_port
monitor_device_list
priority

You can have multiple such connections objects created and appeding the the connection object list and map it to
the device IP key in connection_params
'''

connection_params = dict()
conObjList = []
conObjList.append(Connections(allow_filter_list=[], src_port="", monitor_device_list=[], priority=""))
connection_params.update({'': conObjList })

# +++++++++++++++ End of Input +++++++++++++++++++#
'''
Create Object for controller. If the password is different than the default, pass it as separate argument. 
Check the Controller class to know all available arguments
'''
controller = Controller('<Controller IP address>') 

for ip in nxos_device_list:
    print("##########################################################")
    print("# STARTING CONFIGURATIONS FOR SWITCH %s             #" % ip)
    print("##########################################################")
    print("Connecting to Switch %s" % ip)
    device = NXOSSwitch(ip, controller=controller, device_params=device_params[ip])
    device.connect()
    print("Registering switch %s with Nexus Data Broker Controller %s" % (ip, controller.ip_address))
    controller.register(device)
    print("Enable monitoring device for switch %s" % ip)
    controller.enable_monitoring_devices(device)
    print("Enable edge ports for switch %s" % ip )
    controller.enable_edge_ports(device)
    print("Create flows/rules on switch %s based on the connection parameters" % ip)
    controller.create_connections(device, connection_params[ip])
    print("##########################################################")
    print("# END OF CONFIGURATIONS FOR SWITCH %s               #" % ip)
    print("##########################################################")

