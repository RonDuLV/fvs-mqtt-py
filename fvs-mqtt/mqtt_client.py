import os
import time
import threading
import paho.mqtt.client as mqtt

# Define MQTT broker details
BROKER = '192.168.0.96'
PORT = 1883
TOPIC = 'sensor_data'
fifo_path = "/home/root/fvs-mqtt/mqtt_pipe"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def monitor_sensor(fifo_path, topic):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT, 60)

    client.loop_start()  # Start the loop in a non-blocking way

    last_line = ""
    while True:
        with open(fifo_path, 'r') as fifo:
            line = fifo.readline().strip()
            if line != last_line:
                last_line = line
                temperature, mode, status = line.split(',')
                payload = {
                    'temperature': temperature,
                    'mode': mode,
                    'status': status
                }
                print("mqtt Python received from pipe {}".format(temperature))
                client.publish(TOPIC, str(payload))
            # client.loop()  # Manually call loop to process network traffic and callbacks
        time.sleep(1)
        
    client.loop_stop()  # This will only be reached if the

if __name__ == "__main__":
    threads = []

    # Create threads for each sensor
    t1 = threading.Thread(target=monitor_sensor, args=(fifo_path, "sensor_data"))
    # t2 = threading.Thread(target=monitor_sensor, args=("/tmp/sensor2_fifo", "sensor2/data"))
    # t3 = threading.Thread(target=monitor_sensor, args=("/tmp/sensor3_fifo", "sensor3/data"))

    threads.append(t1)
    # threads.append(t2)
    # threads.append(t3)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()