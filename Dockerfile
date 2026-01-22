FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Prevent compiling
ENV PIP_ONLY_BINARY=:all:

RUN pip install --no-cache-dir \
    llama-cpp-python==0.2.48 \
    --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

RUN pip install --no-cache-dir "huggingface_hub<0.25.0" gradio

WORKDIR /app
COPY . .
CMD ["python", "app.py"]