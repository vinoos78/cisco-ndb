#!/auto/bgl-golden/python/bin/python2.7

import pexpect
from time import sleep
import sys,os
import re
import logging
import requests, ast, json
from requests.auth import HTTPBasicAuth

#from nxos_switchconfiguration import *
sys.path.append(os.path.abspath("/home/trex/BITS/SEM4-PROJECT/swagger_client"))
sys.path.append(os.path.abspath("/home/trex/BITS/SEM4-PROJECT/swagger_client/api"))

from configuration import *
from api_client import *
from resource_manager_northbound_api import *
from monitor_northbound_api import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########################################################################
######################    Main Script starts here    ######################
###########################################################################

# Uncomment the following lines if Log needs to be stored 

#logFile = '/tmp/' + 'CopyFileToStart' + time.strftime("_%d_%b_%Y_%H_%M_%S",time.gmtime())
#print('\nLogs will be stored at {0}\n'.format(logFile))
#print('\nScript Started... Please wait for Linux prompt...\n\n')
#log_file = open(logFile,"w+")
#sys.stdout = log_file

class NDBController:

    def __init__(self, ip_address, version=None, con_type='http', port=8443, username='admin', password='admin'):

        self.ip_address = ip_address
        self.version = version
        self.con_type = con_type
        self.port = port
        self.username = username
        self.password = password

        kvDict = dict()
        kvDict['host'] = "https://{0}:{1}".format(self.ip_address, self.port)
        kvDict['username'] = self.username
        kvDict['password'] = self.password
        self.configuration = Configuration(kvDict)

        self.api_client = ApiClient(configuration=self.configuration)
        self.monitor_object = None

        self.handle = None

    def get_apiclient(self):
        return self.api_client

    def get_configuration(self):
        return self.configuration

    def get_ip_address(self):
        return self.ip_address

    def get_version(self):
        return self.version

    def get_con_type(self):
        return self.con_type

    def get_port(self):
        return self.port

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


    def connect(self):
        pass

    def register(self, switch):
        print("Registration of switch %s with NDB controller started. NX-API based switches will take time to register" % switch.ip_address)
        print("Finding the platform of the switch. It can be BRCM, MTC or TAHOE based. Classifying it to NX or OF")
        platform = switch.get_platform()
        if platform == "BRCM" or platform == "MTC":
            print("This switch %s belongs to %s platform and is a Openflow supported switch " % (switch.ip_address, platform))
            switch.register_openflow_device()
        elif platform == "TAHOE":
            print("This switch %s belongs to %s platform and is a NX-API supported switch " % (switch.ip_address, platform))
            self.register_nxapi_device(switch=switch, Body=self.get_rest_NX_register_body(switch))

        ret_val = self.getNodeID(switch_ip=switch.ip_address)
        if not ret_val:
            return False
        else:
            switch.set_node_id(ret_val)

        return True


    def register_nxapi_device(self, switch=None, Body=dict()):
        print("Invoking REST-API calls to NDB controller to register switch via NX-API")
        print("Connecting to switch %s via NX-API port 8080" % switch.ip_address)
        res_mgr = ResourceManagerNorthboundApi(api_client=self.api_client)
        res_mgr.resource_resource_manager_northbound_add_node_put(ip_address='%s' % switch.ip_address, body=Body)

    def get_rest_NX_register_body(self, switch):
        Body = dict()
        Body = {
          "address": "%s" % switch.ip_address,
          "port": "8080",
          "username": "%s" % switch.username,
          "password": "%s" % switch.password,
          "type": "%s" % switch.ndb_type,
          "activeIp": "%s" % switch.ip_address,
          "isDeviceReady": 'true',
          "hybridMode": 'false'
        }

        return Body


    def add_monitor_port(self, Body=dict()):
        res_mon = None
        if not self.monitor_object:
            res_mon = MonitorNorthboundApi(api_client=self.api_client)
            self.monitor_object = res_mon
        else:
            res_mon = self.monitor_object
        res_mon.resource_monitor_northbound_add_port_put(body=Body)

    def add_monitoring_device(self, monitor_device_name=None, network='default', Body=dict()):
        res_mon = None
        if not self.monitor_object:
            res_mon = MonitorNorthboundApi(api_client=self.api_client)
            self.monitor_object = res_mon
        else:
            res_mon = self.monitor_object
        res_mon.resource_monitor_northbound_add_device_put(device_name=monitor_device_name, network=network, body=Body)

    def enable_monitoring_devices(self, switch):
        for port in switch.mon_port_list:
            print("Configure port %s as Delivery port" % port)
            name = switch.int_mon_name_dict[port]
            self.add_monitor_port(Body=self.get_rest_monitor_add_port_device_body(switch=switch, port=port, monitor_port_type='Delivery'))
            sleep(3)
            print("Adding Monitoring Device properties to port %s" % port)
            self.add_monitoring_device(monitor_device_name=name, network='default', Body=self.get_rest_monitor_device_body(switch=switch, port=port))

        return True

    def enable_edge_ports(self, switch):
        for port in switch.tap_port_list:
            print("Configuring port %s as Edge-SPAN port" % port)
            self.add_monitor_port(Body=self.get_rest_monitor_add_port_device_body(switch=switch, port=port, monitor_port_type='Edge-SPAN'))
            sleep(3)

        return True

    def create_connections(self, switch, connection_params=[]):
        res_mon = None
        if not self.monitor_object:
            res_mon = MonitorNorthboundApi(api_client=self.api_client)
            self.monitor_object = res_mon
        else:
            res_mon = self.monitor_object

        print("Started Flow/Rule creation for switch %s....." % switch.ip_address)
        for flowObj in connection_params:
            Body = None
            con_name = flowObj.get_connection_name()
            allowFilterList = flowObj.get_allowed_filter_list()
            denyFilterList = flowObj.get_deny_filter_list()
            src_port = flowObj.get_source_port()
            mon_dev_list = flowObj.get_monitor_device_list()
            prio = flowObj.get_priority()
            Body = self.get_rest_connection_body(switch=switch, con_name=str(con_name), port=src_port,
                                          allowFilterList=allowFilterList, denyFilterList=denyFilterList,
                                          monitorDeviceList=mon_dev_list, priority=prio)

            res_mon.resource_monitor_northbound_add_or_modify_rule_put(rule_name=con_name, body=Body)

            alP = ' '.join(allowFilterList)
            dlP = ' '.join(denyFilterList)
            mlP = ' '.join(mon_dev_list)
            print("[SUCCESS] --> Connection name = %s, Allowed Filters = %s, Deny Filters = %s, Source port = %s, Monitor Devices = %s, Priority = %s " % (str(con_name), alP, dlP, src_port, mlP, prio))

    def get_rest_monitor_add_port_device_body(self, switch=None, port=None, monitor_port_type=None):
        Body = dict()
        ndb_type = switch.ndb_type
        node_id = switch.node_id

        converted_port = self.getNDBConvertedPortNamesWrapper(ndb_type=ndb_type, swPortName=port, node_id=node_id)

        #ForkedPdb().set_trace()

        if ndb_type == 'NX':
            Body = {
              "nodeConnector": "NX|%s@NX|%s" % (converted_port, node_id),
              "monitorPortType": "%s" % monitor_port_type,
              "timeStampTagging": "false",
              "timeStampStrip": "false",
              "description": "Delivery Port",
              "adminState": 1,
              "blockRx": "true",
              "dropICMPv6NSM": "true"
            }
        elif ndb_type == 'OF':
            Body = {
                "nodeConnector": "OF|%s@OF|%s" % (converted_port, node_id),
                "monitorPortType": "%s" % monitor_port_type,
                "timeStampTagging": "false",
                "timeStampStrip": "false",
                "description": "",
                "adminState": 1,
                "useLoopback": "false",
                "dropICMPv6NSM": "false",
                "modeTapVlan": 0,
                "blockRx": "true",
                "groupNames": [],
                "erspanId": 0
            }

        return Body

    def get_rest_monitor_device_body(self, switch=None, port=None):
        Body = dict()
        name = switch.int_mon_name_dict[port]
        ndb_type = switch.ndb_type
        node_id = switch.node_id
        converted_port = self.getNDBConvertedPortNamesWrapper(ndb_type=ndb_type, swPortName=port, node_id=node_id)
        Body = {
           "name": "%s" % name,
           "icon": "monitor1",
           "nodeConnector": "%s|%s@%s|%s" % (ndb_type, converted_port, ndb_type, node_id),
           "monitorPortGroup": [],
           "creatorUser": "admin",
           "creatorRole": "Network-Admin"
        }
        print("Monitor Device %s added to port %s" % (name, port))

        return Body


    def get_rest_connection_body(self,switch=None, con_name=None, port=None, allowFilterList=[], denyFilterList=[], monitorDeviceList=[], priority=None):
        Body = dict()
        ndb_type = switch.ndb_type
        node_id = switch.node_id
        converted_port = self.getNDBConvertedPortNamesWrapper(ndb_type=ndb_type, swPortName=port, node_id=node_id)
        Body = {
           "name": "%s" % con_name,
           "allowFilter": allowFilterList,
           "denyFilter": denyFilterList,
           "sourcePort": [
             "%s|%s@%s|%s" % (ndb_type, converted_port, ndb_type, node_id),
           ],
           "device": monitorDeviceList,
           "priority": "%s" % (str(priority)),
           "stripVlan": "false",
           "installInHw": "true",
           "lock": "false",
           "isDeny": "false"
         }

        return Body

    def getNodeID(self, switch_ip=None):
        print("Getting NDB Node ID for switch %s" % switch_ip)
        nodeDict = {}
        OFNodeID = None

        i = 0
        while i < 200:
            try:
                r = requests.get('https://%s:%d/controller/nb/v2/switchmanager/default/nodes' % (self.ip_address,self.port), auth=HTTPBasicAuth('{}'.format(self.username), '{}'.format(self.password)), verify=False, headers={'Content-Type':'application/json'})
   
                if r.status_code == 200:
                    nodeDict = ast.literal_eval(json.dumps(r.json()))
  
                    for ele in nodeDict['nodeProperties']:
                        nN = ele['properties']['ipAddress']['value']
                        if str(switch_ip) == nN:
                            OFNodeID = ele['node']['id']
                            print("NDB node ID for switch %s is %s" % (switch_ip, OFNodeID))
                            return OFNodeID
                else:
                    print("Response for query from NDB controller is not successful. Will retry")

            except Exception:
                if not OFNodeID:
                    print("Openflow Node ID for Switch %s is not yet registered with NDB controller. Waiting for 10 seconds" % switch_ip)
                    i = i + 10
                    sleep(10)

        if not OFNodeID:
            print("Openflow Node ID for Switch %s is not yet registered with NDB controller even after 180 seconds")

        return OFNodeID

    def getNDBConvertedPortNamesWrapper(self, ndb_type=None, swPortName=None, node_id=None):
        if ndb_type == "OF":
            conDict = dict()
            conDict = self.getNDBNodeConnectorProperties(nodeType=ndb_type, nodeID=node_id)
            converted_port = self.getNDBConvertedPortNames(conDict, swPortName)
        elif ndb_type == "NX":
            converted_port = swPortName

        return converted_port

    def getNDBNodeConnectorProperties(self,nodeType="OF", nodeID=None):
        con = None
        conv_nodeID = convert_fid_http_req_format(nodeID)
        r = requests.get('https://%s:%d/controller/nb/v2/switchmanager/default/node/%s/%s' % (self.ip_address,self.port, nodeType, conv_nodeID), auth=HTTPBasicAuth('{}'.format(self.username), '{}'.format(self.password)), verify=False, headers={'Content-Type':'application/json'})
        con = ast.literal_eval(json.dumps(r.json()))

        return con

    def getNDBConvertedPortNames(self, conPropDict, swPortName, state = 1):

        ndb_port_num = None
    
        portN = None
        if re.search("^[Ee]th.*",swPortName):
            portN = re.search("^[a-zA-Z-]+\s*([0-9/]+)", swPortName)
            if portN:
                port_num = "Eth" + portN.group(1)
        elif re.search("^[Pp]ort.*",swPortName):
            portN = re.search("^[a-zA-Z-]+\s*([0-9]+)", swPortName)
            if portN:
                port_num = "Po" + portN.group(1)
    
        for ele in conPropDict['nodeConnectorProperties']:
            if str(port_num) == str(ele['properties']['name']['value']) and ele['properties']['state']['value'] == state:
                ndb_port_num = ele['nodeconnector']['id']
    
        return ndb_port_num


def convert_fid_http_req_format(fid):
    fidnew = fid.replace(':', "%3A")
    return fidnew

###########################################################################
######################     Main Script ends here     ######################
###########################################################################
