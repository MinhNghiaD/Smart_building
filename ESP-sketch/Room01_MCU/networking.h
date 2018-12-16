#ifndef NETWORK_H
#define NETWORK_H

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
/*---------------------------------WIFI-----------------------------------------*/
void wifi_connect(char* ssd, char* password);			//establish wifi connection

/*---------------------------------MQTT-----------------------------------------*/
void MQTT_connect(PubSubClient client, char* clientID, char** topic, unsigned int nb_topic);           //maintain connection with MQTT Server
#endif

void wifi_connect(char* ssd, char* password)
{
  	WiFi.begin(ssd, password);
  	Serial.println("Connecting to wifi");
  
  	//attemp to connect until connection establish
 	while(WiFi.status() != WL_CONNECTED)
  	{
    		delay(500);
    		Serial.print(".");
  	}
  	Serial.println();

  	//When connected to wifi, print out IPv4 assigned for ESP
  	Serial.print("Connected. IP address of ESP: ");
  	Serial.println(WiFi.localIP());               
}

void MQTT_connect(PubSubClient client, char* clientID, char** topic, unsigned int nb_topic)
{
    //Serial.println("Check Connection with MQTT server");
    while(!client.connected()) 
    {
        if(!client.connect(clientID)) 
        {
          Serial.print("False to reconnect. ");
          Serial.print(client.state());
          Serial.println(" try again in 5 seconds");
          delay(5000);            // Wait 5 seconds before retrying
        }
        else          //connected
        {
          for(int i=0; i<nb_topic; i++)
          {
            client.subscribe(topic[i]);
          }
        }
    }
    if(!client.loop())
    {
        client.connect(clientID);
        
    }
    //Serial.println("Connected to MQTT");
}
