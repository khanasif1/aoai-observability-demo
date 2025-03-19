import os
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
import azure.functions as func
import json
import logging
from datetime import datetime, timedelta
import requests

# Replace with your Application Insights workspace ID
APP_INSIGHTS_WORKSPACE_ID = "307cf6d9-1b66-4fe4-bb75-370488b21827"

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="aoai_pricing_appinsight_api")
def aoai_pricing_appinsight_api(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        # results = query_app_insights()
         
        # Authenticate using Managed Identity (inside Azure) or environment credentials
        credential = DefaultAzureCredential()
        client = LogsQueryClient(credential)
        print("Credential created"+str(credential.__dict__.keys()))
        # Define the Kusto Query
        query = "AppTraces | take 10"
        
        start_time = datetime.utcnow() - timedelta(days=10)
        end_time = datetime.utcnow()
        print("Start time: ", start_time)
        print("End time: ", end_time)
        print(f'Query: {query}')
        print(f'APP_INSIGHTS_WORKSPACE_ID:{APP_INSIGHTS_WORKSPACE_ID}')
        # Execute the query
        response = client.query_workspace(
            APP_INSIGHTS_WORKSPACE_ID,            
            query,
            # timespan="P1D"  # Query logs from the past 1 day
            timespan=(start_time, end_time)
        )
        if not response.tables:
            print("No data returned.")
                     
        print("Response received"+response.tables)
        # Process response
        results = []
        print(f"Response body: {response.tables}")
       
        if response.tables:
            print("In response......")
            for table in response.tables:
                columns = [col.name for col in table.columns]
                for row in table.rows:                    
                    results.append(dict(zip(columns, row)))
                    
        print("read response......")            
        if response.tables:
            for table in response.tables:
                columns = [col.name for col in table.columns]  # Get column names
                for row in table.rows:
                    row_data = dict(zip(columns, row))  # Convert row to dict
                    print(row_data)
                        
        print("Results main fn: ", results[0].name)
        return func.HttpResponse(
            json.dumps(results, indent=2),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )


# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# @app.route(route="aoai_pricing_appinsight_api")
# def aoai_pricing_appinsight_api(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )