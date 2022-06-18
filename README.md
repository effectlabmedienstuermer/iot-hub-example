# iot-hub-example
Example for sending telemetry data from a client to an IoT hub

## Getting everything to run
Obtain a device connection string by going to the Azure portal and running 
```
az iot hub device-identity create --device-id <myDeviceId> --hub-name effectlab-test-iot-hub
az iot hub device-identity connection-string show --device-id <myDeviceId> --hub-name effectlab-test-iot-hub -o table
```
Place the connection string in a file called `connection-string.txt` in the same folder as the Python scripts.

Tested with Python 3.8.10, dependencies are in the `requirements.txt` file. Then simply run 
`python3 simulated_temp_sensor.py`.

