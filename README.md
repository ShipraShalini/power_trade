#### System Requirements
`Python >= 3.11`

#### Steps before running the script.
1. Install poetry 
```shell
pip install poetry
```
2. Initialise project
```shell
poetry init
```
3. Start APIs
```shell
uvicorn main:app --reload
```

#### Using the App
1. Access the API Docs:
   Go to `http://localhost:8000/docs`
2. Generate Report
   Run `python generate_report_script.py -t <trader_id> -d <date in ISO format>`