import platform
import socket
import getpass
import paho.mqtt.client as mqtt
import json
from pynput import mouse
from datetime import datetime
import time

# Set the root topic (each student should customize this)
ROOT_TOPIC = "uns/usa/tx/dallas/wdr"

# Global variable to track the last mouse movement timestamp
last_mouse_movement = None


# Collect descriptive namespace: user, system, and location information
def generate_descriptive_namespace():
    descriptive_info = {
        'username': getpass.getuser(),
        'system': platform.system(),
        'release': platform.release(),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname()),
        'location': 'Dallas, TX'  # Replace with actual location if available
    }
    return descriptive_info


# Collect functional namespace: user-defined JSON
def generate_functional_namespace():
    functional_info = {
        'process': 'mouse_tracking',
        'status': 'running',
        'last_mouse_movement': last_mouse_movement  # Tracks the last mouse movement timestamp
    }
    return functional_info


# Collect informative namespace: user-defined JSON
def generate_informative_namespace():
    informative_info = {
        'message': 'System running smoothly',
        'alerts': [],
        'uptime': '24 hours'
    }
    return informative_info


# Connect and publish to MQTT broker
def publish_namespace(client, namespace, topic_suffix):
    namespace_json = json.dumps(namespace)
    full_topic = f"{ROOT_TOPIC}/{topic_suffix}"
    result = client.publish(full_topic, namespace_json)

    # Check the result of the publish action
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Published to {full_topic}: {namespace_json}")
    else:
        print(f"Failed to publish to {full_topic}: {result.rc}")


# MQTT callbacks (for subscribing)
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(f"{ROOT_TOPIC}/#")  # Subscribe to the student's unique topic


def on_message(client, userdata, msg):
    print(f"Received message from {msg.topic}: {msg.payload.decode()}")


# Mouse movement listener to track the timestamp of the last movement
def on_move(x, y):
    global last_mouse_movement
    last_mouse_movement = datetime.now().isoformat()  # Update with the current timestamp
    print(f"Mouse moved at {last_mouse_movement}")


def start_mouse_listener():
    listener = mouse.Listener(on_move=on_move)
    listener.start()


# Main program
if __name__ == "__main__":
    # Start mouse movement listener
    start_mouse_listener()

    # Generate different types of namespaces
    descriptive_namespace = generate_descriptive_namespace()
    functional_namespace = generate_functional_namespace()
    informative_namespace = generate_informative_namespace()

    print(f"Generated Descriptive Namespace: {descriptive_namespace}")
    print(f"Generated Functional Namespace: {functional_namespace}")
    print(f"Generated Informative Namespace: {informative_namespace}")

    # MQTT client setup
    mqtt_broker = "broker_address"
    mqtt_port = 1883  # Use 8883 for TLS

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)

    # Start the MQTT loop to process network traffic in the background
    client.loop_start()

    # Publish namespaces initially
    publish_namespace(client, descriptive_namespace, "descriptive")
    publish_namespace(client, functional_namespace, "functional")
    publish_namespace(client, informative_namespace, "informative")

    # Continuously update the functional namespace and publish every 5 seconds
    while True:
        functional_namespace = generate_functional_namespace()
        publish_namespace(client, functional_namespace, "functional")
        time.sleep(5)
