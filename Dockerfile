# --- Builder Stage ---
FROM python:3.11 AS builder
WORKDIR /usr/src/app
ENV PATH="/venv/bin:$PATH"
RUN apt-get update && apt-get install -y git
RUN python -m venv /venv
COPY . /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# --- Ollama Server Stage ---
FROM ollama/ollama:0.1.32 AS ollama


# --- Final Image Stage ---
FROM python:3.11
WORKDIR /usr/src/app

COPY --from=ollama /usr/bin/ollama /usr/bin/ollama
RUN chmod +x /usr/bin/ollama

ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=http://0.0.0.0:11434

# Copy the virtual environment and app code from the builder.
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app /usr/src/app


# Ensure our virtual environment's bin directory is in the PATH.
ENV PATH="/venv/bin:$PATH"

# Make the entrypoint script executable.
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the entrypoint script as the container's command.
CMD ["/usr/src/app/entrypoint.sh"]
