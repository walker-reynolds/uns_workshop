# Unified Namespace MQTT Workshop

This repository contains the code for a workshop that demonstrates how to use Python and MQTT to create a unified namespace. The workshop teaches how to collect system information, track real-time activity, and publish data to an MQTT broker. The project is divided into three steps.

## Workshop Overview

The workshop covers the following concepts:

1. **Descriptive Namespace**: Collects system, user, and location information.
2. **Functional Namespace**: Allows students to define custom data and track real-time mouse movements.
3. **Informative Namespace**: Aggregates data to show connected students and real-time activity.

### Prerequisites

Ensure you have the following installed:

- **Python 3.x**
- **Pip** for installing Python packages
- **An MQTT Broker** to connect and publish data

### Steps in the Workshop

This workshop consists of three steps:

---

### Step 1: Basic MQTT Setup

In this step, students will:

- Set up an MQTT client in Python.
- Create descriptive, functional, and informative namespaces.
- Publish these namespaces to an MQTT broker.

---

### Step 2: Dynamic Functional Namespace

This step adds the following functionality:

- Track real-time mouse movements using Python.
- Update and publish the functional namespace dynamically with the timestamp of the last mouse movement.

---

### Step 3: Managing Connected and Active Students

In the final step, students will:

- Track connected students by monitoring their functional namespaces.
- Count how many students have moved their mouse within a given time window.
- Publish aggregated data, including the number of connected and active students, in the informative namespace.

---



