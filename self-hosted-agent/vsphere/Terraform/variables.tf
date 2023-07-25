#===========================#
# VMware vCenter connection #
#===========================#

variable "vsphere_user" {
  type        = string
  description = "VMware vSphere user name"
  sensitive = true
}

variable "vsphere_password" {
  type        = string
  description = "VMware vSphere password"
  sensitive = true
}

variable "vsphere_vcenter" {
  type        = string
  description = "VMWare vCenter server FQDN / IP"
  sensitive = true
}

variable "vsphere-unverified-ssl" {
  type        = string
  description = "Is the VMware vCenter using a self signed certificate (true/false)"
}

variable "vsphere-datacenter" {
  type        = string
  description = "VMWare vSphere datacenter"
}

variable "vsphere-cluster" {
  type        = string
  description = "VMWare vSphere cluster"
  default     = ""
}

variable "vsphere-template-folder" {
  type        = string
  description = "Template folder"
  default = "Templates"
}

#================================#
# VMware vSphere virtual machine #
#================================#

variable "name" {
  type        = string
  description = "The name of the vSphere virtual machines and the hostname of the machine"
}

variable "vm-name-prefix" {
  type        = string
  description = "Name of VM prefix"
  default     =  "k3sup"
}

variable "vm-datastore" {
  type        = string
  description = "Datastore used for the vSphere virtual machines"
}

variable "vm-network" {
  type        = string
  description = "Network used for the vSphere virtual machines"
}

variable "vm-linked-clone" {
  type        = string
  description = "Use linked clone to create the vSphere virtual machine from the template (true/false). If you would like to use the linked clone feature, your template need to have one and only one snapshot"
  default     = "false"
}

variable "cpu" {
  description = "Number of vCPU for the vSphere virtual machines"
  default     = 2
}

variable "cores-per-socket" {
  description = "Number of cores per cpu for workers"
  default     = 1
}

variable "ram" {
  description = "Amount of RAM for the vSphere virtual machines (example: 2048)"
}

variable "disksize" {
  description = "Disk size, example 100 for 100 GB"
  default = ""
}

variable "vm-guest-id" {
  type        = string
  description = "The ID of virtual machines operating system"
}

variable "vm-template-name" {
  type        = string
  description = "The template to clone to create the VM"
}

variable "vm-domain" {
  type        = string
  description = "Linux virtual machine domain name for the machine. This, along with host_name, make up the FQDN of the virtual machine"
  default     = ""
}

variable "dns_server_list" {
  type = list(string)
  description = "List of DNS servers"
  default = ["8.8.8.8", "8.8.4.4"]
}

variable "ipv4_address" {
  type = string
  description = "ipv4 addresses for a vm"
}

variable "ipv4_gateway" {
  type = string
}

variable "ipv4_netmask" {
  type = string
}

variable "ssh_username" {
  type      = string
  sensitive = true
  default   = "sam"
}

variable "public_key" {
  type        = string
  description = "Public key to be used to ssh into a machine"
  default     = "AAAAB3NzaC1yc2EAAAADAQABAAABAQCb7fcDZfIG+SxuP5UsZaoHPdh9MNxtEL5xRI71hzMS5h4SsZiPGEP4shLcF9YxSncdOJpyOJ6OgumNSFWj2pCd/kqg9wQzk/E1o+FRMbWX5gX8xMzPig8mmKkW5szhnP+yYYYuGUqvTAKX4ua1mQwL6PipWKYJ1huJhgpGHrvSQ6kuywJ23hw4klcaiZKXVYtvTi8pqZHhE5Kx1237a/6GRwnbGLEp0UR2Q/KPf6yRgZIrCdD+AtOznSBsBhf5vqcfnnwEIC/DOnqcOTahBVtFhOKuPSv3bUikAD4Vw7SIRteMltUVkd/O341fx+diKOBY7a8M6pn81HEZEmGsr7rT sam@SamMac.local"
}