import os
import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, CompletionsFinishReason
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def get_model_pricing(prompt):

    try:
        endpoint = os.getenv("endpoint") #os.environ["AZURE_OPENAI_CHAT_ENDPOINT"]
        print("Endpoint: ", endpoint)
    except KeyError:
        print("Missing environment variable 'AZURE_OPENAI_CHAT_ENDPOINT'")
        print("Set it before running this sample.")
        exit()

    key_auth = True  # Set to True for key authentication, or False for Entra ID authentication.

    if key_auth:
        from azure.core.credentials import AzureKeyCredential

        try:            
            key = os.getenv("key") #os.environ["AZURE_OPENAI_CHAT_KEY"]
            print("Key: ", key) 
        except KeyError:
            print("Missing environment variable 'AZURE_OPENAI_CHAT_KEY'")
            print("Set it before running this sample.")
            exit()

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key),
            # api_version="2024-06-01",  # Azure OpenAI api-version. See https://aka.ms/azsdk/azure-ai-inference/azure-openai-api-versions
            api_version="2024-12-01-preview", # for o1
        )

    else:  # Entra ID authentication
        from azure.identity import DefaultAzureCredential

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

    return response.choices[0].message.content
    

@app.route(route="http_get_price")
def http_get_price(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    print(name)
    if name:
        URL = 'https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/'
        print ("calling url")
        response = requests.get(URL)               
        soup = BeautifulSoup(response.text, 'html.parser')
        data =  soup.find('section', id='pricing')
        # print(data)  # Print the entire HTML content for debugging
        print("data: received")
        prompt = "Read the html data and extract the prices for all the Azure OpenAI Model gpt-4o Model version 2024-11-20 deployment global get AU currency , list the result in json format. Json should have name, input price, output price and Cached Input price"
        prompt = prompt + str(data)
        # print(prompt)
        modelprice = get_model_pricing(prompt)
        return func.HttpResponse(
                body= modelprice,
                status_code=200,
                mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )