# Ansible Playbook - SAP HANA scale-out

This Ansible Playbook can be executed with:
- Ansible to provision hosts
- Ansible + Terraform to provision hosts
- Existing hosts

This Ansible Playbook can be targeted at the following Infrastructure Platforms:
- Amazon Web Services (AWS)
- Google Cloud Platform (GCP)
- IBM Cloud
- IBM Cloud, IBM Power Virtual Servers
- Microsoft Azure (MS Azure)
- IBM PowerVM
- OVirt
- VMware

SAP HANA software versions (included, compatible with any):
SPS07, SPS06

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP HANA Database Server, Scale-Out Active `Parent` node
2. Host for SAP HANA Database Server, Scale-Out Active Worker node
3. Host for SAP HANA Database Server, Scale-Out Active Worker node
4. Host for SAP HANA Database Server, Scale-Out Active Worker node
5. Host for SAP HANA Database Server, Scale-Out Standby node

The sequence installation is:
- `hdblcm`: Install SAP HANA database server
