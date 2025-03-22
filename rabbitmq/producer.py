import pika
import json

def send_csv_task(operation, data=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='csv_tasks')
    # Send a message with the operation and data
    message = json.dumps({"operation": operation, "data": data})
    channel.basic_publish(exchange='', routing_key='csv_tasks', body=message)
    print(f" [x] Sent {operation} task")
    connection.close()

# Example usage
if __name__ == '__main__':
    # Add a new row
    new_row = {"name": "TEST1", "age": "21", "city": "Pune"}
    send_csv_task("add", new_row)

    # Delete a row by name
    # send_csv_task("delete", {"name": "Siddhi"})