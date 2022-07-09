resource "azurerm_kubernetes_cluster" "default" {
  name                = "${var.aks_name}-aks"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  dns_prefix          = "${var.aks_name}-k8s"

  default_node_pool {
    name            = "default"
    node_count      = 2
    vm_size         = "Standard_D2_v2"
    os_disk_size_gb = 30
  }

  service_principal {
    client_id     = var.client_id
    client_secret = var.client_secret
  }

  role_based_access_control_enabled = true
}
