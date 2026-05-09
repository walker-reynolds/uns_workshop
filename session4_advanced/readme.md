# Advanced UNS Workshop - Session 1

Welcome to Session 4 of the Advanced Unified Namespace (UNS) Workshop. This session introduces an OpenAI-powered chatbot designed to interact with a Unified Namespace (UNS) using MQTT. Additionally, this session includes resources for restoring an Ignition gateway, tags, and projects. Below is a description of the provided files and their purpose.

---

## Files Overview

### 1. **`main.py`**
   - **Purpose**: This is the entry point for the chatbot application. It launches a GUI-based chatbot that allows users to ask questions about data in the UNS.
   - **Key Features**:
     - Uses `Tkinter` to create a user-friendly interface.
     - Subscribes to MQTT topics via the `mqtt_client.py` script.
     - Fetches the latest data from the MQTT broker to provide context-aware responses using OpenAI's GPT model.

### 2. **`mqtt_client.py`**
   - **Purpose**: Handles communication with the MQTT broker and caches incoming data.
   - **Key Features**:
     - Subscribes to topics defined in `config.py`.
     - Updates a local cache with the latest data from the UNS.
     - Returns the data cache to `main.py` for chatbot queries.

### 3. **`openai_client.py`**
   - **Purpose**: Sends user questions and UNS data to OpenAI's GPT model to generate intelligent responses.
   - **Key Features**:
     - Constructs a prompt combining the user's question and cached data.
     - Configures and sends requests to OpenAI's API using the `OPENAI_API_KEY` from `config.py`.

### 4. **`data_cache.py`**
   - **Purpose**: Implements a simple in-memory cache to store the most recent MQTT messages for quick retrieval.
   - **Key Features**:
     - Provides methods to update and retrieve cached data.
     - Designed for lightweight and efficient data handling.

### 5. **`config.py`**
   - **Purpose**: Stores configuration details for the MQTT broker and OpenAI API.
   - **Key Features**:
     - Defines MQTT broker address, port, and topic subscriptions.
     - Includes a placeholder for the OpenAI API key (to be replaced with your key).

   #### Setting Up Your OpenAI API Key
   - To use the chatbot, you need an OpenAI API key. Follow these steps:
     1. Visit the [OpenAI API Key page](https://platform.openai.com/signup/).
     2. Sign up for an account or log in if you already have one.
     3. Navigate to the API Keys section and generate a new key.
     4. Copy the generated key.
     5. Open the `config.py` file in a text editor.
     6. Replace the placeholder on line 4:
        ```python
        OPENAI_API_KEY = ''
        ```
        with your actual API key:
        ```python
        OPENAI_API_KEY = 'your_api_key_here'
        ```
     7. Save the file.
   - Note: Ensure you have sufficient credits in your OpenAI account to use the API.

### 6. **`tags4.json`**
   - **Purpose**: A backup of the tags for the Ignition project containing the simulator.
   - **How to Use**:
     - This file can be imported into your Ignition instance to restore the pre-configured tags for the UNS simulator.
     - Follow these steps:
       1. Open the Ignition Designer.
       2. Navigate to the `Tag Browser`.
       3. Right-click and select `Import Tags`.
       4. Choose the `tags4.json` file and confirm the import.

### 7. **`unsworkshop_20250122180245.zip`**
   - **Purpose**: A backup of the Ignition project for the UNS Workshop, designed for Ignition version 8.1.43 and higher.
   - **How to Use**:
     - Restore this project in Ignition to gain access to all pre-configured settings, tags, and views.
     - Steps to restore:
       1. Log in to the Ignition Gateway Web Interface.
       2. Navigate to `Config` > `Projects` > `Restore`.
       3. Upload the `unsworkshop_20250122180245.zip` file and confirm.
       4. Once restored, open the Ignition Designer and ensure the project is properly loaded.

---

## Chatbot Features

- **Real-Time Data Integration**: The chatbot leverages data from the UNS to provide contextually aware answers to user questions.
- **Customizable MQTT Topics**: Modify the `MQTT_TOPICS` in `config.py` to subscribe to specific namespaces relevant to your operations.
- **Interactive GUI**: A clean and intuitive interface for users to interact with the chatbot.

---

## Getting Started

### Prerequisites
- Python 3.8 or later.
- Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- An active OpenAI API key.
- Access to an MQTT broker.

### Configuration
- Update the `config.py` file with your MQTT broker details and OpenAI API key.

### Run the Application
- Start the chatbot by running:
  ```bash
  python main.py
  ```

---

## Ignition Gateway Resources

This directory includes resources for restoring an Ignition gateway, including pre-configured tags (`tags4.json`) and the UNS Workshop project (`unsworkshop_20250122180245.zip`). Follow the instructions in the **Files Overview** section to import these files into your Ignition system.

---

## Feedback

We hope you find this session informative and engaging. Please share your feedback and questions during the workshop.

---

Stay tuned for additional documentation updates.

