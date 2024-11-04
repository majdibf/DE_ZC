#Docker

Q1: Which docker run tag has the following text? - Automatically remove the container when it exits
A1: docker run --help | grep "Automatically remove the container"
      --rm                               Automatically remove the container and its associated anonymous volumes when it exits

docker run --rm

Q2: Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
    Check the python modules that are installed.
    What is version of the package wheel ?

A2: docker run -it --entrypoint=bash  python:3.9
    pip list
    wheel 0.44.0

#Postgres
Run Postgres and load data as shown in the videos We'll use the green taxi trips from September 2019:

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13


wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


Q3: How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that lpep_pickup_datetime and lpep_dropoff_datetime columns are in the format timestamp (date and hour+min+sec) and not in date.

A3: select count(1) from green_taxi_trips where date(lpep_pickup_datetime) in ('2019-09-18') and date(lpep_dropoff_datetime) in ('2019-09-18')

15612

Q4: Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance.

A4: 
SELECT date(lpep_pickup_datetime)
FROM green_taxi_trips
WHERE trip_distance = (
  SELECT MAX(trip_distance)
  FROM green_taxi_trips
)
LIMIT 1;

2019-09-26

Q5:Three biggest pick up Boroughs
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown
Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

A5:

SELECT
    Z."Borough",
    SUM(G."total_amount") AS "TOTAL"
FROM
    GREEN_TAXI_TRIPS G
    LEFT JOIN ZONES Z ON G."PULocationID" = Z."LocationID"
WHERE
    DATE(G."lpep_pickup_datetime") = '2019-09-18'
GROUP BY
    Z."Borough"
HAVING
    SUM(G."total_amount")>50000

order by "TOTAL" DESC

=>  "Brooklyn" "Manhattan" "Queens"

Q6: Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

A6:
SELECT ZDO."Zone", max(G.tip_amount) AS max_tip
FROM GREEN_TAXI_TRIPS G
LEFT JOIN ZONES ZPU ON G."PULocationID" = ZPU."LocationID"
LEFT JOIN ZONES ZDO ON G."DOLocationID" = ZDO."LocationID"
WHERE EXTRACT(YEAR FROM G.lpep_pickup_datetime) = 2019
  AND EXTRACT(MONTH FROM G.lpep_pickup_datetime) = 9
  AND ZPU."Zone" = 'Astoria'
GROUP BY ZDO."Zone"
ORDER BY max_tip DESC
LIMIT 1;

=> "JFK Airport"	62.31

Q7:create a GCP Bucket and Big Query Dataset.

A7:

$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.homework_dataset will be created
  + resource "google_bigquery_dataset" "homework_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "homework_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = {
          + "goog-terraform-provisioned" = "true"
        }
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "terraform-demo-438421"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = {
          + "goog-terraform-provisioned" = "true"
        }

      + access (known after apply)
    }

  # google_storage_bucket.homework-bucket will be created
  + resource "google_storage_bucket" "homework-bucket" {
      + effective_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-438421-homework-bucket"
      + project                     = (known after apply)
      + project_number              = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = {
          + "goog-terraform-provisioned" = "true"
        }
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type          = "AbortIncompleteMultipartUpload"
                # (1 unchanged attribute hidden)
            }
          + condition {
              + age                    = 1
              + matches_prefix         = []
              + matches_storage_class  = []
              + matches_suffix         = []
              + with_state             = (known after apply)
                # (3 unchanged attributes hidden)
            }
        }

      + soft_delete_policy (known after apply)

      + versioning (known after apply)

      + website (known after apply)
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.homework_dataset: Creating...
google_storage_bucket.homework-bucket: Creating...
google_bigquery_dataset.homework_dataset: Creation complete after 2s [id=projects/terraform-demo-438421/datasets/homework_dataset]
google_storage_bucket.homework-bucket: Creation complete after 2s [id=terraform-demo-438421-homework-bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.