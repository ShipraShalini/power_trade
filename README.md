#### Overview
A modular trading data management system designed to store, process, and visualize trade activity. This project includes:

- A RESTful API for storing and querying trade data with authentication.
- A CSV batch importer to automate trade data ingestion from daily exchange reports.
- A PnL computation workflow that generates trade performance reports in the terminal.
- A web dashboard for traders to visualize their daily trading reports interactively.
- GitHub Actions for automating the trade import workflow by calling the API to input trade data.


#### System Requirements
`Python >= 3.11`

#### Steps before running the script.
1. Install poetry 
```shell
pip install poetry
```
2. Initialise project
```shell
poetry install
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

#### Running with docker-compose
1. Set up environment variables
2. Run `docker-compose up -d`
3. Access API Docs at `http://localhost:8000/docs`
4. Access PnL Dashboard at `http://localhost:3000`
5. Run scripts in shell by running `docker exec -it power_trade_backend bash`



#### Run Tests
1. Install poetry
```shell
pip install poetry
```
2. Initialise project
```shell
poetry install --with dev
```
3. Run tests
```shell
pytest -s
```
