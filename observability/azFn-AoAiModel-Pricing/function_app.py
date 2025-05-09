# import os
# import azure.functions as func
# import logging
# import requests
# from bs4 import BeautifulSoup
# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage, UserMessage, CompletionsFinishReason
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.inference.models import SystemMessage, UserMessage
# import json

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
# model="gpt-4o"
# model_version="2024-11-20"

# def get_model_pricing(prompt):

#     try:
#         endpoint = os.getenv("endpoint") #os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
#         print("Endpoint: ", endpoint)
#     except KeyError:
#         print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT'")
#         print("Set it before running this sample.")
#         exit()

#     key_auth = True  # Set to True for key authentication, or False for Entra ID authentication.

#     if key_auth:
#         from azure.core.credentials import AzureKeyCredential

#         try:            
#             key = os.getenv("key") #os.environ["AZURE_OPENAI_CHAT_KEY"]
#             print("Key: ", key) 
#         except KeyError:
#             print("Missing environment variable 'AZURE_OPENAI_CHAT_KEY'")
#             print("Set it before running this sample.")
#             exit()

#         client = ChatCompletionsClient(
#             endpoint=endpoint,
#             credential=AzureKeyCredential(key),
#             # api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
#             api_version="2024-12-01-preview", # for o1
#         )

#     else:  # Entra ID authentication
#         from azure.identity import DefaultAzureCredential

#         client = ChatCompletionsClient(
#             endpoint=endpoint,
#             credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
#             credential_scopes=["https://cognitiveservices.azure.com/.default"],
#             # api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
#             api_version="2024-12-01-preview", # for o1
#         )       
  
#     print("Calling chat completions...")
#     response = client.complete(
#         messages=[
#             SystemMessage("You are assistant, which reads html data and extracts information from html and produces result in json,cvs,text."),
#             UserMessage(prompt),
#         ]
#     )

#     return response.choices[0].message.content
    

# @app.route(route="http_get_price")
# def http_get_price(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     model = req.params.get('model')
#     model_version = req.params.get('model_version')    
#     if model and model_version:
#         print(f"Details: {model} : {model_version}")
#         URL = 'https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/'
#         print ("calling url")
#         response = requests.get(URL)               
#         soup = BeautifulSoup(response.text, 'html.parser')
#         data =  soup.find('section', id='pricing')
#         # print(data)  # Print the entire HTML content for debugging
#         print("data: received")
#         prompt = f"Read the html data and extract the prices for all the Azure OpenAI Model : {model} Model version : {model_version} deployment global get AU currency , list the result in json format. Json should have name, input price, output price and Cached Input price"
#         prompt = prompt + str(data)
#         # print(prompt)
#         modelprice = get_model_pricing(prompt)
#         return func.HttpResponse(
#                 body= modelprice,
#                 status_code=200,
#                 mimetype="application/json"
#         )
#     else:
#         return func.HttpResponse(
#              "Error!! Please pass model and model_version in the query string",
#              status_code=400
#         )

import logging
import azure.functions as func
import json

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

STORAGE_ACCOUNT_URL = "https://aoaipricingstorage.blob.core.windows.net"
CONTAINER_NAME = "modelprices"
BLOB_NAME = "model_price.json"
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_get_price")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request for model price using Entra ID.')

    model_name = req.params.get('model_name')
    print(f"Model Name: {model_name}")
    if not model_name:
        return func.HttpResponse("Missing 'model_name' query parameter.", status_code=400)

    try:
        # Authenticate with Managed Identity (Entra ID)
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
        blob_client = blob_service_client.get_container_client(CONTAINER_NAME).get_blob_client(BLOB_NAME)
        print("Blob client created successfully.")
        
        # Read blob content
        blob_data = blob_client.download_blob().readall()
        raw_str = blob_data.decode("utf-8")
        parsed_data = json.loads(raw_str)
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)
        print(f"Json data loaded successfully {parsed_data}")
        
        # Search for model
        for item in parsed_data:
            if item["name"] == model_name:
                print(f"Model found: {item}")
                return func.HttpResponse(
                    json.dumps(item, indent=2),
                    mimetype="application/json"
                )

        return func.HttpResponse(f"Model '{model_name}' not found.", status_code=404)

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Internal server error", status_code=500)
