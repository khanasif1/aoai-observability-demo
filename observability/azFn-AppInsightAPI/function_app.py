import logging
import azure.functions as func
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.identity import DefaultAzureCredential
import os
import json
import requests
from datetime import datetime, timedelta
# Use DefaultAzureCredential to get token (it picks up az login credentials)
# credential = DefaultAzureCredential()

# Create LogsQueryClient
# client = LogsQueryClient(credential)

# Set Application Insights Workspace ID
APP_INSIGHTS_APP_ID = ""
APP_INSIGHTS_APP_ID_OpenTel = "4584e6a8-ed2e-4227-812c-a3d59fc66d4a" # Resource :Subscription: Microsoft Non-Production  RG: rg_aihub | AppInsight: sk_demo_insight
APP_INSIGHTS_APP_ID_APIM = "18d3088c-24b1-4e88-9e06-8970db759e15" # Resource :Subscription: Microsoft Non-Production  RG: rg_aoai_pricing | AppInsight: appinsight-aoaiPricingApim

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="aoai_pricing_appinsight_api")
def http_get_insight(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Azure Function HTTP trigger received a request.")

    queryType = req.params.get('qType')
    if not queryType:
        return func.HttpResponse(
            "Please pass a query type (qType = opentel | apim) on the query string",
            status_code=400
        )
    try:
          # Get token using DefaultAzureCredential (works if you've logged in via az login)
        credential = DefaultAzureCredential()
        token = credential.get_token("https://api.applicationinsights.io/.default").token
        # print("Token acquired: ", token)
        # Define query
        # query = "dependencies | where target contains 'Get4o Processing' or target contains 'chat' | where timestamp >= ago(10d) | project id, operation_ParentId, target, name,customDimensions['gen_ai.usage.input_tokens'],customDimensions['gen_ai.usage.output_tokens'], customDimensions['User Name']"
        print("Query Type: ", queryType)
        query = ""
        if queryType == "opentel":
            APP_INSIGHTS_APP_ID = APP_INSIGHTS_APP_ID_OpenTel
            query = """let usr = dependencies 
                    | where target contains 'Get4o Processing' 
                    | where timestamp >= ago(10d) 
                    | project timestamp,id, operation_ParentId, target_usr=target, name, user=customDimensions['User Name'], performanceBucket;

            let token = dependencies 
                    | where target contains 'chat' 
                    | where timestamp >= ago(10d) 
                    | project id, operation_ParentId, target_token=target, name, ot=customDimensions['gen_ai.usage.output_tokens'],it=customDimensions['gen_ai.usage.input_tokens'], performanceBucket,model=customDimensions['gen_ai.response.model'];

            usr 
                    | join kind=inner (token) on $left.id == $right.operation_ParentId
                    | where isnotempty(user) and isnotnull(it)
                    | project timestamp, ApiCall=model, User=user, InputToken=it, OutputToken=ot,Perforamnce=performanceBucket;"""
        elif queryType == "apim":
            APP_INSIGHTS_APP_ID = APP_INSIGHTS_APP_ID_APIM
            query = """requests
                    | where isnotnull(customDimensions["Response-Body"]) and resultCode == 200
                    | where timestamp >= ago(10d)                    
                    | extend response_body = tostring(parse_json(customDimensions)["Response-Body"])
                    | extend user = tostring(parse_json(tostring(parse_json(tostring(parse_json(customDimensions)["Request-Body"]))["metadata"]))["user-name"])
                    | extend parsed_body = parse_json(response_body)
                    | extend usage = parsed_body.usage
                    | where isnotempty(user)
                    | project timestamp, ApiCall=parsed_body.model, User=user, InputToken=usage["prompt_tokens"], OutputToken=usage["completion_tokens"],Perforamnce=performanceBucket;"""
       
       
       
       
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
    print("****Transform data*")
    output_data = {"data": []}

    for table in input_data.get("tables", []):
        columns = [col["name"] for col in table.get("columns", [])]  # Extract column names
        for row in table.get("rows", []):
            row_dict = {columns[i]: row[i] for i in range(len(columns)) if row[i] is not None}  # Exclude None values
            output_data["data"].append([row_dict])
   
    print(f"Transform   ****: {output_data}****")
    return output_data