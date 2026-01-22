FROM python:3.13.1-slim

RUN groupadd -r ferlab && useradd -r -g ferlab -s /bin/bash ferlab
RUN mkdir -p /home/ferlab/app && chown -R ferlab:ferlab /home/ferlab

RUN apt-get update && apt-get install -y --no-install-recommends build-essential      

USER ferlab

COPY polars-requirements.txt /home/ferlab/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r /home/ferlab/requirements.txt
RUN rm /home/ferlab/requirements.txt

COPY src/public_datalake /home/ferlab/app/public_datalake
COPY scripts/normalize.py /home/ferlab/app/normalize.py

ENV PYTHONPATH=/home/ferlab/app

WORKDIR /home/ferlab/app
