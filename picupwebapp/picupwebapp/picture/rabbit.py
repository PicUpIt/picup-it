import pika
from django.conf import settings

def get_rabbit_connection():
    """Get RabbitMQ connection.
    """
    if settings.DEBUG:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',port=5672))
    else:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5673))
    return connection
    
    
def get_rabbit_channel():
    """Get RabbitMQ Channel.
    """
    connection = get_rabbit_connection()
    channel = connection.channel()
    return channel

