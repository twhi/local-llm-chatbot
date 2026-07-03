# Local LLM Chat Interface

A fast, Streamlit-based UI for interacting with local LLMs via `llama.cpp`. This interface is specifically optimised for reasoning models (e.g., DeepSeek-R1, Qwen reasoning variants). It parses the `reasoning_content` stream, rendering the model's internal thought process into a collapsible UI element to keep the chat clean. 

It also optimises your context window by stripping previous reasoning blocks from the chat history before sending subsequent prompts back to the server.

## Features

* **Real-Time Streaming:** Zero-latency Time To First Token (TTFT) directly from the local inference engine.
* **Reasoning Model Support:** Separates and streams reasoning/thinking tokens into an expandable `💭 Thinking Process` block.
* **Context Optimisation:** Prevents context window exhaustion by excluding past reasoning chains from the active API payload.
* **OpenAI API Compatible:** Connects via the standard OpenAI Python client to any OpenAI-compatible local endpoint (defaulting to `http://127.0.0.1:8080/v1`).

## Prerequisites

* Python 3.8+
* `llama.cpp` compiled with server support (`llama-server`)
* A reasoning GGUF model (e.g., `qwen.gguf`)