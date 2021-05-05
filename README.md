# Back end / service layer / FastAPI

## How to run the project: 

```sh
git clone https://github.com/fohs-score-tracker/service
cd service
python -m venv venv  # optional
pip install -r requirements.txt 
uvicorn scoretracker:app
```

## Configuration variables

Environment variables are used for configuration (which can also be set in `.env`)

Example config file: 

```sh
## Default values
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0

## No values by default
#REDIS_PASSWORD="123456"
#REDIS_USERNAME="user"
```
