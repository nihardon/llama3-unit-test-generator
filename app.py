import gradio as gr
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import threading
import time

# --- Global State ---
llm_model = None
load_status = "Starting..."
is_loaded = False

# --- Background Loader ---
def load_model_in_background():
    global llm_model, load_status, is_loaded
    
    try:
        print("⏳ Background thread started...")
        load_status = "⬇️ Downloading model (approx 1-2 mins)..."
        
        # Download the model
        model_path = hf_hub_download(
            repo_id="nihardon/fine-tuned-unit-test-generator",
            filename="llama-3-8b.Q4_K_M.gguf",
        )
        
        load_status = "🧠 Loading into RAM (approx 60s)..."
        print("Loading weights...")
        
        # Load the model (verbose=False speeds it up slightly)
        llm_model = Llama(
            model_path=model_path,
            n_ctx=1024,
            n_threads=2,
            verbose=False 
        )
        
        load_status = "✅ Model Ready!"
        is_loaded = True
        print("🚀 Model successfully loaded!")
        
    except Exception as e:
        load_status = f"❌ Error: {str(e)}"
        print(load_status)

# Start the loader immediately in the background
threading.Thread(target=load_model_in_background, daemon=True).start()

# --- The Generator Function ---
def generate_test(user_code):
    global llm_model, is_loaded, load_status
    
    # 1. Check if model is ready
    if not is_loaded or llm_model is None:
        return f"⚠️ SYSTEM INITIALIZING...\n\nCurrent Status: {load_status}\n\nPlease wait 60 seconds and click Generate again."
    
    # 2. Run Generation
    prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You are an expert Python QA engineer. Write a pytest unit test for the following function.
Rules:
1. Use the 'pytest' framework.
2. Do NOT use 'unittest.TestCase' classes.
3. Use simple functions starting with 'test_'.
4. Include assert statements.

### Input:
{user_code}

### Response:
"""
    try:
        output = llm_model(
            prompt,
            max_tokens=512,
            stop=["### Instruction:", "### Input:"],
            echo=False
        )
        return output["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error during generation: {str(e)}"

# --- The UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧪 AI Unit Test Generator")
    gr.Markdown("**Status:** System starts automatically. If the model isn't ready, it will tell you.")
    
    with gr.Row():
        with gr.Column():
            input_box = gr.Code(
                language="python",
                value="def add(a, b):\n    return a + b",
                label="Function"
            )
            btn = gr.Button("Generate Pytest", variant="primary")
        with gr.Column():
            output_box = gr.Code(language="python", label="Generated Test Case")
            
    btn.click(generate_test, inputs=input_box, outputs=output_box)

demo.launch(server_name="0.0.0.0", server_port=7860)