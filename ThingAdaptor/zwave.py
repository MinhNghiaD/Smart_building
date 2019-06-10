#!/usr/bin/env python

import logging
import sys, os
import resource
#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger('openzwave')
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time


device="/dev/ttyACM0"                       #COM port of device, normally ttyUSB0, if not exist => switch to ttyACM0
log="Debug"

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        logging.log("help : ")
        logging.log("  --device=/dev/yourdevice ")
        logging.log("  --log=Info|Debug")

#step 1: configuration=========> should be cached to simplify utilization
options = ZWaveOption(device, \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level(log)
#options.set_save_log_level('Info')
options.set_logging(False)
options.lock()

#step 2: create network object

def createNetwork(options, log=None, autostart=True, kvals=True):
    network = ZWaveNetwork(options, log=None)
    time_started = 0
    for i in range(0,100):
        if network.state>=network.STATE_AWAKED:
            break
        else:
            time_started += 1
            time.sleep(1.0)
    if network.state<network.STATE_AWAKED:
        print("Network is not awake but continue anyway")

    for i in range(0,300):
        if network.state>=network.STATE_READY:
            print("home ID {}".format(home_id))
            break
        else:
            sys.stdout.write(".")
            time_started += 1
            #sys.stdout.write(network.state_str)
            #sys.stdout.write("(")
            #sys.stdout.write(str(network.nodes_count))
            #sys.stdout.write(")")
            #sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)

    if not network.is_ready:
        print("network is not ready but start anyway")
    network.start()
    return network;

#Function of controller
def getController(options):
     network = createNetwork(option)
     controller = network.controller
     return controller

def getDevices(network):
    listDevices = []
    for node in network.notes:
        device = {
            'node_id' : network.nodes[node].node_id,
            'name': network.nodes[node].name,
            'manufacturer' : {'id' : network.nodes[node].manufacturer_id, 'name':network.nodes[node].manufacturer_name},
            'type' : network.nodes[node].device_type,
            'product' : {'id' : network.nodes[node].product_id, 'name' : network.nodes[node].product_name, 'type' : network.nodes[node].product_type},
            'version' : network.nodes[node].version,
            'command_class' : network.nodes[node].command_classes_as_string,
            'capabilities' : network.nodes[node].capabilities,
            'can_sleep' : network.nodes[node].can_wake_up()
        }
        listDevices.append(device)
    return listDevices

def addDevice(controller, security_check=False):
    #start inclusion process to add new nodes to network
    controller.begin_command_add_device(high_power=True)
    controller.addNode(security_check)

def removeDevice(controller):
    controller.begin_command_remove_device(high_power=True)

def checkNodefail(controller, node_id):
    return controller.begin_command_has_node_failed(node_id)

def removeFailedNode(controller, node_id):
    controller.begin_command_remove_failed_node(node_id)
    controller.remove_failed_node(nodeid)

def removeNode(controller, node_id):
    controller.remove_node(node_id)

def cancelCommand(controller):
    controller.cancel_command()

def softReset(controller):
    controller.soft_reset()

def hardReset(controller):
    controller.hard_reset()

def healNetwork(network):
    network.heal(upNodeRoute= True)

def switchAll(command = True):
    network.switch_all(command)

def getNeighbor(controller):
    return controller.neighbors

#Function of nodes
def nodeID(node):
    return node.node_id     #return node Id for later use  => attribute of a node

def getNeighbor(node):
    return node.neighbors

def neighborUpdate(node):
    node.neighbor_update()

def nodeIsSleeping(node):
    return node.is_sleeping

def nodeLocation(node):
    return node.location

def getPower_level(node):
    return node.get_power_levels()

def getBattery_level(node):
    node.get_battery_levels()

#list all posible channel of a node
def getSensors(node):
    listSensors = []
    for channel in node.get_sensors():
        sensor = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listSensors.append(sensor)
    return listSensors

def getDimmers(node):
    listDimmers = []
    for channel in node.get_dimmers():
        dimmer = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listDimmers.append(dimmer)
    return listDimmers

def getSwitches(node):
    listSwitches = []
    for channel in node.get_switches() :
        switch = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listSwitches.append(switch)
    return listSwitches

def getRgbBulbs(node):
    listRgbbulbs = []
    for channel in node.get_rgbbulbs():
        bulb = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listRgbbulbs.append(bulb)
    return listRgbbulbs

def getThermostats(node):
    listThermostats = []
    for channel in node.get_rgbbulbs():
        thermostat = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listThermostats.append(thermostat)
    return listThermostats

def getDoorlocks(node):
    listDoorlocks = []
    for channel in node.get_doorlocks():
        doorlock = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listDoorlocks.append(doorlock)
    return listDoorlocks

def getProtections(node):
    listProtection = []
    for channel in node.get_protections():
        protection = {
            #attributes of a channel
            'value_id': channel.value_id,
            'label':node.values[channel].label,
            'help':node.values[channel].help,
            'max':node.values[channel].max,
            'min':node.values[channel].min,
            'units':node.values[channel].units,
            'data':node.values[channel].data,
            'data_str':node.values[channel].data_as_string,
            'genre':node.values[channel].genre,
            'type':node.values[channel].type,
            'ispolled':node.values[channel].is_polled,
            'readonly':node.values[channel].is_read_only,
            'writeonly':node.values[channel].is_write_only,
        }
        listProtection.append(protection)
    return listProtection

#function for channels
#sensors
def getSensor_value(value_id):
    return get_sensor_value(value_id)

#derivative for dimmers
def getDimmer_value(value_id):
    return get_dimmer_level(value_id)

def setDimmer_value(value_id, value):
    set_dimmer(value_id, value)

#derivative for Switch
def getSwitch_state(value_id):
     return get_switch_state(value_id)

def setSwitch(value_id, value):
     set_switch(value_id, value)

#derivative for Rgb Bulbs
def getRgbBulb_value(value_id):
    return get_rgbw(value_id)

def setRgbBulb_value(value_id, value):
    set_rgbw(value_id, value)

#derivative for Thermostats
def getThermostat_value(value_id):
    return value_id.data

def setThermostat_value(value_id, value):
    data = value_id.check_data(value)
    set_thermostat(value_id, data)

#derivative for Door lock
def getUsercode(value_id):
    return value_id.get_usercodes(index='All')

def setUser_code(value_id, value):
    set_usercode(value_id, value)

def setDoorlock_value(value_id, value):
    #lock = true, unlock= false
    set_doorlock(value_id, value)

network = createNetwork(options, log=None, autostart=True, kvals=True)
print("***********************************************************************")
for node in network.nodes:  #dict() of nodes
    print("type: {}".format(network.nodes[node].device_type))
    print("{} - Name : {}".format(network.nodes[node].node_id,network.nodes[node].name))
    print("{} - Manufacturer name / id : {} / {}".format(network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
    print("{} - Product name / id / type : {} / {} / {}".format(network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type))
    print("{} - Version : {}".format(network.nodes[node].node_id, network.nodes[node].version))
    print("{} - Command classes : {}".format(network.nodes[node].node_id,network.nodes[node].command_classes_as_string))
    print("{} - Capabilities : {}".format(network.nodes[node].node_id,network.nodes[node].capabilities))
    print("{} - Neigbors : {}".format(network.nodes[node].node_id,network.nodes[node].neighbors))
    print("{} - Can sleep : {}".format(network.nodes[node].node_id,network.nodes[node].can_wake_up()))
    print("************************************")

    for cmd in network.nodes[node].command_classes:
        print("   ---------   ")
        #print("cmd = {}".format(cmd))
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print("{} - Values for command class : {} : {}".format(network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values))
    print("------------------------------------------------------------")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  state: {}".format(network.nodes[node].get_switch_state(val)))
