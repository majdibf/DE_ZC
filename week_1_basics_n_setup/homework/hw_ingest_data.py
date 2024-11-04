#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import gzip


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url_data = params.url_data
    url_zone = params.url_zone


    gz_name = "green_tripdata_2019-09.csv.gz"
    csv_name = "green_tripdata_2019-09.csv"

    os.system(f'wget {url_data} -O {gz_name}')

    with gzip.open(gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            f_out.write(f_in.read())

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    df = df.to_sql(name=table_name, con=engine, if_exists="append")

    try:

        while True:
            t_start = time()
            df = next(df_iter)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df = df.to_sql(name=table_name, con=engine, if_exists="append")
            t_end = time()
            print("inserted another chunk..., took %.3f second " % (t_end - t_start))
    except StopIteration:
        print("All data has been processed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
    taxi_zone_file_name = 'taxi_zone_lookup.csv'
    os.system(f'wget {url_zone} -O {taxi_zone_file_name}')
    df_zones = pd.read_csv(taxi_zone_file_name)
    df_zones.to_sql(name="zones", con=engine, if_exists="replace")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the result to')
    parser.add_argument('--url_data', help='url of data csv file')
    parser.add_argument('--url_zone', help='url of zone csv file')


    args = parser.parse_args()

    main(args)
