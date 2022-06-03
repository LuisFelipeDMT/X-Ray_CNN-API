FROM python:3.8-buster

COPY scripts/simple.py simple.py
COPY scripts/imageprocess.py imageprocess.py
COPY model/model_resnet152_05.h5 model_weights.h5
COPY model/model_resnet152_05.json model.json
COPY requirements.txt requirements.txt

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "simple:app", "--host", "0.0.0.0",  "--port",  "8080"]
