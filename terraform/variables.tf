variable "subscription_id" {
  description = "The azure subscription id"
  default     = "change_me"
}

variable "tenant_id" {
  description = "The azure tenant id"
  default     = "change_me"
}

variable "client_id" {
  description = "The azure client id"
  default     = "change_me"
}

variable "client_secret" {
  description = "The azure client secret"
  default     = "change_me"
}

variable "acr_name" {
  description = "The name for the Azure Container Registry"
  default     = "iotedgecluster"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  default     = "DefaultResourceGroup-CUS"
}

variable "resource_group_location" {
  description = "The location of the resource group"
  default     = "South Central US"
}
