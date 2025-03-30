# Use the Scraping solution


- python -m venv .venv
- pip install -r requirements.txt


func settings add API_KEY your-secret-api-key

func azure functionapp publish  fn-get-modelcost-appserv --python
