FROM python:3.10.1

WORKDIR /scoretrackerApp

COPY ./requirements.txt  /scoretrackerApp/requirements.txt
COPY .env  /scoretrackerApp/.env

RUN pip install --no-cache-dir --upgrade -r /scoretrackerApp/requirements.txt

COPY ./scoretracker /scoretrackerApp/scoretracker

CMD ["uvicorn", "scoretracker:app", "--host", "0.0.0.0", "--port", "8080"]
