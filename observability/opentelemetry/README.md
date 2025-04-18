
https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-inference/samples
---
page_type: sample
languages:
  - python
products:
  - azure
  - azure-ai
urlFragment: model-inference-samples
---

# Samples for Azure AI Inference client library for Python

These are runnable console Python scripts that show how to do chat completion and text embeddings against Serverless API endpoints and Managed Compute endpoints.

Samples with `azure_openai` in their name show how to do chat completions and text embeddings against Azure OpenAI endpoints.

Samples in this folder use the a synchronous clients. Samples in the subfolder `async_samples` use the asynchronous clients. The concepts are similar, you can easily modify any of the synchronous samples to asynchronous.

## Prerequisites

See [Prerequisites](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-inference/README.md#prerequisites) here.

## Setup

* Clone or download this sample repository
* Open a command prompt / terminal window in this samples folder
* Install the client library for Python with pip:
  ```bash
  pip install azure-ai-inference
  ```
  or update an existing installation:
  ```bash
  pip install --upgrade azure-ai-inference
  ```
* If you plan to run the asynchronous client samples, insall the additional package [aiohttp](https://pypi.org/project/aiohttp/):

  ```bash
 & {.\.venv\Scripts\python.exe -m pip install -r requirements.txt}

  pip install aiohttp

  pip install --upgrade pip
  pip install opentelemetry-api

  pip install opentelemetry-exporter-otlp 

  pip install azure-monitor-opentelemetry
  ```


## Run Sample : sample_chat_completions_azure_openai.py

- Login with az login
- python sample_chat_completions_azure_openai.py
- Provide user : {enter any name}
- Enter prompt :{ask what you like}