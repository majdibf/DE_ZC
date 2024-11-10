import pandas as pd
from sqlalchemy import create_engine
from time import time
from pyarrow import parquet as pq
import datetime as datetime

def ingest_callable(user, password, host, port, db, table_name, parquet_file, execution_date):
    print(table_name, parquet_file, execution_date)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print('connection established successfully, inserting data...')

    t_start = time()

    chunk_size = 100000
    pf = pq.ParquetFile(parquet_file)
    i = 0
    for batch in pf.iter_batches(batch_size=chunk_size):
        df = batch.to_pandas()

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        if(i == 0):
            df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
        
        df = df.to_sql(name=table_name, con=engine, if_exists="append")
        t_end = time()
        print('inserted the first chunk, took %.3f second' % (t_end - t_start))
        i+=1


if __name__ == '__main__':
    ingest_callable('root', 'root', 'localhost', '5432', 'ny_taxi', 'yellow_taxi', '/home/mbenfredj/PycharmProjects/data-engineering-zc/week_2_data_ingestion/airflow/yellow_tripdata_2024-01.parquet','01/01/2024')
