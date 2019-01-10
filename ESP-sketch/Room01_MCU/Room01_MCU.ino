/*
 * Created 20/11/2018 by Minh Nghia Duong
 * 
 * This Ketch yse function in network.h head file to connect to Wifi and MQTT server and functions in sensor.h to take data from sensor
 * It controls the temperature, humidity and light in the room
 * The NodeMCU will reveive the data from DHT11 sensor and send back data to the server to be stored in InfuxDB database
 * When activated by the server, the heater will maintain the temperature in the room between 17°C and 26°C if there is a presence in the room
 * And the Lamp will be controled by a switch on the dashboard
 * 
 */


#include "networking.h"
#include "sensor.h"
#define DHTpin 5         //connect DHT11 to GPIO5
#define lamp 4           //connect LED to GPIO4 
#define relay 16         //connect Relay to GPIO16(D0)
#define PIR_sensor 0     //connect PIR sensor to pin GPIO0
#define DHTTYPE DHT11    

int now = millis();                 //started time
int previous = 0;
static int lamp_switch = 0;
static int heater_switch = 0;       //switch of heater ----> Command from server ON or OFF
static int heater_state = 0;        //state of heater  ----> State of Heater ON or OFF

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
char clientID[] = "SC-NodeMCU01";                         //Restrict Client ID by prefix SC-
char mqtt_username[] = "nodemcu";                              //login and password for mosquitto broker
char mqtt_password[] = "esp8266";
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
      lamp_switch = 1;
      Serial.println("On");
    }
    else if(message == "0")    //OFF
    {
      digitalWrite(lamp, LOW);
      lamp_switch = 0;
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
  //set up input
  pinMode(DHTpin, INPUT);     
  pinMode(PIR_sensor, INPUT);

  //set up output
  pinMode(lamp, OUTPUT);
  pinMode(relay, OUTPUT);
  digitalWrite(relay, LOW);                         //lock by default
  
  Serial.begin(115200);
  wifi_connect(ssd, password);                     //connect to wifi
  client.setCallback(callback);
}

/*--------------------------------------------LOOP------------------------------------------------------------*/
void loop() {
  MQTT_connect(client, clientID, mqtt_username, mqtt_password, topic, nb_topic);        //verify connection with MQTT broker
  now = millis();
  int motion = digitalRead(PIR_sensor);         //motion detection
    
    //lamp reaction when motion detected
   if(motion == HIGH)
   {
     if(lamp_switch == 1)
     {
       digitalWrite(lamp, HIGH);
     }
     if(now-previous >= 5000)
     {
        client.publish("Room01/Motion", "1");        //publish state to topic in after time interval 
     }
     
   }
   else if(now-previous >= 5000)
   {
     digitalWrite(lamp, LOW);
     client.publish("Room01/Motion", "0");        //publish state to topic in after time interval
   }
    
  if(now-previous >= 5000)                               //idle in 30 senconds
  {
    previous = now;               //reset clock
    if(!read_DHT(dht, &data))     //attemp to read data from DHT11
    {
       Serial.println("Fail to read from HDT11");
       return;                                    //if false to read from sensor -----> break the loop
    }
    
    Serial.println(heater_state);
    
    if(heater_switch==1)      //only when turned on by server
    {
         if(data.temperature < 23 && !heater_state && motion==HIGH)             //turn on heater if it's off and temperature lower than 23°C and there is presence in the room
         {
            digitalWrite(relay, HIGH);
            heater_state = 1;
            client.publish("Room01/Heater/State", "1");        //publish heater state to topic
            Serial.println("heater on");
         }
         else if((data.temperature > 25 || motion==LOW) && heater_state)         //turn off heater if it's on and temperature higher than 25°C or there is no presence in the room
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
  }
}
