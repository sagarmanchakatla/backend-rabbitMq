import pika
import csv
import io
import requests

def process_csv(csv_data):
    # Parse CSV data into a list of dictionaries
    csv_file = io.StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    return list(reader)

def callback(ch, method, properties, body):
    csv_data = body.decode('utf-8')
    print(" [x] Received CSV task")
    processed_data = process_csv(csv_data)
    print("Processed Data:", processed_data)
    # Send processed data back to master via API call
    requests.post('http://127.0.0.1:5000/update', json=processed_data)

# Start consuming messages
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='csv_tasks')
channel.basic_consume(queue='csv_tasks', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for CSV tasks. To exit press CTRL+C')
channel.start_consuming()