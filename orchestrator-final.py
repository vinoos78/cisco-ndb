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
from ndb_controller import *
from connections import *

device_params = dict()

nxos_device_list = ['10.197.137.52', '10.197.137.54', '10.197.137.74']
device_params = {'10.197.137.52': {'mon_port_list': ['Ethernet1/1', 'Ethernet1/3'],
                 'mon_device_name_list': ['FIREPOWER', 'VoD'],
                'tap_port_list': ['Ethernet1/2']},
                '10.197.137.54': {'mon_port_list': ['Ethernet1/10'],
                 'mon_device_name_list': ['IDS'],
                'tap_port_list': ['Ethernet1/16']},
                 '10.197.137.74': {'mon_port_list': ['Ethernet1/31'],
                 'mon_device_name_list': ['WEB-FILTER'],
                'tap_port_list': ['Ethernet1/32']}
                }

connection_params = dict()
conObjList = []
conObjList.append(Connections(allow_filter_list=["Default-Match-IP"], src_port="Ethernet1/2", monitor_device_list=['FIREPOWER'], priority="100"))
conObjList.append(Connections(allow_filter_list=["Default-Match-ICMP"], src_port="Ethernet1/2", monitor_device_list=['VoD'], priority="200"))
conObjList.append(Connections(deny_filter_list=["Default-Match-ARP"], src_port="Ethernet1/2", monitor_device_list=[], priority="10"))
connection_params.update({'10.197.137.52': conObjList })

conObjList = []
conObjList.append(Connections(allow_filter_list=["Default-Match-IP"], src_port="Ethernet1/16", monitor_device_list=['IDS'], priority="100"))
connection_params.update({'10.197.137.54': conObjList })

conObjList = []
conObjList.append(Connections(allow_filter_list=["Default-Match-all"], src_port="Ethernet1/32", monitor_device_list=['WEB-FILTER'], priority="20"))
connection_params.update({'10.197.137.74': conObjList })

#Create Object for NDB controller
ndb = NDBController('10.197.137.68')

for ip in nxos_device_list:
    print("##########################################################")
    print("# STARTING CONFIGURATIONS FOR SWITCH %s             #" % ip)
    print("##########################################################")
    print("Connecting to Switch %s" % ip)
    device = NXOSSwitch(ip, ndb_controller=ndb, device_params=device_params[ip])
    device.connect()
    print("Registering switch %s with Nexus Data Broker Controller %s" % (ip, ndb.ip_address))
    ndb.register(device)
    print("Enable monitoring device for switch %s" % ip)
    ndb.enable_monitoring_devices(device)
    print("Enable edge ports for switch %s" % ip )
    ndb.enable_edge_ports(device)
    print("Create flows/rules on switch %s based on the connection parameters" % ip)
    ndb.create_connections(device, connection_params[ip])
    print("##########################################################")
    print("# END OF CONFIGURATIONS FOR SWITCH %s               #" % ip)
    print("##########################################################")

