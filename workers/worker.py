import pika
import json
import pandas as pd
import os
import requests

# Path to the CSV file
CSV_FILE = '../flask_app/data.csv'

def process_csv_task(operation, data):
    df = pd.read_csv(CSV_FILE)
    if operation == "add":
        # Add a new row to the CSV
        new_row = pd.DataFrame([data])  
        df = pd.concat([df, new_row], ignore_index=True)
    elif operation == "delete":
        # Delete a row by name
        df = df[df['name'] != data['name']]
    # Save the updated CSV
    df.to_csv(CSV_FILE, index=False)

def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    operation = message.get("operation")
    data = message.get("data")
    print(f" [x] Received {operation} task")
    process_csv_task(operation, data)
    # Send the updated CSV data back to the Flask app
    # df = pd.read_csv(CSV_FILE)
    # requests.post('http://127.0.0.1:5000/update', json=df.to_dict(orient='records'))

# Start consuming messages
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='csv_tasks')
channel.basic_consume(queue='csv_tasks', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for CSV tasks. To exit press CTRL+C')
channel.start_consuming()