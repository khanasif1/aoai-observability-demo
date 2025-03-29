# azFn-AppInsightAPI Deployment 

## Run function locally

- Create virtual env
 python -m venv .venv

- enable virtual environment 

`
.\.venv\Scripts\Activate.ps1

`

- Pip install packages

`
pip install -r requirements.txt

`
- Install function Core for windows
https://github.com/Azure/azure-functions-core-tools/blob/v4.x/README.md#windows

- Run function

`
func start --python

`
## Deploy Function

- Create a Azure function using portal or CLI

- If you are direcly deploying function enale virtual environment
`
.\.venv\Scripts\Activate.ps1

`
- Deploy

`
func azure functionapp publish  fn-get-insight --python

`


- 



az functionapp config appsettings set --name fn-get-insight --resource-group rg_aoai_pricing --settings WEBSITE_RUN_FROM_PACKAGE=0
func azure functionapp publish fn-get-insight


Compress-Archive -Path * -DestinationPath functionapp.zip -Force
az functionapp deployment source config-zip --resource-group rg_aoai_pricing --name fn-get-insight --src functionapp.zip
