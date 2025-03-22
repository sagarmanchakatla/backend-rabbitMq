# Distributed CSV Processing System

A backend service that integrates multiple components for asynchronous CSV processing with distributed workers and real-time dashboard updates.

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Design Decisions and Trade-offs](#design-decisions-and-trade-offs)
- [Testing](#testing)
- [Hidden Challenge Solution](#hidden-challenge-solution)

## Overview

This system allows for asynchronous processing of CSV data through a combination of:

1. A Flask API for HTTP-based data access
2. RabbitMQ for reliable message distribution
3. Distributed worker nodes for parallel CSV processing
4. Flask-SocketIO for real-time updates to clients
5. Streamlit dashboard for visualization

## Technologies Used

- **RabbitMQ**: For asynchronous message distribution
- **Flask**: For HTTP API endpoints
- **Flask-SocketIO**: For real-time client notifications
- **Python CSV libraries**: For CSV data processing
- **Streamlit**: For data visualization dashboard
- **Pandas**: For data manipulation
- **Pika**: For RabbitMQ integration

## Project Structure

```
project/
├── flask_app/
│   ├── app.py            # Main Flask application with SocketIO integration
│   └── data.csv          # Shared CSV file
├── worker/
│   └── worker.py         # Distributed worker implementation
├── client/
│   └── producer.py       # Example client to send CSV tasks
├── dashboard/
│   └── streamlit_app.py  # Streamlit dashboard
└── README.md             # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- RabbitMQ server
- Required Python packages

### 1. Install Dependencies

```bash
pip install flask flask-socketio pika pandas streamlit python-socketio requests
```

### 2. Configure RabbitMQ

Ensure RabbitMQ server is running locally:

```bash
# Start RabbitMQ server (Debian/Ubuntu)
sudo service rabbitmq-server start

# For macOS (with Homebrew)
brew services start rabbitmq

# Using Docker
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

### 3. Running the System

#### Start the Flask API Server

```bash
cd flask_app
python app.py
```

This will start the Flask server on http://127.0.0.1:5000.

#### Start Worker Nodes

Open one or more new terminals to start worker nodes:

```bash
cd worker
python worker.py
```

You can start multiple worker instances to scale out processing.

#### Launch the Streamlit Dashboard

In a new terminal:

```bash
cd dashboard
streamlit run streamlit_app.py
```

This will open the dashboard in your default web browser.

#### Sending CSV Tasks

Use the producer to send sample CSV tasks:

```bash
cd client
python producer.py
```

## Design Decisions and Trade-offs

### Message Queue Architecture

I implemented a message queue architecture using RabbitMQ to decouple CSV processing from the main application. This provides several advantages:

1. **Scalability**: Worker nodes can be added or removed without changing the core system
2. **Reliability**: Messages persist in the queue even if workers go offline
3. **Load Balancing**: Work is naturally distributed among available workers

### Shared CSV File

Instead of maintaining state in memory, the system uses a shared CSV file as a simple "database". This approach:

- Provides persistence across restarts
- Simplifies worker implementation
- Allows multiple components to access the same data

Trade-off: This approach has limitations with concurrent access and would need to be replaced with a proper database in a production environment.

### Real-time Updates

The system implements real-time updates using Flask-SocketIO, which:

- Pushes updates to connected clients immediately
- Reduces the need for polling
- Provides a better user experience

Trade-off: Requires maintaining socket connections, which can be resource-intensive with many clients.

### Worker Design

Workers are designed to:

- Process specific operations (add, delete) on CSV data
- Work independently from the main system
- Scale horizontally by adding more instances

Trade-off: The current design has workers directly modifying the shared CSV file, which could lead to race conditions in high-concurrency scenarios.

## Testing

### Flask API Testing

The Flask API endpoints were tested using:

- Manual testing with curl commands
- Verification of responses and status codes

Example test:

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test data endpoint
curl http://localhost:5000/data
```

### RabbitMQ Integration Testing

RabbitMQ functionality was tested by:

- Sending test messages through the producer
- Verifying message receipt by workers
- Checking queue statistics in RabbitMQ management interface

### Distributed Worker Testing

Worker nodes were tested by:

- Running multiple worker instances simultaneously
- Sending batches of messages to verify load distribution
- Verifying all messages were processed correctly

### Streamlit Dashboard Testing

The dashboard was tested by:

- Verifying initial data load
- Testing real-time updates when CSV data changes
- Checking UI responsiveness and layout

## Hidden Challenge Solution

### Message Idempotency and Data Consistency

To address the hidden challenge of ensuring data consistency across distributed workers and handling potential message duplication, I implemented:

1. **Atomic Operations**: Each worker performs atomic operations (add/delete) that can be safely repeated without side effects
2. **Operation-based Messages**: Instead of sending raw CSV data, messages contain specific operations to perform (add row, delete row)
3. **File-based Coordination**: Using a shared CSV file as the single source of truth prevents data inconsistency
4. **Event-driven Updates**: After processing, the system emits SocketIO events to ensure all clients have the latest data

This approach ensures that:

- Duplicate messages don't create duplicate data
- Operations are applied consistently regardless of which worker processes them
- All components (API, workers, dashboard) maintain a consistent view of the data
