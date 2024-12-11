# TGI FastStream
This project aims to create a proof of concept for setting up an intermediate service using [FastStream](https://github.com/airtai/faststream). It facilitates the passing of RPC requests from a [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server) broker to a [Text Generation Inference](https://github.com/huggingface/text-generation-inference) (TGI) server. This architecture allows for efficient utilization of a horizontally scalable TGI through a simple sidecar service.

## Requirements
To run this proof of concept, ensure you have the following:
- A machine equipped with an <strong>Nvidia GPU</strong>
- <strong>Docker</strong> installed
- <strong>Python</strong> version <strong>3.10</strong> or higher
## Setup
Copy the example environment file:

```bash
cp sample.env .env
```

Install required dependencies:
```bash
# Create a virtual environment 
python -m venv .venv
source .venv/bin/activate


# Install requirements
pip install -r requirements.txt
```

## Proof of Concept
You can run the proof of concept in two ways:
1) Run TGI and RabbitMQ services with Docker
2) Run all components in Docker

### Option 1: Run TGI and RabbitMQ services with Docker
Execute the following command to start the TGI and RabbitMQ services:
```bash
docker compose up tgi rabbitmq
```

In two separate terminal windows, run the following commands:
- In the first terminal:
```bash
faststream run consumer:app --workers <NUM_WORKERS>
```
- In the second terminal:
```bash
python producer.py -m 1000
```

### Option 2: Run all components in Docker
To run the consumer and producer along with TGI and RabbitMQ services, use:
```bash
docker compose up
```
