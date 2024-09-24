import platform
import socket
import getpass
import paho.mqtt.client as mqtt
import json
from pynput import mouse
from datetime import datetime, timedelta
import time

# Global variables to track last mouse movement and connected students
last_mouse_movement = None
students_last_movement = {}
connected_students = set()
last_update_timestamp = None

# Time window to check recent mouse movement (i.e., since the last informative update)
MOVEMENT_THRESHOLD_SECONDS = 5

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

# Collect informative namespace: total connected and active students
def generate_informative_namespace():
    global last_update_timestamp
    last_update_timestamp = datetime.now().isoformat()

    # Count students who moved their mouse since the last update
    now = datetime.now()
    active_students_count = sum(1 for timestamp in students_last_movement.values()
                                if now - timestamp <= timedelta(seconds=MOVEMENT_THRESHOLD_SECONDS))

    informative_info = {
        'total_connected_students': len(connected_students),
        'active_students': active_students_count,  # Total number of active students
        'last_update': last_update_timestamp
    }

    # Debug output for better tracking
    print(f"[DEBUG] Informative Namespace - Connected Students: {len(connected_students)}, Active Students: {active_students_count}")
    return informative_info

# Connect and publish to MQTT broker
def publish_namespace(client, namespace, topic_suffix):
    namespace_json = json.dumps(namespace)
    full_topic = f"{student_topic}/{topic_suffix}"
    result = client.publish(full_topic, namespace_json)

    # Check the result of the publish action
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Published to {full_topic}: {namespace_json}")
    else:
        print(f"Failed to publish to {full_topic}: {result.rc}")

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to all students under the "uns/#" topic hierarchy
    client.subscribe("uns/#")

def on_message(client, userdata, msg):
    global connected_students
    global students_last_movement

    payload = json.loads(msg.payload.decode())
    topic_parts = msg.topic.split('/')
    
    # Extract student identifier based on the topic format: uns/(country code)/(province/state)/(city)/(initials)
    student_id = "/".join(topic_parts[1:5])  # Country code, state/province, city, initials

    # Add student to the connected students set
    connected_students.add(student_id)

    # If it's a functional namespace, update their last mouse movement timestamp
    if 'functional' in msg.topic and 'last_mouse_movement' in payload:
        movement_time = payload.get('last_mouse_movement')
        if movement_time:
            # Update the student's last mouse movement
            students_last_movement[student_id] = datetime.now()
            print(f"[DEBUG] Student {student_id} last mouse movement at {movement_time}")

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
    # Get student-specific topic based on their location and initials
    country_code = 'usa'  # Example: Replace with actual country code
    state_code = 'tx'     # Example: Replace with actual state/province code
    city = 'dallas'       # Example: Replace with actual city
    initials = 'wdr'      # Example: Replace with actual initials
    student_topic = f"uns/{country_code}/{state_code}/{city}/{initials}"

    # Start mouse movement listener
    start_mouse_listener()

    # Generate different types of namespaces
    descriptive_namespace = generate_descriptive_namespace()
    functional_namespace = generate_functional_namespace()

    print(f"Generated Descriptive Namespace: {descriptive_namespace}")
    print(f"Generated Functional Namespace: {functional_namespace}")

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

    # Continuously update the functional and informative namespace and publish every 5 seconds
    while True:
        # Update functional namespace with last mouse movement timestamp
        functional_namespace = generate_functional_namespace()
        publish_namespace(client, functional_namespace, "functional")

        # Generate and publish informative namespace
        informative_namespace = generate_informative_namespace()
        publish_namespace(client, informative_namespace, "informative")

        time.sleep(5)
