import logging
import azure.functions as func
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential
import os
import json
import requests
from datetime import datetime, timedelta
# Use DefaultAzureCredential to get token (it picks up az login credentials)
credential = DefaultAzureCredential()

# Create LogsQueryClient
client = LogsQueryClient(credential)

# Set Application Insights Workspace ID
APP_INSIGHTS_APP_ID = "4584e6a8-ed2e-4227-812c-a3d59fc66d4a"
APP_INSIGHTS_RESOURCE_ID = "/subscriptions/c0346e61-0f1f-411a-8c22-32620deb01cf/resourceGroups/rg_aihub/providers/microsoft.insights/components/sk_demo_insight"

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_get_apim_model_insight")
def http_get_apim_model_insight(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    try:
          # Get token using DefaultAzureCredential (works if you've logged in via az login)
        credential = DefaultAzureCredential()
        token = credential.get_token("https://api.applicationinsights.io/.default").token
        # print("Token acquired: ", token)
        # Define query
        # query = "dependencies | where target contains 'Get4o Processing' or target contains 'chat' | where timestamp >= ago(10d) | project id, operation_ParentId, target, name,customDimensions['gen_ai.usage.input_tokens'],customDimensions['gen_ai.usage.output_tokens'], customDimensions['User Name']"
        
        query = """requests
                    | where isnotnull(customDimensions["Response-Body"])
                    | extend response_body = tostring(parse_json(customDimensions)["Response-Body"])
                    | extend parsed_body = parse_json(response_body)
                    | extend usage = parsed_body.usage
                    | project usage["prompt_tokens"], usage["completion_tokens"], usage["total_tokens"], 
                                tostring(parse_json(tostring(parse_json(tostring(parse_json(customDimensions)["Request-Body"]))["messages"]))[0]), 
                                parsed_body.model,url;"""
                    
       
        # Call Application Insights REST API
        url = f"https://api.applicationinsights.io/v1/apps/{APP_INSIGHTS_APP_ID}/query"
        headers = {
            "Authorization": f"Bearer {token}",
            'Content-Type': 'application/json'
            }
        params = {"query": query}
        print("****Call Start*")        
        response = requests.get(url, headers=headers, params=params)
        print("****Call complete*")
        
        if response.status_code == 200:
            print("****200*")
            # Parse the JSON response
            api_data = response.json()            
            transfrom_api_data = transform_data(api_data)
           
            print(f"****Data received*{transfrom_api_data}")
            # Return the data as an HTTP response
            return func.HttpResponse(
                body=json.dumps(transfrom_api_data),
                status_code=200,
                mimetype="application/json"
        )
        else:
            print("****ERROR*")
            # If the API call fails, return an error response
            return func.HttpResponse(
                f"API call failed with status code: {response.status_code} and message: {response.text}",
                status_code=response.status_code
            )
        

    except Exception as e:
        logging.error(f"Error querying Application Insights: {str(e)}")
        print("Error querying Application Insights: ", str(e))
        return func.HttpResponse(f"Error querying Application Insights: {str(e)}", status_code=500)

def transform_data(input_data):
        # Transform data
    output_data = {"data": []}

    for table in input_data.get("tables", []):
        columns = [col["name"] for col in table.get("columns", [])]  # Extract column names
        for row in table.get("rows", []):
            row_dict = {columns[i]: row[i] for i in range(len(columns)) if row[i] is not None}  # Exclude None values
            output_data["data"].append([row_dict])
   
    # Convert to JSON string and print
    print(output_data)
    return output_data