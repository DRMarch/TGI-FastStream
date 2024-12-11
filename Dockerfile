FROM python:3.12-slim

# Copy required dependency file
COPY requirements.txt /tmp/requirements.txt

# Install required dependencies
RUN pip install -r /tmp/requirements.txt
