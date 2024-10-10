Data Engineering is the design and development of systems for collecting, storing and analyzing data at scale.

A data pipeline is a service that receives data as input and outputs more data. For example, reading a CSV file, transforming the data somehow and storing it as a table in a PostgreSQL database.

Docker is a containerization software that allows us to isolate software in a similar way to virtual machines but in a much leaner way.
A Docker image is a snapshot of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

Docker containers are stateless: any changes done inside a container will NOT be saved when the container is killed and started again.

build the image:
docker build -t test:pandas

run docker container from image:
docker run -it test:pandas some_number

Running Postgres in a container:

mkdir week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data
sudo chmod 755 week_1_basics_n_setup/2_docker_sql/ny_taxi_postgres_data

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

If you see that ny_taxi_postgres_data is empty after running the container, try these:
    Deleting the folder and running Docker again (Docker will re-create the folder)
    Adjust the permissions of the folder by running sudo chmod a+rwx ny_taxi_postgres_data

Once the container is running, we can log into our database with pgcli with the following command:
pip install pgcli 
pip install "psycopg2[binary]"
sudo apt-get install libpq5

pgcli -h localhost -p 5432 -u root -d ny_taxi

pgcli --help

pip install jupyter
jupyter notebook

NY Trips Dataset:
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
gzip -d yellow_tripdata_2021-01.csv.gz  :The command will restore the compressed file to its original state and remove the .gz file.
gzip -dk yellow_tripdata_2021-01.csv.gz  : to keep the compressed file

head -n 100 yellow_tripdata_2021-01.csv
head -n 100 yellow_tripdata_2021-01.csv > yellow_head.csv

wc -l yellow_head.csv

pip install sqlalchemy
pip install psycopg2-binary

Running pgAdmin & postgres in the same network:
docker network create pg-network

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name=pgadmin \
  dpage/pgadmin4

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name=pg-database \
  postgres:13

Convert a jupyter notebook to python script:
jupyter nbconvert --to python upload-data.ipynb

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}

build taxi_ingest from dockerfile:
docker build -t taxi_ingest:v001 .

run taxi_ingest container:

docker run  -it --network=pg-network \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}


strat services with:
docker-compose up
docker-compose -d up

docker compose up
docker compose -d up

Stop services with:
docker-compose down
docker compose down