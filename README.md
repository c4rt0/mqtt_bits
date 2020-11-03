# mqtt_bits

A collection of bits of code which caused me a bit of a headache related to issue solving. 
1. File 
    */MQTT/mqtt_client_with_loop.py 
    I used while loop instead of if statement, so same message was copied across a whole array, instead of stored as a single message mqtt client this way created a full (10x) array and presented it in terminal, every time mqtt message was published by the mqttBroker.