import platform
import socket
import getpass
import paho.mqtt.client as mqtt
import json

# Set the root topic (each student should customize this)
ROOT_TOPIC = "uns/usa/tx/dallas/wdr"

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
    # The student will define what goes into this functional namespace
    functional_info = {
        'process': 'example_process',
        'status': 'running',
        'timestamp': '2024-09-24T14:30:00Z'
    }
    return functional_info

# Collect informative namespace: user-defined JSON
def generate_informative_namespace():
    # The student will define what goes into this informative namespace
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
    client.publish(full_topic, namespace_json)
    print(f"Published to {full_topic}: {namespace_json}")

# MQTT callbacks (for subscribing)
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(f"{ROOT_TOPIC}/#")  # Subscribe to the student's unique topic

def on_message(client, userdata, msg):
    print(f"Received message from {msg.topic}: {msg.payload.decode()}")

# Main program
if __name__ == "__main__":
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

    # Publish namespaces
    publish_namespace(client, descriptive_namespace, "descriptive")
    publish_namespace(client, functional_namespace, "functional")
    publish_namespace(client, informative_namespace, "informative")

    # Loop to process network traffic and consume messages
    client.loop_forever()
