#!/bin/bash

URL_DATA="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
URL_ZONE="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

python hw_ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url_data="${URL_DATA}" \
  --url_zone="${URL_ZONE}"
