"""Example of a consumer making RPC request
"""
# Standard Imports
import asyncio
import logging
import json
import os
# Third Party Imports
from faststream import FastStream
from huggingface_hub import InferenceClient
from huggingface_hub.inference._generated.types import ChatCompletionOutput
from huggingface_hub.errors import HfHubHTTPError
from requests.exceptions import ConnectionError
# Local Imports
from objects import TGIChatCompletionArgs, QueueResponse
from utils import make_broker_from_env, RABBITMQ_QUEUE


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up FastStream with RabbitMQ
broker = make_broker_from_env()
app = FastStream(broker)

# Set up TGI client
TGI_PORT = os.getenv("TGI_PORT", "8080")
TGI_URL = os.getenv("TGI_URL", "localhost")
TGI_CLIENT = InferenceClient(f"http://{TGI_URL}:{TGI_PORT}/v1/chat/completions")


@broker.subscriber(RABBITMQ_QUEUE)
async def handle_message(message: TGIChatCompletionArgs) -> QueueResponse:
    try:
        response: ChatCompletionOutput = TGI_CLIENT.chat_completion(**message.model_dump())
    except HfHubHTTPError as e:
        logger.warning(f"Got HfHubHTTPError error {e}, returning error code 422")
        return QueueResponse(
            error_code=422,
            message=str(e)
        )
    except ConnectionError as e:
        logger.warning(f"Got ConnectionError error {e}, returning error code 503")
        return QueueResponse(
            error_code=503,
            message=str(e)
        )
    return QueueResponse(
        error_code=200,
        message=json.dumps(response.__dict__)
    )


@app.on_startup
async def setup_queue() -> None:
    await broker.connect()
    await broker.declare_queue(RABBITMQ_QUEUE)


async def main() -> None:
    await app.run()


if __name__ == "__main__":
    asyncio.run(app.run())
