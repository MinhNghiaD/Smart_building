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



class Controller:
    def __init__(self):
        #super(, self).__init__()
        options = ZWaveOption(device, \
          user_path=".", cmd_line="")
        options.set_log_file("OZW_Log.log")
        options.set_append_log_file(False)
        options.set_console_output(True)
        options.set_save_log_level(log)
        #options.set_save_log_level('Info')
        options.set_logging(False)
        options.lock()
        self._optiton = options
        self.network = ZWaveNetwork(options, log=None)
        time_started = 0
        for i in range(0,100):
            if self.network.state>=self.network.STATE_AWAKED:
                break
            else:
                time_started += 1
                time.sleep(1.0)
        if self.network.state<self.network.STATE_AWAKED:
            print("Network is not awake but continue anyway")

        for i in range(0,300):
            if self.network.state>=self.network.STATE_READY:
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
        self.controller = network.controller

    def getDevices(self):
        return self.network.nodes

    def addDevice(self, security_check=False):
        #start inclusion process to add new nodes to network
        self.controller.begin_command_add_device(high_power=True)
        self.controller.addNode(security_check)

    def removeDevice(self):
        self.controller.begin_command_remove_device(high_power=True)

    def checkNodefail(self, node_id):
        return self.controller.begin_command_has_node_failed(node_id)

    def removeFailedNode(self, node_id):
        self.controller.begin_command_remove_failed_node(node_id)
        self.controller.remove_failed_node(nodeid)

    def removeNode(self, node_id):
        self.controller.remove_node(node_id)

    def cancelCommand(self):
        self.controller.cancel_command()

    def softReset(self):
        self.controller.soft_reset()

    def hardReset(self):
        self.controller.hard_reset()

    def healNetwork(self):
        self.network.heal(upNodeRoute= True)

    def switchAll(command = True):
        self.network.switch_all(command)

    def getNeighbor(self):
        return controller.neighbors

class Node:
    '''Base class of other zwave nodes in network'''
    def __init__(self, node):
        self.node = node

    def nodeID(self):
        return self.node.node_id     #return node Id for later use  => attribute of a node

    def info(self):
        info = {
            'node_id' : self.node.node_id,
            'name': self.node.name,
            'manufacturer' : {'id' : self.node.manufacturer_id, 'name':self.node.manufacturer_name},
            'type' : self.node.device_type,
            'product' : {'id' : self.node.product_id, 'name' : self.node.product_name, 'type' : self.node.product_type},
            'version' : self.node.version,
            'command_class' : self.node.command_classes_as_string,
            'capabilities' : self.node.capabilities,
            'can_sleep' : self.node.can_wake_up()
        }
        return
    def getNeighbor(self):
        return self.node.neighbors

    def neighborUpdate(self):
        return self.node.neighbor_update()

    def nodeIsSleeping(self):
        return self.node.is_sleeping

    def nodeLocation(self):
        return self.node.location

    def getPower_level(self):
        return self.node.get_power_levels()

    def getBattery_level(self):
        return self.node.get_battery_levels()

class

def main():
    controller = Controller()
    listDevices = controller.getDevices()
    for device in listDevices:
        node = Node(device)
        print(node.info())

if __name__ == "__main__":
    main()
