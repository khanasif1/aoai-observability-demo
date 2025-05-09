import os
import json
import requests
from bs4 import BeautifulSoup
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, CompletionsFinishReason
from azure.core.credentials import AzureKeyCredential

from azure.ai.inference.models import SystemMessage, UserMessage
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

from io import StringIO
from azure.storage.blob import BlobServiceClient

# 🔧 Replace with your actual Azure Storage values
STORAGE_ACCOUNT_NAME = "aoaipricingstorage"
CONTAINER_NAME = "modelprices"
BLOB_NAME = "model_price.json"
URL = 'https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/'
#updates
load_dotenv()

def get_model_pricing(prompt):

    try:
        endpoint = os.getenv("endpoint") #os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        print("Endpoint: ", endpoint)

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
            credential_scopes=["https://cognitiveservices.azure.com/.default"],
            # api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
            api_version="2024-12-01-preview", # for o1
        )
        
  
        print("Calling chat completions...")
        response = client.complete(
            messages=[
                SystemMessage("You are assistant, which reads html data and extracts information from html and produces result in json,cvs,text."),
                UserMessage(prompt),
            ]
        )

        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT'")
        print("Set it before running this sample.")
        exit()

def upload_to_blob(data):
    print("Uploading JSON to Azure Blob Storage...")
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
        credential=credential
    )

    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    try:
        container_client.create_container()
        print(f"ℹ️ Created container '{CONTAINER_NAME}'")
    except Exception:
        print(f"ℹ️ Container '{CONTAINER_NAME}' already exists")


    json_str = StringIO()
    json.dump(data, json_str, indent=2)
    json_bytes = json_str.getvalue().encode('utf-8')

    blob_client = container_client.get_blob_client(BLOB_NAME)
    blob_client.upload_blob(json_bytes, overwrite=True)
    # blob_client.upload_blob(json.dumps(data, indent=2), overwrite=True)

    print(f"✅ Uploaded JSON to blob as '{BLOB_NAME}' in container '{CONTAINER_NAME}'")





response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
data = pricing_section = soup.find('section', id='pricing')
print("Length of data:", len(str(data)))  # Print the string length of the HTML content
print("Number of child elements:", len(data.contents) if data else 0)  # Print number of child elements
# prompt = "Read the html data and extract the prices for all the Azure OpenAI Model gpt-4o Model version 2024-11-20 deployment global get AU currency , list the result in json format. Json should have name, input price, output price and Cached Input price"
prompt = "Read the html data and extract the prices for all the Azure OpenAI Models " \
        "Model Name : o1 Model version : 2024-12-17 \n" \
        "Model Name : o3 mini Model version : 2025-01-31 \n" \
        "Model Name : GPT-4.1 Model version :2025-04-14 \n" \
        "Model Name : GPT-4o Model version :2024-1120 \n" \
        "Model Name : GPT-4o mini Model version :0718 \n" \
        " use deployment global get AU currency , list the result in json format. Json should have name, input price, output price and Cached Input price " \
        "\n" 
# "look for models identify the prices Input,Cached Input, Output " \
prompt = prompt + str(data)
print(prompt)
json_model_price = get_model_pricing(prompt)
print("json_model_price: ", json_model_price)
print("Start uploading to blob")
upload_to_blob(json_model_price)


