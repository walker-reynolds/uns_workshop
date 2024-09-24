# Unified Namespace: UNS with MQTT Workshop

This repository contains the code for a workshop that demonstrates how to use Python and MQTT to create a unified namespace. The workshop teaches how to collect system information, track real-time activity, and publish data to an MQTT broker. The workshop is broken into three sessions and each session's project is divided into three steps.

## Workshop Overview for Session 1

All necessary code for Session 1 can be found in [Session 1 Folder](https://github.com/walker-reynolds/uns_workshop/tree/main/session1)

The technical lesson covers the following concepts:

1. **Descriptive Namespace**: Collects system, user, and location information.
2. **Functional Namespace**: Allows students to define custom data and track real-time mouse movements.
3. **Informative Namespace**: Aggregates data to show connected students and real-time activity.

The technical lesson is broken into three steps.  The code for each step is located in separate python files in the repository.  Students will create a new python project using PyCharm (or VSCode) called 'unsworkshop'.  

1. Create requirements.txt (pre-requisites will be listed here)
2. Create main.py (step code will go here)
3. In the terminal, run ```pip install -r requirements.txt```
4. Connect to MQTT Broker using **MQTT Explorer**
5. For each step, update the code in main.py with the corresponding code in step1.py, step2.py and step3.py
6. Each step requires configuration in the code

### Prerequisites For Session 1

Ensure you have the following software installed:

- **Python 3.x**: The programming language used to write and execute the scripts.
- **Pip**: The package installer for Python, used to install required libraries.
- **PyCharm Community Edition**: A free Python IDE for writing and managing Python code.
- **MQTT Explorer**: A GUI tool for monitoring and debugging MQTT traffic, useful for observing topics and messages published by the students.

### Steps in the Workshop Session 1

This workshop consists of three steps:

---

## Step 1: Basic MQTT Setup

In this step, we set up a basic MQTT client using Python and `paho-mqtt`. The student will:

- Create and publish three types of namespaces:
  - **Descriptive Namespace**: Collects system, user, and location information.
  - **Functional Namespace**: Contains user-defined data, such as process status and a timestamp.
  - **Informative Namespace**: Holds general system information such as status messages and uptime.
  
- Connect to the MQTT broker using the provided credentials.
- Publish the descriptive, functional, and informative namespaces to the student's unique MQTT topic.
- Subscribe and listen for any incoming messages on the specified topic.

**Key Features:**
- Generates and publishes information about the user's system and custom data to a topic structure based on `uns/{country_code}/{state_code}/{city}/{initials}`.
- Subscribes to the topic and processes any incoming messages.

**MQTT Topic Structure:**
The student will publish to a unique root topic:
example: uns/usa/tx/dallas/wdr

Namespaces will be published under subtopics like:
- uns/usa/tx/dallas/wdr/descriptive 
- uns/usa/tx/dallas/wdr/functional 
- uns/usa/tx/dallas/wdr/informative

---

## Step 2: Dynamic Functional Namespace with Mouse Tracking

In this step, we extend the functionality from Step 1 by introducing **mouse tracking**. The student will:

- Use Python's `pynput` library to track real-time mouse movements.
- Dynamically update the **functional namespace** to include the timestamp of the last mouse movement.
- Continuously publish the updated functional namespace every 5 seconds to the MQTT broker.

### Key Features:
- **Mouse Tracking**: Every time the mouse is moved, the timestamp of the movement is recorded.
- **Dynamic Functional Namespace**: The functional namespace now includes the `last_mouse_movement` timestamp, which updates in real-time.
- **Continuous Publishing**: The functional namespace is re-published every 5 seconds, reflecting the most recent mouse movement.
  
### MQTT Topic Structure:
The student will continue to publish to a unique root topic:
uns/usa/tx/dallas/wdr

Namespaces will be published under subtopics like:
- uns/usa/tx/dallas/wdr/descriptive
- uns/usa/tx/dallas/wdr/functional
- uns/usa/tx/dallas/wdr/informative


### How It Works:
1. **Descriptive Namespace**: Collects system and user information, similar to Step 1.
2. **Functional Namespace**: Updated dynamically with the last mouse movement timestamp.
3. **Informative Namespace**: A placeholder for system messages, unchanged from Step 1.

In this step, the script continues to handle MQTT communication and monitor mouse movements in real-time. Every 5 seconds, the functional namespace is updated and published, showing the latest interaction.

---

### Step 3: Managing Connected and Active Students

In the final step, students will:

- Track connected students by monitoring their functional namespaces.
- Count how many students have moved their mouse within a given time window.
- Publish aggregated data, including the number of connected and active students, in the informative namespace.

---

### Software Setup Instructions

1. **Python 3.x**: Download and install Python 3 from the [official website](https://www.python.org/downloads/). Ensure `pip` is also installed with Python.

2. **PyCharm Community Edition**: Download and install PyCharm from the [JetBrains website](https://www.jetbrains.com/pycharm/download/). This will be used as the integrated development environment (IDE) for writing, running, and debugging Python code.

3. **MQTT Explorer**: Download and install MQTT Explorer from the [official site](https://mqtt-explorer.com/). This will help you visualize the topics and messages exchanged during the workshop.

---

### MQTT Topics

Each student will publish to a unique topic using the following format:

uns/{country_code}/{state_code}/{city}/{student_initials}/
For example: uns/usa/tx/dallas/wdr


Namespaces will be published under subtopics like `descriptive`, `functional`, and `informative`.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This workshop is designed to teach students how to use Python and MQTT to create real-time, distributed systems that collect and share data in a unified namespace.

