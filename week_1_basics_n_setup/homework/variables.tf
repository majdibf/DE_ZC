variable "credentials" {
  description = "My Credentials"
  default     = "../1_terraform/terrademo/keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "terraform-demo-438421"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "homework_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-438421-homework-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}