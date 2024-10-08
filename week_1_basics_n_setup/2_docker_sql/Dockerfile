FROM python:3.9
LABEL authors="mbenfredj"

RUN pip install pandas
WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT ["python", "pipeline.py"]