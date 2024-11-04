#WEEK 1

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


docker-compose create a default network named according to the following format :
<folder_name>_default
2_docker_sql_default

docker run  -it --network=2_docker_sql_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}


taxi zones url:
https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv


Terraform installation:
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

export GOOGLE_CREDENTIALS='/home/mbenfredj/data-engineering-zc/week_1_basics_n_setup/1_terraform/terrademo/keys/my-creds.json'

terraform fmt
terraform init
terraform plan
terraform apply
terraform destroy

Unset linux variable:
unset GOOGLE_CREDENTIALS

install terraform:
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

Set environment variable to point the GCP keys: 
export GOOGLE_APPLICATION_CREDENTIALS="/home/mbenfredj/terrademo/keys/my-creds.json"


#WEEK 2

cd ~ && mkdir -p ~/.google/credentials/
mv ~/Bureau/terraform-demo-438421-383ae38d40e7.json ~/.google/credentials/google_credentials.json

mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

#Build the image when there's any change in the Dockerfile
docker-compose build

#Initialize the Airflow scheduler, DB, and other config
docker-compose up airflow-init

#Kick up the all the services from the container
docker-compose up

#see which containers are up & running (there should be 7, matching with the services in your docker-compose file)
docker-compose ps


#Login to Airflow web UI with default creds: airflow/airflow
localhost:8080

#shut down the container/s:
docker-compose down
