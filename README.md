# AI Agents Practice Code 

This project is specifically for practice purpose, breakdown, debugging and learning of how AI Workflows and AI Agents can be build on open source tools. (Please ignore code quality)

## Ollama Setup and Llama 3.2 Model

This document provides instructions for setting up and running Ollama with the Llama 3.2 model.

## Steps

1. **Install Ollama**: If Ollama is not already installed, follow the instructions at [Ollama Download](https://ollama.com/download).
2. **Pull the Llama 3.2 Model**: Use the command `ollama pull llama3:2` to pull the model from the Ollama repository.
3. **Run the Model**: Execute `ollama run llama3:2` to start the Ollama server and load the Llama 3.2 model for inference.

## Prerequisites

- Ensure Docker is installed (if using the Docker version of Ollama).
- Sufficient system resources to run Llama 3.2.

## Usage

1. **Install Ollama**: Follow instructions at [Ollama Download](https://ollama.com/download).
2. **Pull the Llama 3.2 Model**: `ollama pull llama3:2`
3. **Run the Model**: `ollama run llama3:2`

## Package Management and Running Python Files with `uv`

1. **Install `uv`**: Ensure `uv` is installed in your environment. You can install it using pip:
   ```bash
   pip install uv
   ```
2. Add a pacakge.For example: `uv add requests`
3. Execute a python file. For example: `uv run tool_calling.py`

For more information, refer to the official [Ollama documentation](https://ollama.com/docs).