# Standard Imports
import os
# Third Party Imports
from faststream.rabbit import RabbitBroker, RabbitQueue


RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME", "test")
RABBITMQ_QUEUE = RabbitQueue(
    name=RABBITMQ_QUEUE_NAME,
    durable=True
)

def make_broker_from_env() -> RabbitBroker:
    """Make a broker from env vars
    """
    return RabbitBroker(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_URL}:{RABBITMQ_PORT}")
