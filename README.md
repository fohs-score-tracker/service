# Back end / service layer / FastAPI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


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
REDIS_URL="redis://user:password@server/db"
```
