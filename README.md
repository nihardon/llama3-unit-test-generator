# 🧪 Llama-3 Unit Test Generator

A fine-tuned LLM inference engine that autonomously writes `pytest` unit tests for Python functions.

**[🔴 Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/nihardon/unit-test-generator)**

## 🚀 Key Features
* **Model:** Meta Llama-3-8B fine-tuned on 18k Python instruction sets (Alpaca-Python).
* **Quantization:** Implements 4-bit GGUF quantization to run on CPU-only environments (reduced VRAM from 16GB → 4.5GB).
* **Infrastructure:** Custom Docker container with manual `cmake` compilation for `llama-cpp-python` to resolve Linux kernel mismatches.
* **UX:** Asynchronous background loading to bypass server timeouts on cold starts.

## 🛠️ Tech Stack
* **Python 3.9**
* **Llama.cpp** (GGUF Inference)
* **Gradio** (Web UI)
* **Docker** (Containerization)
* **Hugging Face Hub** (Model Registry)

## 📦 Installation (Local)
1. Clone the repo:
   ```bash
   git clone [https://github.com/nihardon/llama3-unit-test-generator](https://github.com/nihardon/llama3-unit-test-generator)
   cd llama3-unit-test-generator
