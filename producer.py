# Standard Imports
import asyncio
import logging
import json
import argparse
# Third Party Imports
from faststream.rabbit import RabbitMessage
# Local Imports
from objects import TGIChatCompletionArgs, QueueResponse
from utils import make_broker_from_env, RABBITMQ_QUEUE_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up FastStream with RabbitMQ
broker = make_broker_from_env()


async def run_request(msg: TGIChatCompletionArgs, semaphore: asyncio.Semaphore) -> None:
   broker = make_broker_from_env()
   await broker.connect()
   async with semaphore:
      output: RabbitMessage = await broker.request(
         msg,
         queue=RABBITMQ_QUEUE_NAME,
      )
   response_body = QueueResponse(**json.loads(output.body))
   if response_body.error_code == 200:
      try:
         response_dict = json.loads(response_body.message)
         logger.info(f"Success! Response: {response_dict}")
      except json.JSONDecodeError:
         logger.error(f"Could not decode body of {response_body.message}")
   else:
      logger.error("Failed! Response:", response_body.message)
   await broker.close()


async def submit_requests(workers: int, messages: int) -> None:
   semaphore = asyncio.Semaphore(workers)
   await broker.connect()
   message_request_list: list[TGIChatCompletionArgs] = [
      TGIChatCompletionArgs(messages=[{"role": "user", "content": f"What is 1 + {i}"}])
      for i in range(1, messages+1)
   ]
   tasks = [run_request(request, semaphore) for request in message_request_list]
   _ = await asyncio.gather(*tasks)
   await broker.close()
   pass


def main():
   parser = argparse.ArgumentParser()
   parser.add_argument('-w', '--workers', type=int, default=None, help='Number of workers to use', required=False)
   parser.add_argument('-m', '--messages', type=int, default=1000, help='Number of messages to send')
   args = parser.parse_args()

   number_of_messages = int(args.messages)
   num_of_workers = int(args.workers) if args.workers is not None else number_of_messages

   asyncio.run(submit_requests(num_of_workers, number_of_messages))


if __name__ == "__main__":
   main()
