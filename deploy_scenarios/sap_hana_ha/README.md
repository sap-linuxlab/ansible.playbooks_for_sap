# Ansible Playbook - SAP HANA scale-up with HA

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
1. Host for SAP HANA Database Server, Primary node
2. Host for SAP HANA Database Server, Secondary node

The sequence of installation is:
- `hdblcm`: Install SAP HANA database server
- `yum + pcs/crmsh + cibadmin`: Install Linux Pacemaker and configure dependencies for SAP HANA (e.g. Fence Agents, Resource Agents)
- `hdblcm`: Install SAP HANA System Replication for SAP HANA HA/DR
