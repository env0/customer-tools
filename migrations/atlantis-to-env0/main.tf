terraform {
  # Use the backend gcs block below for Atlantis, then move to the remote backend block to migrate to env0, then you can remove the backend block altogether after the migration.
  backend "gcs" {
    bucket = "tekanaid-tf-state-prod"
    prefix = "terraform/state"
  }
  # backend "remote" {
  #   hostname = "backend.api.env0.com"
  #   organization = "1cec7bbf-68cc-43a9-9f82-95d654bb6489.46ee7664-9f3d-47f3-b82f-7b250bf86502"

  # workspaces {
  #   name = "dev-env0-atlantis-migration-test"
  # }
  # }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.40.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
}

resource "google_compute_instance" "default" {
  name         = var.instance_name
  machine_type = "e2-micro"
  
  zone         = var.zone
  tags = ["dev", "engineering"]

  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2204-jammy-v20221014"
      labels = {
        env = "dev"
      }
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }
}
