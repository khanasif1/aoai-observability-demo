# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""
DESCRIPTION:
    This sample demonstrates how to get a chat completions response from
    the service using a synchronous client, with an Azure OpenAI (AOAI) endpoint.
    Two types of authentications are shown: key authentication and Entra ID
    authentication.

USAGE:
    1. Update `key_auth` below to `True` for key authentication, or `False` for
       Entra ID authentication.
    2. Update `api_version` (the AOAI REST API version) as needed.
       See the "Data plane - inference" row in the table here for latest AOAI api-version:
       https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
    3. Set one or two environment variables, depending on your authentication method:
        * AZURE_OPENAI_CHAT_ENDPOINT - Your AOAI endpoint URL, with partial path, in the form
            https://<your-unique-resouce-name>.openai.azure.com/openai/deployments/<your-deployment-name>
            where `your-unique-resource-name` is your globally unique AOAI resource name,
            and `your-deployment-name` is your AI Model deployment name.
            For example: https://your-unique-host.openai.azure.com/openai/deployments/gpt-4o
        * AZURE_OPENAI_CHAT_KEY - Your model key. Keep it secret. This is only required for key authentication.
    4. Run the sample:
       python sample_chat_completions_azure_openai.py
"""

import os
from opentelemetry import trace
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, CompletionsFinishReason
from azure.core.credentials import AzureKeyCredential
from azure.monitor.opentelemetry import configure_azure_monitor

from azure.ai.inference.models import SystemMessage, UserMessage
from dotenv import load_dotenv


# [START trace_function]
from opentelemetry.trace import get_tracer

tracer = get_tracer(__name__)

load_dotenv()

@tracer.start_as_current_span("Get4o Processing")  # type: ignore
def sample_chat_completions_azure_openai(username, prompt):
    print("Sample Chat Completions Azure OpenAI")

    span = trace.get_current_span()
    span.set_attribute("User Name",username)
    span.set_attribute("User Prompt",prompt)
    try:
        endpoint = os.getenv("endpoint") #os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT'")
        print("Set it before running this sample.")
        exit()

    key_auth = True  # Set to True for key authentication, or False for Entra ID authentication.

    if key_auth:
        from azure.core.credentials import AzureKeyCredential

        try:
            key = os.getenv("key") #os.environ["AZURE_OPENAI_CHAT_KEY"]
        except KeyError:
            print("Missing environment variable 'AZURE_OPENAI_CHAT_KEY'")
            print("Set it before running this sample.")
            exit()

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
            api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
        )

    else:  # Entra ID authentication
        from azure.identity import DefaultAzureCredential
        
       
        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
            credential_scopes=["https://cognitiveservices.azure.com/.default"],
            api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
        )
        
  
    print("Calling chat completions...")
    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage(prompt),
        ]
    )  
    print("Response: ", response.choices[0].message.content)

if __name__ == "__main__":
    configure_azure_monitor()
    username = input("Enter user name: ")
    prompt = input("Enter your prompt: ")
    sample_chat_completions_azure_openai(username, prompt)
