# Back end / service layer / FastAPI

## How to run the project: 

``` 
pip install -r requirements.txt 
uvicorn scoretracker:app
```

## Configuration variables

Environment variables are used for configuration (which can also be set in `.env`)

Supported variables:

- `DATABASE_URL`: The url of the SQL Database to connect to (example: `sqlite:///example.db`)
