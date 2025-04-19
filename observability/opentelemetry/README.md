# Console application with opentelemetry

These are runnable console Python scripts that show how to do chat completion against Serverless API endpoints and Managed Compute endpoints.

Samples with `azure_openai` in their name show how to do chat completions against Azure OpenAI endpoints.


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