import pika

def send_csv_task(csv_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='csv_tasks')
    channel.basic_publish(exchange='', routing_key='csv_tasks', body=csv_data)
    print(" [x] Sent CSV task")
    connection.close()

# Example usage
if __name__ == '__main__':
    csv_data = """name,age,city
John,23,New York
Jane,29,Los Angeles"""
    send_csv_task(csv_data)