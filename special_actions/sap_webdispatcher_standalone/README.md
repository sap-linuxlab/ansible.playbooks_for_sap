# Ansible Playbook - SAP Web Dispatcher installation

The structure of this Ansible Playbook differs from all `deploy_scenarios` in this repository:
- Requires existing SAP System host details and credentials

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

**Critical Note:**
- SAP Gateway HTTP (`33<<ASCS_NN>>`) and HTTPS (`48<<ASCS_NN>>`) must be activated on the backend SAP System
- SAP ICM must be activated on the backend SAP System

---

## Execution of Ansible Playbook

Prior to execution, please read the [full documentation of the Ansible Playbooks for SAP](../docs/README.md) for the capabilities and different execution methods.

## Execution outcome

When executing this Ansible Playbook for SAP, the following hosts are provisioned (unless an Ansible Inventory is provided for existing hosts):
1. Host for SAP Web Dispatcher Standalone

The sequence of a Standard System installation is:
- `SWPM`: Install SAP Web Dispatcher Standalone and connect to backend SAP System

This therefore matches to the SAP SWPM Product ID prefixes that are executed in sequence:
- `NW_Webdispatcher`, Web Dispatcher Standalone
