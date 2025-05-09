# Use the Scraping solution to get Model price from Azure pricing

## Run function locally

- Create virtual env
 
 ```
 python -m venv .venv
```
- enable virtual environment 

```
.\.venv\Scripts\Activate.ps1

```

- Pip install packages

```
pip install -r requirements.txt

```
- Install function Core for windows
https://github.com/Azure/azure-functions-core-tools/blob/v4.x/README.md#windows

- Run function


```
func start --python
```

## Deploy Function

- az login

- python -m venv .venv

- func settings add API_KEY your-secret-api-key

- func azure functionapp publish  fn-get-model-price-app --python
