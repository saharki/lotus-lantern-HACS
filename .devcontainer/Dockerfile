FROM python:3.11-slim

# Install bluetooth dependencies
RUN apt-get update && apt-get install -y \
    bluetooth bluez libbluetooth-dev libglib2.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /workspace

# Install python deps
COPY * .
RUN pip install -r requirements.txt