import paho.mqtt.client as mqtt
import threading
import time

def on_connect(client, userdata, returnCode):
    if returnCode == 0:
        self.client.connected_flag = True
        print("connected")
    else:
        print("bad connection, return code: {}".fromat(returnCode))

def on_disconnect(client, userdata, returnCode=0):
    logging.debug("Disconnected result code : " + str(returnCode))
    client.loop_stop()

class Reactor:
    '''contains list of controller (object that used control channels)
    when a message arrive, it distributes the message and to topic to all controller
    a controller can be activate or desactivate'''
    def __init__(self):
        self.activeControllers = []
        self.inactiveControllers = []
    def addController(self, controller):
        self.activeControllers.append(controller)
    def desactivateController(self, controller):
        self.inactiveControllers.append(controller)
        self.activeControllers.remove(controller)
    def activateController(self, controller):
        self.activeControllers.append(controller)
        self.inactiveControllers.remove(controller)
    def removeController(self, controller):
        self.activeControllers.remove(controller)
        self.inactiveController.remove(controller)
    def getController(self, id):
        for controller in self.activeControllers:
            if controller.id == id :
                return controller
        for controller in self.inactiveControllers:
            if controller.id == id:
                return controller
    def reactToCommand(self, client, userdata, message):
        for controller in self.activeControllers:
            controller.execute(message)


class Controller:
    '''define syntax control in mainFunc passed as an argument'''
    def __init__(self, id, topic, mainFunc):
        self.id = id
        self.topic = topic
        self.mainFunc = mainFunc
    def execute(self, message):
        if (message.topic = self.topic):
            self.mainFunc(message.payload.decode("utf-8")) #if match the topic -> pass the command message to mainFunc to execute



class Sender:
    '''Regroup message and send it to the broker'''
    def __init__(self):
        self.channels = []
    def addChannel(self, name, topic, channel, interval=10):
        timer = threading.Timer()

class SendMessage:
    def __init__(self, topic, channel):
        self.channel = 


mqtt.Client.connected_flag = False


class MQTTAdaptor:
    def __init__(self, clientID, clean_session=True, userdata=None, brokerIP="127.0.0.1"):
        self.client = mqtt.Client(clientID, clean_session, userdata)
        self.reactor = Reactor()
        self.client.on_connect = on_connect        #on_connect callback
        self.client.on_disconnect = on_disconnect
        self.client.on_message = self.reactor.reactToCommand
        self.client.loop_start()
        print("connecting to MQTT broker " + brokerIP)
        self.client.connect(brokerIP)
        while not client.connected_flag:
            time.sleep(1)
    def __del__(self):
        self.client.loop_stop()
        self.client.disconnect()
    def addController(self, name, topic, mainFunc):
        try:
            self.client.subscribe(topic)
            self.reactor.addController(Controller(name, topic, mainFunc))
        except:
            print("error occurs when adding new controller")
    def removeController(self, name):
        controller = self.reactor.getController(name)
        self.reactor.removeController(controller)
