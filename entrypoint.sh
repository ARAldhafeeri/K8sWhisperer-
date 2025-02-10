#!/bin/bash

# Start Ollama (make sure the model is available)
/usr/bin/ollama serve & 

pid=$!

sleep 5


echo "pulling tinyllama"

ollama pull tinyllama 

# Start your Python application
kopf run main.py --verbose

# Keep the container running
wait $pid 