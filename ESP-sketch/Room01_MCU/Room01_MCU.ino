/*
 * Created 20/11/2018 by Minh Nghia Duong
 * 
 * This Ketch yse function in network.h head file to connect to Wifi and MQTT server and functions in sensor.h to take data from sensor
 * It controls the temperature, humidity and light in the room
 * The NodeMCU will reveive the data from DHT11 sensor and send back data to the server to be stored in InfuxDB database
 * When activated by the server, the heater will maintain the temperature in the room between 17°C and 26°C
 * And the Lamp will be controled by a switch on the dashboard
 * 
 */


#include "networking.h"
#include "sensor.h"
#define DHTpin 5         //connect DHT11 to GPIO5
#define lamp 4           //connect LED to GPIO4 
#define relay 16         //connect Relay to GPIO16(D0)
#define DHTTYPE DHT11    

int now = millis();
int previous = 0;
static int heater_switch = 0;       //switch of heater
static int heater_state = 0;        //state of heater

DHT dht(DHTpin, DHTTYPE);     //Initialise DHT object
char DHT_buffer[40];  

DHT_data data;

//wifi information
char ssd[] = "rasp";
char password[] = "raspserver";

//PubSubClient parameter
WiFiClient wificlient;
char MQTT_Server[] = "10.42.0.1";
int port = 1883;

//subscribe to 2 topic Lamp and Heater
char* topic[] = {"Room01/Lamp/Activated", "Room01/Heater/Activated"};           
unsigned int nb_topic = 2;
char clientID[] = "NodeMCU01";
PubSubClient client(MQTT_Server, port, wificlient);       //Constructor of PubSubClient object


/*-----------------------------Callback function is called when ever a new message arrive------------------------------------*/
void callback(String topic, byte* payload, unsigned int length)
{
  String message;
  int i;
  for(i=0; i<length; i++)
  {
    message += (char)payload[i];              //convert payload to string
  }
  Serial.print("Message arrive: Topic ");
  Serial.print(topic);
  Serial.print(", message ");
  Serial.println(message);
  if(topic == "Room01/Lamp/Activated")
  {
    Serial.print("Changing Room lamp to ");
    if(message == "1")      //ON
    {
      digitalWrite(lamp, HIGH);
      Serial.println("On");
    }
    else if(message == "0")    //OFF
    {
      digitalWrite(lamp, LOW);
      Serial.println("Off");
    }
    else
    {
      Serial.println("Message corrupt");
    }
  }
  
  else if(topic == "Room01/Heater/Activated")
  {
     Serial.print("Changing Room Heater to ");
     if(message == "1")      //ON
     {
       heater_switch = 1;            //allow heater to function
       Serial.println("On");
     }
     else if(message == "0")    //OFF
     {
       heater_switch = 0;            //lock all functional of heater
       digitalWrite(relay, LOW);     //turn of heater
       Serial.println("Off");
     }
     else
     {
       Serial.println("Message corrupt");
     }
  }
}


/*--------------------------------------------SET UP----------------------------------------------------------*/
void setup() {
  pinMode(DHTpin, INPUT);     
  pinMode(lamp, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);                         //lock by default
  
  Serial.begin(115200);
  wifi_connect(ssd, password);                     //connect to wifi
  client.setCallback(callback);
}

/*--------------------------------------------LOOP------------------------------------------------------------*/
void loop() {
  MQTT_connect(client, clientID, topic, nb_topic);
  now = millis();
  if(now-previous >= 30000)
  {
    previous = now;
    if(!read_DHT(dht, &data))     //attemp to read data from DHT11
    {
       Serial.println("Fail to read from HDT11");
       return;                    //break the loop
    }
    Serial.println(heater_state);
    if(heater_switch==1)
    {
      
       if(data.temperature < 23 && !heater_state)             //turn on heater
       {
          digitalWrite(relay, HIGH);
          heater_state = 1;
          client.publish("Room01/Heater/State", "1");        //publish state to topic
          Serial.println("heater on");
       }
       else if(data.temperature > 25 && heater_state)         //turn off heater
       {
          digitalWrite(relay, LOW);
          heater_state = 0;
          client.publish("Room01/Heater/State", "0");         //publish state to topic
          Serial.println("heater off");
       }
      
    }
    //convert DHT data to string
    String buffer;
    buffer += F("{\"temperature\":");
    buffer += String(data.temperature, 3);
    buffer += F(",\"humidity\":");
    buffer += String(data.humidity, 3);
    buffer += F("}");
    buffer.toCharArray(DHT_buffer, 50);
    
    client.publish("Room01/DHT11", DHT_buffer);
    Serial.println(buffer);
  
    /*
    dtostrf(data.temperature, 3, 2, temperature);
    
    dtostrf(data.humidity, 3, 2, humidity);
    client.publish("Room01/Humidity", humidity);
    Serial.print("Temperature: ");
    Serial.println(data.temperature);
    Serial.print("Humidity: ");
    Serial.println(data.humidity);
   
    */
  }
}
