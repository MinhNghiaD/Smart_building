# Smart_building
This is a Smart Building Project using MQTT protocol to connect all IoTs services in the building.
The architecture is as follow:

                                    ---------------
                                    | Main Server | 
                                    |172.26.22.187|
                                    ---------------
                                            |
                                            |
                     ------------------------------------------------
                     |                                              |
                     |                                              |
                     |                                              |
             ----------------                                 ---------------- 
             | 172.26.22.20 |                                 |172.26.24.250 |
             | Local Server |                                 | Local Server |
             |   10.42.0.1  |                                 |   10.42.0.1  |
             ----------------                                 ----------------
                     |                                              |
             ----------------                                 ----------------
             | IoTs devices |                                 | IoTs devices |
             |   10.42.0.18 |                                 |   10.42.0.18 |
             ----------------                                 ----------------
             
 There are several Local Servers situate at each sector of the building. Each local server also works as a wifi access point to suply the wifi for its sector.
 These Local Server hosts a MQTT Broker and a Web Server Node-RED. The MQTT Broker manage all topics in his sector, all MQTT clients
 can publish a message to a topic or subscribe to a topic. Each message sent to a topic will be sent to all of its subscribers by the MQTT Broker.
 The Node-RED application becomes an MQTT client, it's receive the data from other IoTs devices and create a Web Interface to helps users to control
 all IoTs services in the sector where they are connected to.
 
 In each sector of the Building, IoTs devices connect to their Local Server using its private wifi network (10.42.0.0/16). 
 They publish the data collected from sensors to the Sensor topics and receive commands from Server by subscribing to Command topics. 
 Each Local Server has 2 interfaces, 1 connected to the Ethernet Network of the building (172.26.16.0/20) and one is wifi network (10.42.0.1/16).
 All Local Server manages independently all local events in its private wifi network. Users have to be connected to its wifi in order to access to Node-RED web interface and control the devices.
 
 The Main Server is connected to the Building's network at address 172.26.22.187. In order to communicate with all Local Server inside the building, it has to become an MQTT client of all Local Server.
 It subscribes to all topics of every Local Server, therefore receives every messages that have been sent to the Local Server. Administrators can control every Iots Services of the building by publishing 
 command message to corresponding Local Server. The Main Server saves all the data received in its data base and can act as a bridge between Local Server. A message can be deliveried between Local Server 
 by Main Server.
 
 It is possible to expand the project to create a bigger IoTs network by using the same principal. For example, to create a Network between Smart Buildings, we just need to have another Central Server who subsribes to 
 all Main Server of each Building.
