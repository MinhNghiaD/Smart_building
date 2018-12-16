

#ifndef SENSOR_H
#define SENSOR_H
#include <DHT.h>

/*----------------------------------DHT11--------------------------------------*/
//data from DHT
struct DHT_data
{
  	float temperature;
  	float humidity;
};
int read_DHT(DHT dht, DHT_data* data);		//read data from DHT sensor into DHT_data object, return 1 if success, 0 if fail to read from sensor

#endif


int read_DHT(DHT dht, DHT_data* data)
{
	//read data from DHT
	data->temperature = dht.readTemperature();
  	data->humidity = dht.readHumidity();

	//error check 
  	if(isnan(data->temperature) || isnan(data->humidity))
  	{
   		return 0;                   	//if false return 0
  	}
  	return 1;                        	//if success return 1
}



